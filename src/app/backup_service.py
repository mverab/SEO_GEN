import os
import json
import logging
from datetime import datetime
from typing import Dict, Optional
import shutil

logger = logging.getLogger(__name__)

class BackupService:
    def __init__(self):
        self.backup_dir = "backups"
        self.ensure_backup_directory()
        
    def ensure_backup_directory(self):
        """Asegura que exista el directorio de respaldos"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            logger.info(f"Directorio de respaldos creado: {self.backup_dir}")
            
    def create_backup_path(self, article_id: str) -> str:
        """Crea estructura de directorios para respaldo"""
        date_str = datetime.now().strftime('%Y%m%d')
        backup_path = os.path.join(self.backup_dir, date_str)
        
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
            
        return backup_path
        
    async def save_backup(
        self,
        content: str,
        metadata: Dict,
        article_id: str
    ) -> Optional[str]:
        """Guarda respaldo local del documento"""
        try:
            backup_path = self.create_backup_path(article_id)
            
            # Guardar contenido
            content_file = os.path.join(backup_path, f"{article_id}_content.md")
            with open(content_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            # Guardar metadata
            metadata_file = os.path.join(backup_path, f"{article_id}_metadata.json")
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Respaldo creado: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Error creando respaldo para {article_id}: {str(e)}")
            return None
            
    async def save_batch_backup(self, articles: Dict[str, Dict]) -> Dict[str, str]:
        """Guarda respaldo de un lote de artículos"""
        results = {}
        for article_id, article_data in articles.items():
            if article_data['status'] == 'completed':
                backup_path = await self.save_backup(
                    article_data['content'],
                    {
                        'id': article_id,
                        'title': article_data.get('title', 'Untitled'),
                        'timestamp': article_data.get('timestamp', datetime.now().isoformat()),
                        'research_data': article_data.get('research_data', '')
                    },
                    article_id
                )
                if backup_path:
                    results[article_id] = backup_path
                    
        return results
        
    def cleanup_old_backups(self, days: int = 30):
        """Limpia respaldos antiguos"""
        try:
            current_date = datetime.now()
            for date_dir in os.listdir(self.backup_dir):
                dir_path = os.path.join(self.backup_dir, date_dir)
                if not os.path.isdir(dir_path):
                    continue
                    
                try:
                    dir_date = datetime.strptime(date_dir, '%Y%m%d')
                    days_old = (current_date - dir_date).days
                    
                    if days_old > days:
                        shutil.rmtree(dir_path)
                        logger.info(f"Respaldo antiguo eliminado: {dir_path}")
                except ValueError:
                    continue
                    
        except Exception as e:
            logger.error(f"Error limpiando respaldos: {str(e)}") 