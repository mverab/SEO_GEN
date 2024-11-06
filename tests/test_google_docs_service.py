import pytest
from unittest.mock import Mock, patch, AsyncMock
from google_docs_service import GoogleDocsService

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def google_docs_service(mock_env):
    """Fixture para GoogleDocsService"""
    service = GoogleDocsService()
    return service

@pytest.mark.asyncio
async def test_save_content(google_docs_service):
    """Prueba guardado de contenido en Google Docs"""
    with patch('google_docs_service.build') as mock_build:
        mock_docs = Mock()
        mock_docs.documents().create().execute.return_value = {"documentId": "test_doc_id"}
        mock_build.return_value = mock_docs
        
        result = await google_docs_service.save_content(
            content="Test content",
            title="Test Title",
            article_id="test_123"
        )
        
        assert result == "test_doc_id"
        mock_docs.documents().create.assert_called_once()
        mock_docs.documents().batchUpdate.assert_called_once()

async def test_save_content_with_error(google_docs_service):
    """Prueba manejo de errores al guardar"""
    with patch('google_docs_service.build') as mock_build:
        mock_docs = Mock()
        mock_docs.documents().create.side_effect = Exception("API Error")
        mock_build.return_value = mock_docs
        
        result = await google_docs_service.save_content(
            content="Test content",
            title="Test Title",
            article_id="test_123"
        )
        
        assert result is None

async def test_save_batch(google_docs_service):
    """Prueba guardado de lote de documentos"""
    with patch('google_docs_service.build') as mock_build:
        mock_docs = Mock()
        mock_docs.documents().create().execute.return_value = {"documentId": "test_doc_id"}
        mock_build.return_value = mock_docs
        
        articles = {
            "test_1": {
                "status": "completed",
                "content": "Content 1",
                "title": "Title 1"
            },
            "test_2": {
                "status": "completed",
                "content": "Content 2",
                "title": "Title 2"
            }
        }
        
        results = await google_docs_service.save_batch(articles)
        
        assert len(results) == 2
        assert all(doc_id == "test_doc_id" for doc_id in results.values())
        assert mock_docs.documents().create.call_count == 2
        assert mock_docs.documents().batchUpdate.call_count == 2