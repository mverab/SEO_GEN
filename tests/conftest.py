import pytest
import asyncio
import pandas as pd

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
async def research_service():
    """Fixture para PerplexityResearchService"""
    return PerplexityResearchService(
        api_key="test_key"  # Solo necesita una API key según la clase actual
    )

@pytest.fixture
def sample_article_data():
    """Fixture para datos de prueba"""
    return {
        "id": "test_123",
        "title": "Test Title",
        "keyword": "test keyword",
        "secondary_keywords": ["kw1", "kw2"],
        "perplexity_query": "Test query"
    }

@pytest.fixture
def sample_df():
    """Fixture para DataFrame de prueba"""
    return pd.DataFrame({
        'id': [1, 2],
        'title': ['Test 1', 'Test 2'],
        'keyword': ['kw1', 'kw2'],
        'secondary_keywords': ['sk1, sk2', 'sk3, sk4'],
        'PerplexityQuery': ['Query 1', 'Query 2']
    })