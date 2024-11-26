from typing import List, Dict, Optional
import json
import os
from datetime import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ResourceService:
    def __init__(self, storage_dir: str = "resources"):
        """Inicializa el servicio de recursos"""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.resources_file = self.storage_dir / "resources.json"
        self.load_resources()

    def load_resources(self):
        """Carga recursos existentes"""
        if self.resources_file.exists():
            with open(self.resources_file, 'r', encoding='utf-8') as f:
                self.resources = json.load(f)
        else:
            self.resources = {
                "niches": {},
                "metadata": {
                    "last_updated": datetime.now().isoformat()
                }
            }
            self._save_resources()

    def _save_resources(self):
        """Guarda recursos en disco"""
        with open(self.resources_file, 'w', encoding='utf-8') as f:
            json.dump(self.resources, f, indent=2, ensure_ascii=False)

    def add_niche_resource(
        self,
        niche: str,
        content: str,
        resource_type: str = "text",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Agrega un recurso a un nicho"""
        if niche not in self.resources["niches"]:
            self.resources["niches"][niche] = []

        resource = {
            "id": len(self.resources["niches"][niche]) + 1,
            "type": resource_type,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat()
        }

        self.resources["niches"][niche].append(resource)
        self._save_resources()
        return resource

    def get_niche_resources(self, niche: str) -> List[Dict]:
        """Obtiene recursos de un nicho"""
        return self.resources["niches"].get(niche, [])

    def get_resource_context(self, niche: str) -> str:
        """Genera contexto basado en recursos del nicho"""
        resources = self.get_niche_resources(niche)
        if not resources:
            return ""

        context = f"Contexto del nicho '{niche}':\n\n"
        
        for resource in resources:
            if resource["type"] == "text":
                context += f"- {resource['content']}\n"
            elif resource["type"] == "image":
                context += f"- Imagen: {resource['metadata'].get('description', 'Sin descripción')}\n"
        
        return context

    def delete_resource(self, niche: str, resource_id: int) -> bool:
        """Elimina un recurso específico"""
        if niche not in self.resources["niches"]:
            return False

        resources = self.resources["niches"][niche]
        for i, resource in enumerate(resources):
            if resource["id"] == resource_id:
                resources.pop(i)
                self._save_resources()
                return True
        return False

    def clear_niche_resources(self, niche: str) -> bool:
        """Limpia todos los recursos de un nicho"""
        if niche in self.resources["niches"]:
            self.resources["niches"][niche] = []
            self._save_resources()
            return True
        return False 