from typing import Dict, List
import asyncio
from datetime import datetime
import pandas as pd
import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from config import BATCH_CONFIG

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('batch_processor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class BatchResearchProcessor:
    def __init__(self, perplexity_api_key: str, anthropic_api_key: str):
        """Inicializa el procesador de investigación por lotes"""
        self.perplexity_client = Client(api_key=perplexity_api_key)
        self.anthropic_client = anthropic.Client(api_key=anthropic_api_key)
        self.queue = asyncio.Queue()
        self.results = {}
        self.batch_size = BATCH_CONFIG["SIZE"]
        
    async def add_to_queue(self, articles_df: pd.DataFrame):
        """Añade artículos a la cola de procesamiento"""
        try:
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
                
        except Exception as e:
            logger.error(f"Error añadiendo artículos a la cola: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(BATCH_CONFIG["MAX_RETRIES"]), 
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def research_article(self, article_data: Dict) -> Dict:
        """Procesa investigación para un artículo"""
        try:
            logger.info(f"Iniciando investigación para artículo {article_data['id']}")
            
            # Obtener investigación de Perplexity
            research = await self.perplexity_client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=[{
                    "role": "user",
                    "content": self._build_research_prompt(
                        article_data["keyword"],
                        article_data["secondary_keywords"]
                    )
                }],
                temperature=0.7,
                search_recency_filter="month"
            )
            
            if research:
                logger.info(f"Investigación completada para {article_data['id']}")
                
                # Generar contenido con Claude
                content = await self._generate_content(
                    article_data,
                    research.choices[0].message.content
                )
                
                return {
                    "id": article_data["id"],
                    "status": "completed",
                    "content": content,
                    "timestamp": datetime.now().isoformat()
                }
            
            logger.warning(f"No se obtuvo investigación para {article_data['id']}")
            return {"status": "failed", "error": "No research data obtained"}
                
        except Exception as e:
            logger.error(f"Error procesando artículo {article_data['id']}: {str(e)}")
            return {"status": "failed", "error": str(e)}
            
    def _build_research_prompt(self, keyword: str, secondary_keywords: List[str]) -> str:
        """Construye el prompt de investigación"""
        return f"""Please search all relevant sources to give the most accurate, valuable and concrete answer about:
        Main topic: {keyword}
        Secondary topics: {', '.join(secondary_keywords)}
        
        Additional instructions:
        - Use english written sources
        - Order answer in SEO friendly way
        - Include semantic context
        - Focus on relevant information for news/blog perspective
        - Use 40% spartan tone, casual style
        - Avoid blank spaces between lines
        """
        
    async def process_batch(self):
        """Procesa artículos en lotes"""
        while True:
            batch = []
            try:
                # Recolectar artículos para el lote
                for _ in range(self.batch_size):
                    if self.queue.empty():
                        break
                    article = await self.queue.get()
                    batch.append(article)
                
                if not batch:
                    logger.info("Cola vacía, finalizando procesamiento")
                    break
                    
                logger.info(f"Procesando lote de {len(batch)} artículos")
                
                # Procesar lote
                tasks = [self.research_article(article) for article in batch]
                results = await asyncio.gather(*tasks)
                
                # Actualizar resultados
                for article, result in zip(batch, results):
                    self.results[article["id"]] = result
                    logger.info(f"Artículo {article['id']} procesado: {result['status']}")
                    
            except Exception as e:
                logger.error(f"Error procesando lote: {str(e)}")
                
            # Respetar rate limits
            await asyncio.sleep(BATCH_CONFIG["RATE_LIMIT_DELAY"])