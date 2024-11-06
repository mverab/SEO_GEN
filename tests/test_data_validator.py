import pytest
from unittest.mock import Mock, patch
import pandas as pd
from data_validator import DataValidator
import os

pytestmark = pytest.mark.asyncio

@pytest.fixture
def validator():
    return DataValidator()

@pytest.fixture
def sample_csv_data():
    return """title,keyword,secondary_keywords,PerplexityQuery
Test Article,test keyword,"kw1, kw2, kw3",What is test keyword?
Another Test,another keyword,"kw4, kw5, kw6",Tell me about another keyword
"""

async def test_validate_csv_structure(validator, sample_csv_data, tmp_path):
    """Prueba validación de estructura del CSV"""
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(sample_csv_data)
    
    df = pd.read_csv(csv_path)
    assert validator.validate_csv_structure(df) == True

async def test_validate_row_valid(validator):
    """Prueba validación de fila válida"""
    row = pd.Series({
        'title': 'Test Title',
        'keyword': 'test keyword',
        'secondary_keywords': 'kw1, kw2, kw3',
        'PerplexityQuery': 'What is test keyword?'
    })
    
    is_valid, errors = validator.validate_row(row, 0)
    assert is_valid == True
    assert len(errors) == 0

async def test_validate_csv_complete(validator, sample_csv_data, tmp_path):
    """Prueba validación completa de CSV"""
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(sample_csv_data)
    
    is_valid, results = validator.validate_csv(str(csv_path))
    assert is_valid == True
    assert results["total"] == 2
    assert results["valid"] == 2