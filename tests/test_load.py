import pytest
import asyncio
import pandas as pd
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
import numpy as np

from research_service import PerplexityResearchService
from batch_processor import ArticleBatchProcessor
from google_docs_service import GoogleDocsService
from backup_service import BackupService

@pytest.fixture
def large_test_data():
    """Genera un conjunto grande de datos de prueba"""
    num_articles = 50
    return pd.DataFrame({
        'id': range(num_articles),
        'title': [f'Test Article {i}' for i in range(num_articles)],
        'keyword': [f'keyword_{i}' for i in range(num_articles)],
        'secondary_keywords': ['kw1, kw2, kw3'] * num_articles
    })

@pytest.mark.asyncio
async def test_batch_processor_large_load():
    """Prueba procesamiento de lote grande"""
    processor = ArticleBatchProcessor(
        perplexity_api_key="test_key",
        anthropic_api_key="test_key",
        batch_size=20
    )
    
    # Generar datos de prueba
    df = pd.DataFrame({
        'id': range(100),
        'title': ['Test'] * 100,
        'keyword': ['kw'] * 100,
        'secondary_keywords': ['sk1, sk2'] * 100
    })
    
    start_time = datetime.now()
    
    await processor.add_to_queue(df)
    await processor.process_batch()
    
    duration = (datetime.now() - start_time).total_seconds()
    
    # Verificar métricas
    assert processor.processing_stats["total"] == 100
    assert duration >= (100 / 20) * 60  # Debido al rate limiting

@pytest.mark.asyncio
async def test_concurrent_api_calls():
    """Prueba llamadas concurrentes a APIs"""
    research_service = PerplexityResearchService(
        perplexity_api_key="test_key",
        anthropic_api_key="test_key",
        openai_api_key="test_key"
    )
    
    # Simular múltiples llamadas concurrentes
    tasks = []
    for i in range(30):  # Más que el límite de rate
        article_data = {
            "id": f"test_{i}",
            "title": f"Test {i}",
            "keyword": "test",
            "secondary_keywords": ["kw1", "kw2"]
        }
        tasks.append(research_service.get_research_data(article_data, "test_tone.txt"))
    
    start_time = datetime.now()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    duration = (datetime.now() - start_time).total_seconds()
    
    # Verificar rate limiting
    assert duration >= 90  # Al menos 1.5 minutos por rate limiting

@pytest.mark.asyncio
async def test_memory_usage(large_test_data):
    """Prueba uso de memoria con lotes grandes"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    processor = ArticleBatchProcessor(
        perplexity_api_key="test_key",
        anthropic_api_key="test_key"
    )
    
    await processor.add_to_queue(large_test_data)
    await processor.process_batch()
    
    final_memory = process.memory_info().rss
    memory_increase = (final_memory - initial_memory) / 1024 / 1024  # MB
    
    # La memoria no debería aumentar más de 500MB
    assert memory_increase < 500

@pytest.mark.asyncio
async def test_backup_service_large_load(tmp_path):
    """Prueba servicio de respaldo con muchos archivos"""
    backup_service = BackupService()
    backup_service.backup_dir = str(tmp_path)
    
    # Generar muchos artículos
    articles = {
        f"test_{i}": {
            "status": "completed",
            "content": f"Content {i}" * 1000,  # Contenido grande
            "title": f"Title {i}",
            "research_data": f"Research {i}" * 1000
        }
        for i in range(50)
    }
    
    start_time = datetime.now()
    results = await backup_service.save_batch_backup(articles)
    duration = (datetime.now() - start_time).total_seconds()
    
    assert len(results) == 50
    # No debería tomar más de 5 segundos por artículo
    assert duration < 250

@pytest.mark.asyncio
async def test_google_docs_rate_limits():
    """Prueba límites de rate de Google Docs"""
    docs_service = GoogleDocsService()
    
    # Simular guardado de muchos documentos
    tasks = []
    for i in range(40):  # Google tiene límite de ~40 docs/min
        tasks.append(
            docs_service.save_content(
                f"Content {i}",
                f"Title {i}",
                f"id_{i}"
            )
        )
    
    start_time = datetime.now()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    duration = (datetime.now() - start_time).total_seconds()
    
    # Debería tomar al menos 60 segundos por rate limiting
    assert duration >= 60

def test_csv_validation_performance():
    """Prueba rendimiento de validación de CSV grande"""
    # Generar CSV grande
    num_rows = 10000
    df = pd.DataFrame({
        'title': [f'Test {i}' for i in range(num_rows)],
        'keyword': [f'kw_{i}' for i in range(num_rows)],
        'secondary_keywords': ['sk1, sk2, sk3'] * num_rows,
        'id': range(num_rows)
    })
    
    from data_validator import DataValidator
    validator = DataValidator()
    
    start_time = datetime.now()
    is_valid, results = validator.validate_csv(df)
    duration = (datetime.now() - start_time).total_seconds()
    
    # La validación no debería tomar más de 5 segundos
    assert duration < 5 