from typing import Dict, List
import asyncio
from datetime import datetime
import pandas as pd
from research_service import PerplexityResearchService
from config import PERPLEXITY_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY, BATCH_CONFIG
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class ArticleBatchProcessor:
    def __init__(self, perplexity_api_key: str, anthropic_api_key: str, openai_api_key: str):
        self.research_service = PerplexityResearchService(
            perplexity_api_key=perplexity_api_key,
            anthropic_api_key=anthropic_api_key,
            openai_api_key=openai_api_key
        )
        self.queue = asyncio.Queue()
        self.results = {}
        self.batch_size = BATCH_CONFIG["SIZE"]
        self.failed_items = []
        self.processing_stats = {
            "total": 0,
            "completed": 0,
            "failed": 0,
            "start_time": None,
            "end_time": None
        }
        
    async def add_to_queue(self, articles_df: pd.DataFrame):
        """Añade artículos a la cola de procesamiento"""
        try:
            # Validar estructura del DataFrame
            required_columns = ['id', 'title', 'keyword', 'secondary_keywords']
            if not all(col in articles_df.columns for col in required_columns):
                raise ValueError(f"CSV debe contener las columnas: {required_columns}")
            
            self.processing_stats["total"] = len(articles_df)
            self.processing_stats["start_time"] = datetime.now()
            
            for _, row in articles_df.iterrows():
                article_data = {
                    "id": f"{datetime.now().strftime('%Y%m%d')}_{row['id']}",
                    "title": row['title'],
                    "keyword": row['keyword'],
                    "secondary_keywords": row['secondary_keywords'].split(','),
                    "status": "pending",
                    "retries": 0
                }
                await self.queue.put(article_data)
                self.results[article_data["id"]] = {"status": "queued"}
                logger.info(f"Artículo {article_data['id']} añadido a la cola")
                
        except Exception as e:
            logger.error(f"Error al cargar artículos: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(BATCH_CONFIG["MAX_RETRIES"]),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def process_article(self, article_data: Dict):
        """Procesa un artículo individual con reintentos"""
        try:
            logger.info(f"Procesando artículo {article_data['id']}")
            result = await self.research_service.get_research_data(
                article_data,
                'tone.txt'
            )
            
            if result:
                self.processing_stats["completed"] += 1
                logger.info(f"Artículo {article_data['id']} procesado exitosamente")
                return {
                    "status": "completed",
                    "content": result['content'],
                    "research_data": result['research_data'],
                    "timestamp": datetime.now().isoformat()
                }
            
            self.processing_stats["failed"] += 1
            self.failed_items.append(article_data)
            logger.error(f"No se pudo procesar el artículo {article_data['id']}")
            return {"status": "failed", "error": "No research data obtained"}
                
        except Exception as e:
            self.processing_stats["failed"] += 1
            self.failed_items.append(article_data)
            logger.error(f"Error procesando artículo {article_data['id']}: {str(e)}")
            return {"status": "failed", "error": str(e)}

    async def process_batch(self):
        """Procesa artículos en lotes con manejo mejorado"""
        try:
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
                    tasks = [self.process_article(article) for article in batch]
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    # Procesar resultados
                    for article, result in zip(batch, results):
                        if isinstance(result, Exception):
                            self.results[article["id"]] = {
                                "status": "failed",
                                "error": str(result)
                            }
                            self.failed_items.append(article)
                        else:
                            self.results[article["id"]] = result
                        
                except Exception as e:
                    logger.error(f"Error procesando lote: {str(e)}")
                    for article in batch:
                        self.failed_items.append(article)
                
                # Respetar rate limits
                await asyncio.sleep(BATCH_CONFIG["RATE_LIMIT_DELAY"])
                
            # Actualizar estadísticas finales
            self.processing_stats["end_time"] = datetime.now()
            self.log_processing_stats()
            
        except Exception as e:
            logger.error(f"Error fatal en procesamiento por lotes: {str(e)}")
            raise

    def log_processing_stats(self):
        """Registra estadísticas del procesamiento"""
        duration = self.processing_stats["end_time"] - self.processing_stats["start_time"]
        logger.info("\n=== Estadísticas de Procesamiento ===")
        logger.info(f"Total de artículos: {self.processing_stats['total']}")
        logger.info(f"Completados: {self.processing_stats['completed']}")
        logger.info(f"Fallidos: {self.processing_stats['failed']}")
        logger.info(f"Duración total: {duration}")
        logger.info(f"Artículos fallidos: {len(self.failed_items)}")