import pytest
import os
from unittest.mock import Mock, patch
from backup_service import BackupService
from datetime import datetime, timedelta
import json

@pytest.fixture
def backup_service(tmp_path):
    service = BackupService()
    service.backup_dir = str(tmp_path)  # Usar directorio temporal para pruebas
    return service

@pytest.mark.asyncio
async def test_save_backup(backup_service):
    """Prueba guardado de respaldo individual"""
    content = "Test content"
    metadata = {
        "id": "test_123",
        "title": "Test Title",
        "research_data": "Test research"
    }
    article_id = "test_123"
    
    backup_path = await backup_service.save_backup(content, metadata, article_id)
    
    assert backup_path is not None
    assert os.path.exists(backup_path)
    
    # Verificar contenido
    content_file = os.path.join(backup_path, f"{article_id}_content.md")
    assert os.path.exists(content_file)
    with open(content_file, 'r', encoding='utf-8') as f:
        assert f.read() == content
        
    # Verificar metadata
    metadata_file = os.path.join(backup_path, f"{article_id}_metadata.json")
    assert os.path.exists(metadata_file)
    with open(metadata_file, 'r', encoding='utf-8') as f:
        saved_metadata = json.load(f)
        assert saved_metadata == metadata

@pytest.mark.asyncio
async def test_save_batch_backup(backup_service):
    """Prueba guardado de respaldo en lote"""
    articles = {
        "test_1": {
            "status": "completed",
            "content": "Content 1",
            "title": "Title 1",
            "research_data": "Research 1"
        },
        "test_2": {
            "status": "completed",
            "content": "Content 2",
            "title": "Title 2",
            "research_data": "Research 2"
        }
    }
    
    results = await backup_service.save_batch_backup(articles)
    
    assert len(results) == 2
    for article_id, backup_path in results.items():
        assert os.path.exists(backup_path)
        assert os.path.exists(os.path.join(backup_path, f"{article_id}_content.md"))
        assert os.path.exists(os.path.join(backup_path, f"{article_id}_metadata.json"))

@pytest.mark.asyncio
async def test_cleanup_old_backups(backup_service):
    """Prueba limpieza de respaldos antiguos"""
    # Crear respaldos con diferentes fechas
    dates = [
        datetime.now() - timedelta(days=40),  # Antiguo
        datetime.now() - timedelta(days=20),  # Reciente
        datetime.now()  # Actual
    ]
    
    for date in dates:
        date_str = date.strftime('%Y%m%d')
        path = os.path.join(backup_service.backup_dir, date_str)
        os.makedirs(path, exist_ok=True)
        # Crear archivo de prueba
        with open(os.path.join(path, "test.txt"), "w") as f:
            f.write("test")
            
    # Ejecutar limpieza
    backup_service.cleanup_old_backups(days=30)
    
    # Verificar resultados
    remaining_dirs = os.listdir(backup_service.backup_dir)
    assert len(remaining_dirs) == 2  # Solo deberían quedar los últimos dos
    
    # El directorio más antiguo debería haberse eliminado
    old_date = dates[0].strftime('%Y%m%d')
    assert old_date not in remaining_dirs

def test_ensure_backup_directory(backup_service):
    """Prueba creación de directorio de respaldo"""
    assert not os.path.exists(backup_service.backup_dir)
    backup_service.ensure_backup_directory()
    assert os.path.exists(backup_service.backup_dir)

@pytest.mark.asyncio
async def test_save_backup_with_invalid_data(backup_service):
    """Prueba manejo de errores en guardado"""
    result = await backup_service.save_backup(
        None,  # Contenido inválido
        {},    # Metadata vacía
        ""     # ID vacío
    )
    assert result is None

def test_cleanup_with_invalid_dates(backup_service):
    """Prueba limpieza con nombres de directorio inválidos"""
    # Crear directorios con nombres inválidos
    os.makedirs(os.path.join(backup_service.backup_dir, "invalid_date"), exist_ok=True)
    os.makedirs(os.path.join(backup_service.backup_dir, "20240101"), exist_ok=True)
    
    # No debería lanzar error
    backup_service.cleanup_old_backups()
    
    # El directorio válido debería permanecer
    assert "20240101" in os.listdir(backup_service.backup_dir) 