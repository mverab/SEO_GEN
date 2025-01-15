from typing import Dict, List, Optional
import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class ResourceService:
    def __init__(self):
        self.resources_dir = "resources"
        self._ensure_resources_dir()
        self.resources = self._load_resources()

    def _ensure_resources_dir(self):
        """Asegura que exista el directorio de recursos"""
        if not os.path.exists(self.resources_dir):
            os.makedirs(self.resources_dir)

    def _load_resources(self) -> Dict:
        """Carga recursos existentes"""
        resources_file = os.path.join(self.resources_dir, "resources.json")
        if os.path.exists(resources_file):
            with open(resources_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_resources(self):
        """Guarda recursos en disco"""
        resources_file = os.path.join(self.resources_dir, "resources.json")
        with open(resources_file, 'w', encoding='utf-8') as f:
            json.dump(self.resources, f, ensure_ascii=False, indent=2)

    def add_niche_resource(
        self,
        niche: str,
        content: str,
        resource_type: str = "text",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Agrega un recurso a un nicho"""
        if niche not in self.resources:
            self.resources[niche] = []

        resource = {
            "id": len(self.resources[niche]) + 1,
            "type": resource_type,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat()
        }

        self.resources[niche].append(resource)
        self._save_resources()
        return resource

    def get_niche_resources(self, niche: str) -> List[Dict]:
        """Obtiene todos los recursos de un nicho"""
        return self.resources.get(niche, [])

    def get_resource_context(self, keyword: str) -> str:
        """Obtiene contexto relevante de recursos para una keyword"""
        context = []
        
        # Buscar en todos los nichos
        for niche, resources in self.resources.items():
            if keyword.lower() in niche.lower():
                for resource in resources:
                    if resource["type"] == "text":
                        context.append(resource["content"])
        
        return "\n\n".join(context) if context else ""

    def delete_resource(self, niche: str, resource_id: int) -> bool:
        """Elimina un recurso específico"""
        if niche not in self.resources:
            return False
            
        for i, resource in enumerate(self.resources[niche]):
            if resource["id"] == resource_id:
                self.resources[niche].pop(i)
                self._save_resources()
                return True
                
        return False

    def update_resource(
        self,
        niche: str,
        resource_id: int,
        content: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Optional[Dict]:
        """Actualiza un recurso existente"""
        if niche not in self.resources:
            return None
            
        for resource in self.resources[niche]:
            if resource["id"] == resource_id:
                if content:
                    resource["content"] = content
                if metadata:
                    resource["metadata"].update(metadata)
                self._save_resources()
                return resource
                
        return None 