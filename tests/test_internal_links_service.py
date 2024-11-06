import pytest
from unittest.mock import Mock, patch
import pandas as pd
from internal_links_service import InternalLinksService

@pytest.fixture
def links_service():
    return InternalLinksService("test_openai_key")

@pytest.fixture
def sample_links_data():
    return """URL,Descripción
https://test.com/1,"Esta es una descripción de prueba uno"
https://test.com/2,"Esta es una descripción de prueba dos"
https://test.com/3,"Esta es una descripción de prueba tres"
"""

@pytest.mark.asyncio
async def test_load_links(links_service, sample_links_data, tmp_path):
    """Prueba la carga de enlaces desde CSV"""
    # Crear archivo temporal
    csv_path = tmp_path / "test_links.csv"
    csv_path.write_text(sample_links_data)
    
    links_service.load_links(str(csv_path))
    
    assert links_service.links_data is not None
    assert len(links_service.links_data) == 3
    assert all(col in links_service.links_data.columns for col in ['URL', 'Descripción'])

@pytest.mark.asyncio
async def test_find_relevant_links(links_service, sample_links_data, tmp_path):
    """Prueba búsqueda de enlaces relevantes"""
    # Configurar datos de prueba
    csv_path = tmp_path / "test_links.csv"
    csv_path.write_text(sample_links_data)
    links_service.load_links(str(csv_path))
    
    # Mock para embeddings
    mock_embeddings = {
        "keyword": [0.8, 0.1, 0.1],
        "desc1": [0.7, 0.2, 0.1],
        "desc2": [0.1, 0.8, 0.1],
        "desc3": [0.1, 0.1, 0.8]
    }
    
    async def mock_get_embedding(text):
        if "uno" in text.lower():
            return mock_embeddings["desc1"]
        elif "dos" in text.lower():
            return mock_embeddings["desc2"]
        elif "tres" in text.lower():
            return mock_embeddings["desc3"]
        return mock_embeddings["keyword"]
    
    with patch.object(links_service, 'get_embedding', side_effect=mock_get_embedding):
        results = await links_service.find_relevant_links("test keyword", num_links=2)
        
        assert len(results) == 2
        # El primer resultado debería ser el más similar
        assert "test.com/1" in results[0]["url"]

def test_format_link_for_content(links_service):
    """Prueba formateo de enlaces para contenido"""
    link_data = {
        "url": "https://test.com/page",
        "description": "Esta es una descripción de prueba. Con más texto."
    }
    
    formatted = links_service.format_link_for_content(link_data)
    assert formatted == "[Esta es una descripción de prueba](https://test.com/page)"
    assert formatted.startswith("[")
    assert formatted.endswith(")")
    assert "https://test.com/page" in formatted 