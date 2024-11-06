import pytest
from unittest.mock import Mock, patch
import asyncio
from research_service import PerplexityResearchService

pytestmark = pytest.mark.asyncio  # Marca todas las pruebas como asíncronas

@pytest.fixture
async def research_service(mock_env):
    service = PerplexityResearchService(
        perplexity_api_key="test_key",
        anthropic_api_key="test_key",
        openai_api_key="test_key"
    )
    return service

async def test_research_service_init(research_service):
    """Prueba inicialización del servicio"""
    assert research_service is not None
    assert research_service.perplexity_client is not None

@pytest.mark.asyncio
async def test_get_research_data(research_service, sample_article_data):
    """Prueba obtención de datos de investigación"""
    with patch.object(research_service.perplexity_client.chat.completions, 'create') as mock_perplexity:
        mock_perplexity.return_value = Mock(
            choices=[Mock(message=Mock(content="Test research data"))]
        )
        
        result = await research_service.get_research_data(
            article_data=sample_article_data,
            tone_file="test_tone.txt"
        )
        
        assert result is not None
        assert "content" in result
        assert "research_data" in result