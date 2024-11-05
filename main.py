import os
import sys
import asyncio
import logging
from datetime import datetime
import pandas as pd
import anthropic
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from config import (
    PERPLEXITY_API_KEY, 
    ANTHROPIC_API_KEY, 
    OPENAI_API_KEY,
    GOOGLE_DOC_ID, 
    FOLDER_ID, 
    FEATURE_FLAGS
)
from batch_processor import ArticleBatchProcessor
from research_service import PerplexityResearchService
from google_docs_service import GoogleDocsService
from data_validator import DataValidator
from backup_service import BackupService

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def read_file(filename):
    try:
        with open(os.path.join(os.path.dirname(__file__), filename), "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"El archivo {filename} no existe.")
        sys.exit(1)

def validate_input(prompt: str) -> str:
    """Valida entrada del usuario"""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Este campo no puede estar vacío.")

def check_google_credentials():
    """Verifica credenciales de Google"""
    if not os.path.exists('credentials.json'):
        logger.error("""
Error: No se encontró el archivo credentials.json
Por favor:
1. Ve a Google Cloud Console
2. Crea o selecciona un proyecto
3. Habilita las APIs de Google Drive y Google Docs
4. Crea credenciales OAuth 2.0
5. Descarga el archivo credentials.json
6. Coloca el archivo en el directorio del proyecto
        """)
        return False
    return True

async def process_batch(csv_file: str):
    """Procesa un lote de artículos desde CSV"""
    try:
        # Validar CSV primero
        validator = DataValidator()
        is_valid, validation_results = validator.validate_csv(csv_file)
        
        if not is_valid:
            logger.error("Validación de CSV fallida:")
            for error in validation_results["errors"]:
                logger.error(f"- {error}")
            return None
            
        logger.info(f"CSV validado exitosamente: {validation_results['valid']} filas válidas")
        
        # Proceder con el procesamiento
        processor = ArticleBatchProcessor(
            perplexity_api_key=PERPLEXITY_API_KEY,
            anthropic_api_key=ANTHROPIC_API_KEY
        )
        
        await processor.add_to_queue(pd.read_csv(csv_file))
        await processor.process_batch()
        
        return processor.results
        
    except Exception as e:
        logger.error(f"Error en procesamiento por lotes: {e}")
        return None

async def main():
    if not check_google_credentials():
        sys.exit(1)
    
    # Inicializar servicios con todas las API keys necesarias
    research_service = PerplexityResearchService(
        perplexity_api_key=PERPLEXITY_API_KEY,
        anthropic_api_key=ANTHROPIC_API_KEY,
        openai_api_key=OPENAI_API_KEY
    )
    docs_service = GoogleDocsService()
    backup_service = BackupService()
    
    # Verificar acceso a APIs
    if not await research_service.validate_api_access():
        logger.error("Error validando acceso a APIs")
        sys.exit(1)
    
    # Modo de operación
    mode = validate_input(
        "Seleccione modo (1: Individual, 2: Batch): "
    )
    
    if mode == "1":
        # Modo individual
        topic = validate_input("Ingresa el tópico: ")
        title = validate_input("Ingresa el título: ")
        keyword = validate_input("Ingresa palabra clave principal: ")
        secondary_keywords = validate_input("Ingresa palabras clave secundarias (separadas por coma): ")
        
        article_data = {
            "id": datetime.now().strftime('%Y%m%d_%H%M%S'),
            "title": title,
            "topic": topic,
            "keyword": keyword,
            "secondary_keywords": [k.strip() for k in secondary_keywords.split(',')]
        }
        
        result = await research_service.get_research_data(article_data, read_file('tone.txt'))
        if result:
            logger.info("Contenido generado exitosamente")
            
            # Crear respaldo local
            backup_path = await backup_service.save_backup(
                result['content'],
                {
                    'id': article_data['id'],
                    'title': article_data['title'],
                    'research_data': result['research_data']
                },
                article_data['id']
            )
            
            if backup_path:
                logger.info(f"Respaldo creado en: {backup_path}")
            
            # Guardar en Google Docs
            doc_id = await docs_service.save_content(
                result['content'],
                article_data['title'],
                article_data['id']
            )
            if doc_id:
                logger.info(f"Documento guardado: https://docs.google.com/document/d/{doc_id}/edit")
            else:
                logger.error("Error al guardar en Google Docs")
        else:
            logger.error("Error generando contenido")
            
    elif mode == "2":
        # Modo batch
        while True:
            csv_file = validate_input("Ingresa ruta del archivo CSV: ")
            
            if not os.path.exists(csv_file):
                logger.error("El archivo no existe")
                continue
                
            if not csv_file.endswith('.csv'):
                logger.error("El archivo debe ser un CSV")
                continue
                
            break
            
        results = await process_batch(csv_file)
        if results:
            logger.info("Procesamiento por lotes completado")
            
            # Crear respaldos del lote
            backup_paths = await backup_service.save_batch_backup(results)
            if backup_paths:
                logger.info("Respaldos creados:")
                for article_id, path in backup_paths.items():
                    logger.info(f"- {article_id}: {path}")
            
            # Guardar lote en Google Docs
            doc_ids = await docs_service.save_batch(results)
            if doc_ids:
                logger.info("Documentos guardados:")
                for article_id, doc_id in doc_ids.items():
                    logger.info(f"- {article_id}: https://docs.google.com/document/d/{doc_id}/edit")
            else:
                logger.error("Error al guardar lote en Google Docs")
        else:
            logger.error("Error en procesamiento por lotes")
    else:
        logger.error("Modo no válido")
        
    # Limpiar respaldos antiguos
    backup_service.cleanup_old_backups()

if __name__ == "__main__":
    asyncio.run(main())
