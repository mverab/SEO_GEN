from typing import Dict, List
import asyncio
from datetime import datetime
import pandas as pd
from research_service import PerplexityResearchService
from config import PERPLEXITY_API_KEY, ANTHROPIC_API_KEY, BATCH_CONFIG
import logging

logger = logging.getLogger(__name__)

class ArticleBatchProcessor:
    def __init__(self, perplexity_api_key: str, anthropic_api_key: str, batch_size: int = 10):
        self.research_service = PerplexityResearchService(perplexity_api_key, anthropic_api_key)
        self.batch_size = batch_size
        self.queue = asyncio.Queue()
        self.results = {}
        
    async def add_to_queue(self, articles_df: pd.DataFrame):
        """Añade artículos a la cola de procesamiento"""
        for _, row in articles_df.iterrows():
            article_data = {
                "id": f"{datetime.now().strftime('%Y%m%d')}_{row['id']}",
                "title": row['title'],
                "keyword": row['keyword'],
                "secondary_keywords": row['secondary_keywords'].split(','),
                "status": "pending"
            }
            await self.queue.put(article_data)
            self.results[article_data["id"]] = {"status": "queued"}
            logger.info(f"Artículo {article_data['id']} añadido a la cola")

    async def process_article(self, article_data: Dict):
        """Procesa un artículo individual"""
        try:
            logger.info(f"Procesando artículo {article_data['id']}")
            result = await self.research_service.get_research_data(
                article_data,
                'tone.txt'
            )
            
            if result:
                logger.info(f"Artículo {article_data['id']} procesado exitosamente")
                return {
                    "status": "completed",
                    "content": result['content'],
                    "research_data": result['research_data'],
                    "timestamp": datetime.now().isoformat()
                }
            
            logger.error(f"No se pudo procesar el artículo {article_data['id']}")
            return {"status": "failed", "error": "No research data obtained"}
                
        except Exception as e:
            logger.error(f"Error procesando artículo {article_data['id']}: {str(e)}")
            return {"status": "failed", "error": str(e)}

    async def process_batch(self):
        """Procesa artículos en lotes"""
        while True:
            batch = []
            try:
                for _ in range(self.batch_size):
                    if self.queue.empty():
                        break
                    article = await self.queue.get()
                    batch.append(article)
                
                if not batch:
                    logger.info("Cola vacía, finalizando procesamiento")
                    break
                    
                logger.info(f"Procesando lote de {len(batch)} artículos")
                tasks = [self.process_article(article) for article in batch]
                results = await asyncio.gather(*tasks)
                
                for article, result in zip(batch, results):
                    self.results[article["id"]] = result
                    
            except Exception as e:
                logger.error(f"Error procesando lote: {str(e)}")
                
            await asyncio.sleep(BATCH_CONFIG["RATE_LIMIT_DELAY"])