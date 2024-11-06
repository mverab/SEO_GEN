import asyncio
import logging
import pandas as pd
from research_service import PerplexityResearchService
from batch_processor import ArticleBatchProcessor
from google_docs_service import GoogleDocsService
from config import PERPLEXITY_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_batch():
    """Procesa el lote de artículos"""
    try:
        # Usar ruta predefinida
        csv_file = "data/input/test_articles.csv"
        
        processor = ArticleBatchProcessor(
            perplexity_api_key=PERPLEXITY_API_KEY,
            anthropic_api_key=ANTHROPIC_API_KEY,
            openai_api_key=OPENAI_API_KEY
        )
        
        await processor.add_to_queue(pd.read_csv(csv_file))
        await processor.process_batch()
        
        return processor.results
        
    except Exception as e:
        logger.error(f"Error en procesamiento por lotes: {str(e)}")
        return None

async def main():
    try:
        # Inicializar servicios
        research_service = PerplexityResearchService(
            perplexity_api_key=PERPLEXITY_API_KEY,
            anthropic_api_key=ANTHROPIC_API_KEY,
            openai_api_key=OPENAI_API_KEY
        )
        
        # Verificar acceso a APIs
        if not await research_service.validate_api_access():
            logger.error("Error validando acceso a APIs")
            return
            
        # Procesar directamente en modo batch
        results = await process_batch()
        
        if results:
            logger.info("Procesamiento por lotes completado")
            # Guardar en Google Docs
            docs_service = GoogleDocsService()
            doc_ids = await docs_service.save_batch(results)
            
            if doc_ids:
                logger.info("Documentos guardados:")
                for article_id, doc_id in doc_ids.items():
                    logger.info(f"- {article_id}: https://docs.google.com/document/d/{doc_id}/edit")
            else:
                logger.error("Error al guardar en Google Docs")
        else:
            logger.error("Error en procesamiento por lotes")
                
    except Exception as e:
        logger.error(f"Error en ejecución: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
