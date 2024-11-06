import pytest
import asyncio

# Configuración para pruebas asíncronas
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Fixtures comunes
@pytest.fixture
def mock_env(monkeypatch):
    """Mock variables de entorno"""
    monkeypatch.setenv("PERPLEXITY_API_KEY", "test_key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key")
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    monkeypatch.setenv("GOOGLE_DOC_ID", "test_id")
    monkeypatch.setenv("FOLDER_ID", "test_folder")

@pytest.fixture
def sample_article_data():
    """Datos de prueba para artículos"""
    return {
        "id": "test_123",
        "title": "Test Title",
        "keyword": "test keyword",
        "secondary_keywords": ["kw1", "kw2"],
        "perplexity_query": "Test query for research"
    } 