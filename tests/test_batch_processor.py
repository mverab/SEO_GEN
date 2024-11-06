import pytest
from unittest.mock import Mock, patch, AsyncMock
import pandas as pd
from batch_processor import ArticleBatchProcessor

@pytest.fixture
async def batch_processor(mock_env):
    return ArticleBatchProcessor(
        perplexity_api_key="test_key",
        anthropic_api_key="test_key",
        openai_api_key="test_key"
    )

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

async def test_add_to_queue(batch_processor, sample_df):
    """Prueba añadir artículos a la cola"""
    await batch_processor.add_to_queue(sample_df)
    assert batch_processor.processing_stats["total"] == 2
    assert len(batch_processor.results) == 2

@pytest.mark.asyncio
async def test_process_batch(batch_processor, sample_df):
    """Prueba procesamiento por lotes"""
    with patch.object(batch_processor.research_service, 'get_research_data', 
                     new_callable=AsyncMock) as mock_research:
        mock_research.return_value = {
            "content": "Test content",
            "research_data": "Test research"
        }
        
        await batch_processor.add_to_queue(sample_df)
        await batch_processor.process_batch()
        
        assert batch_processor.processing_stats["completed"] == 2
        assert batch_processor.processing_stats["failed"] == 0

async def test_error_handling(batch_processor, sample_df):
    """Prueba manejo de errores"""
    with patch.object(batch_processor.research_service, 'get_research_data', 
                     side_effect=Exception("Test error")):
        await batch_processor.add_to_queue(sample_df)
        await batch_processor.process_batch()
        
        assert batch_processor.processing_stats["failed"] > 0
        assert len(batch_processor.failed_items) > 0

async def test_rate_limiting(batch_processor):
    """Prueba rate limiting"""
    large_df = pd.DataFrame({
        'id': range(25),
        'title': ['Test'] * 25,
        'keyword': ['kw'] * 25,
        'secondary_keywords': ['sk1, sk2'] * 25,
        'PerplexityQuery': ['Query'] * 25
    })
    
    start_time = asyncio.get_event_loop().time()
    
    await batch_processor.add_to_queue(large_df)
    await batch_processor.process_batch()
    
    duration = asyncio.get_event_loop().time() - start_time
    assert duration >= 60  # Debería tomar al menos 60 segundos por rate limiting