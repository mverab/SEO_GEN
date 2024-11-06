import pytest
import os
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from research_service import PerplexityResearchService
from batch_processor import ArticleBatchProcessor
from google_docs_service import GoogleDocsService
from backup_service import BackupService
from data_validator import DataValidator

@pytest.fixture
def test_csv_data():
    return """title,keyword,secondary_keywords,id
Test Article,test keyword,"kw1, kw2, kw3",1
Another Test,another keyword,"kw4, kw5, kw6",2
"""

@pytest.fixture
def mock_services():
    """Configura mocks para todos los servicios"""
    with patch('research_service.PerplexityResearchService') as mock_research, \
         patch('google_docs_service.GoogleDocsService') as mock_docs, \
         patch('backup_service.BackupService') as mock_backup:
        
        # Mock para PerplexityResearchService
        mock_research.return_value.get_research_data.return_value = {
            "content": "Test content",
            "research_data": "Test research",
            "internal_links": ["[Link1](url1)"]
        }
        
        # Mock para GoogleDocsService
        mock_docs.return_value.save_content.return_value = "test_doc_id"
        mock_docs.return_value.save_batch.return_value = {
            "test_1": "doc_id_1",
            "test_2": "doc_id_2"
        }
        
        # Mock para BackupService
        mock_backup.return_value.save_backup.return_value = "/test/backup/path"
        mock_backup.return_value.save_batch_backup.return_value = {
            "test_1": "/backup/1",
            "test_2": "/backup/2"
        }
        
        yield {
            "research": mock_research,
            "docs": mock_docs,
            "backup": mock_backup
        }

@pytest.mark.asyncio
async def test_full_article_flow(test_csv_data, mock_services, tmp_path):
    """Prueba el flujo completo de procesamiento de artículo"""
    # Preparar datos de prueba
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(test_csv_data)
    
    # Inicializar servicios
    validator = DataValidator()
    processor = ArticleBatchProcessor(
        perplexity_api_key="test_key",
        anthropic_api_key="test_key"
    )
    
    # Validar CSV
    is_valid, results = validator.validate_csv(str(csv_path))
    assert is_valid == True
    
    # Procesar artículos
    df = pd.read_csv(csv_path)
    await processor.add_to_queue(df)
    await processor.process_batch()
    
    # Verificar resultados
    assert len(processor.results) == 2
    assert processor.processing_stats["completed"] > 0
    assert processor.processing_stats["failed"] == 0

@pytest.mark.asyncio
async def test_error_handling_flow(test_csv_data, mock_services, tmp_path):
    """Prueba el manejo de errores en el flujo"""
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(test_csv_data)
    
    # Simular error en investigación
    mock_services["research"].return_value.get_research_data.side_effect = Exception("API Error")
    
    processor = ArticleBatchProcessor(
        perplexity_api_key="test_key",
        anthropic_api_key="test_key"
    )
    
    df = pd.read_csv(csv_path)
    await processor.add_to_queue(df)
    await processor.process_batch()
    
    assert processor.processing_stats["failed"] > 0
    assert len(processor.failed_items) > 0

@pytest.mark.asyncio
async def test_backup_and_docs_flow(test_csv_data, mock_services, tmp_path):
    """Prueba el flujo de respaldo y guardado en Google Docs"""
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(test_csv_data)
    
    processor = ArticleBatchProcessor(
        perplexity_api_key="test_key",
        anthropic_api_key="test_key"
    )
    
    backup_service = BackupService()
    docs_service = GoogleDocsService()
    
    # Procesar artículos
    df = pd.read_csv(csv_path)
    await processor.add_to_queue(df)
    await processor.process_batch()
    
    # Crear respaldos
    backup_paths = await backup_service.save_batch_backup(processor.results)
    assert len(backup_paths) > 0
    
    # Guardar en Google Docs
    doc_ids = await docs_service.save_batch(processor.results)
    assert len(doc_ids) > 0

@pytest.mark.asyncio
async def test_rate_limiting(mock_services):
    """Prueba el rate limiting"""
    processor = ArticleBatchProcessor(
        perplexity_api_key="test_key",
        anthropic_api_key="test_key",
        batch_size=25  # Más que el límite de 20/min
    )
    
    start_time = datetime.now()
    
    # Simular procesamiento de lote grande
    df = pd.DataFrame({
        'id': range(25),
        'title': ['Test'] * 25,
        'keyword': ['kw'] * 25,
        'secondary_keywords': ['sk1, sk2'] * 25
    })
    
    await processor.add_to_queue(df)
    await processor.process_batch()
    
    duration = (datetime.now() - start_time).total_seconds()
    
    # Debería haber tomado al menos 60 segundos por rate limiting
    assert duration >= 60

@pytest.mark.asyncio
async def test_internal_links_integration(mock_services, tmp_path):
    """Prueba la integración de enlaces internos"""
    article_data = {
        "id": "test_123",
        "title": "Test Title",
        "keyword": "test keyword",
        "secondary_keywords": ["kw1", "kw2"]
    }
    
    research_service = PerplexityResearchService(
        perplexity_api_key="test_key",
        anthropic_api_key="test_key",
        openai_api_key="test_key"
    )
    
    # Crear archivo de enlaces de prueba
    links_csv = tmp_path / "test_links.csv"
    links_csv.write_text("""URL,Descripción
https://test.com/1,"Test description one"
https://test.com/2,"Test description two"
""")
    
    result = await research_service.get_research_data(
        article_data,
        "test_tone.txt",
        str(links_csv)
    )
    
    assert result is not None
    assert "internal_links" in result
    assert len(result["internal_links"]) > 0 