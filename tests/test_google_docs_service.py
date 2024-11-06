import pytest
from unittest.mock import Mock, patch, MagicMock
from google_docs_service import GoogleDocsService
from google.oauth2.credentials import Credentials

@pytest.fixture
def mock_credentials():
    return Mock(spec=Credentials)

@pytest.fixture
def docs_service(mock_credentials):
    with patch('google.oauth2.credentials.Credentials.from_authorized_user_file') as mock_creds:
        mock_creds.return_value = mock_credentials
        service = GoogleDocsService()
        return service

@pytest.mark.asyncio
async def test_save_content(docs_service):
    """Prueba guardado de contenido en Google Docs"""
    # Mock para el servicio de Docs
    mock_docs = MagicMock()
    mock_docs.documents().create().execute.return_value = {"documentId": "test_doc_id"}
    docs_service.docs_service = mock_docs
    
    # Mock para el servicio de Drive
    mock_drive = MagicMock()
    docs_service.drive_service = mock_drive
    
    result = await docs_service.save_content(
        content="Test content",
        title="Test Title",
        article_id="test_123"
    )
    
    assert result == "test_doc_id"
    mock_docs.documents().create.assert_called_once()
    mock_docs.documents().batchUpdate.assert_called_once()
    mock_drive.files().update.assert_called_once()

@pytest.mark.asyncio
async def test_save_content_with_error(docs_service):
    """Prueba manejo de errores al guardar"""
    mock_docs = MagicMock()
    mock_docs.documents().create.side_effect = Exception("API Error")
    docs_service.docs_service = mock_docs
    
    result = await docs_service.save_content(
        content="Test content",
        title="Test Title",
        article_id="test_123"
    )
    
    assert result is None

@pytest.mark.asyncio
async def test_save_batch(docs_service):
    """Prueba guardado de lote de documentos"""
    # Mock para el servicio de Docs
    mock_docs = MagicMock()
    mock_docs.documents().create().execute.return_value = {"documentId": "test_doc_id"}
    docs_service.docs_service = mock_docs
    
    # Mock para el servicio de Drive
    mock_drive = MagicMock()
    docs_service.drive_service = mock_drive
    
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
    
    results = await docs_service.save_batch(articles)
    
    assert len(results) == 2
    assert all(doc_id == "test_doc_id" for doc_id in results.values())
    assert mock_docs.documents().create.call_count == 2
    assert mock_docs.documents().batchUpdate.call_count == 2

def test_authentication_flow(mock_credentials):
    """Prueba flujo de autenticación"""
    with patch('google.oauth2.credentials.Credentials.from_authorized_user_file') as mock_creds, \
         patch('google.auth.transport.requests.Request') as mock_request, \
         patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file') as mock_flow:
        
        # Simular credenciales expiradas que necesitan refresh
        mock_credentials.valid = False
        mock_credentials.expired = True
        mock_credentials.refresh_token = "test_refresh_token"
        mock_creds.return_value = mock_credentials
        
        service = GoogleDocsService()
        
        mock_request.assert_called_once()
        assert service.docs_service is not None
        assert service.drive_service is not None

def test_authentication_new_flow(mock_credentials):
    """Prueba flujo de autenticación nuevo"""
    with patch('google.oauth2.credentials.Credentials.from_authorized_user_file') as mock_creds, \
         patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file') as mock_flow:
        
        # Simular que no hay credenciales previas
        mock_creds.side_effect = FileNotFoundError()
        mock_flow.return_value.run_local_server.return_value = mock_credentials
        
        service = GoogleDocsService()
        
        mock_flow.assert_called_once()
        assert service.docs_service is not None
        assert service.drive_service is not None

@pytest.mark.asyncio
async def test_save_content_formatting(docs_service):
    """Prueba formato de contenido al guardar"""
    mock_docs = MagicMock()
    mock_docs.documents().create().execute.return_value = {"documentId": "test_doc_id"}
    docs_service.docs_service = mock_docs
    
    test_content = "# Title\n\nTest content with **bold** and *italic*"
    
    await docs_service.save_content(
        content=test_content,
        title="Test Title",
        article_id="test_123"
    )
    
    # Verificar que se llamó a batchUpdate con el formato correcto
    batch_update_call = mock_docs.documents().batchUpdate.call_args[1]
    assert "requests" in batch_update_call["body"]
    assert batch_update_call["body"]["requests"][0]["insertText"]["text"] == test_content 