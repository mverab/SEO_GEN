import os
import logging
import aiohttp
import json
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class DynamicContentService:
    def __init__(self):
        # Get your Jina AI API key for free: https://jina.ai/?sui=apikey
        self.api_key = os.getenv('JINA_API_KEY')
        if not self.api_key:
            raise ValueError("JINA_API_KEY no encontrada en variables de entorno")
            
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        self.format_templates = {
            "markdown": {
                "prefix": "",
                "suffix": ""
            },
            "html": {
                "prefix": "<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>",
                "suffix": "</body></html>"
            },
            "wordpress": {
                "prefix": "<!-- wp:paragraph -->",
                "suffix": "<!-- /wp:paragraph -->"
            }
        }

    async def enrich_content(
        self,
        keyword: str,
        content: str,
        format: str = "markdown",
        reference_urls: Optional[List[str]] = None
    ) -> Dict:
        """Enriquece contenido con referencias y formato"""
        try:
            # 1. Obtener referencias si se proporcionan URLs
            references = []
            if reference_urls:
                references = await self._get_references(reference_urls)

            # 2. Enriquecer contenido con referencias
            enriched_content = await self._add_references(content, references)

            # 3. Aplicar formato
            formatted_content = self._apply_format(enriched_content, format)

            return {
                "keyword": keyword,
                "content": formatted_content,
                "format": format,
                "references": references
            }

        except Exception as e:
            logger.error(f"Error enriqueciendo contenido: {str(e)}")
            return {
                "error": str(e),
                "keyword": keyword,
                "content": content
            }

    async def _get_references(self, urls: List[str]) -> List[Dict]:
        """Obtiene referencias usando Jina Reader API"""
        references = []
        
        async with aiohttp.ClientSession() as session:
            for url in urls[:3]:  # Limitado a 3 referencias
                try:
                    headers = {
                        **self.headers,
                        "X-With-Links-Summary": "true",
                        "X-With-Images-Summary": "true"
                    }
                    
                    async with session.post(
                        'https://r.jina.ai/',
                        headers=headers,
                        json={"url": url}
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            if "data" in data:
                                references.append({
                                    "url": url,
                                    "title": data["data"].get("title", ""),
                                    "content": data["data"].get("content", ""),
                                    "links": data["data"].get("links", {}),
                                    "images": data["data"].get("images", {})
                                })
                
                except Exception as e:
                    logger.error(f"Error obteniendo referencia {url}: {str(e)}")
                    continue
                    
        return references

    async def _add_references(self, content: str, references: List[Dict]) -> str:
        """Agrega referencias al contenido"""
        if not references:
            return content
            
        enriched = content + "\n\n## Referencias\n"
        for i, ref in enumerate(references, 1):
            enriched += f"\n{i}. [{ref['title']}]({ref['url']})"
            
        return enriched

    def _apply_format(self, content: str, format: str) -> str:
        """Aplica formato al contenido"""
        template = self.format_templates.get(format, self.format_templates["markdown"])
        
        if format == "html":
            # Convertir Markdown a HTML básico
            content = content.replace("\n\n", "</p><p>")
            content = f"<p>{content}</p>"
            content = content.replace("## ", "<h2>").replace("\n", "</h2>")
            
        elif format == "wordpress":
            # Formato WordPress Gutenberg
            paragraphs = content.split("\n\n")
            formatted = []
            for p in paragraphs:
                if p.startswith("## "):
                    formatted.append(f"<!-- wp:heading --><h2>{p[3:]}</h2><!-- /wp:heading -->")
                else:
                    formatted.append(f"<!-- wp:paragraph --><p>{p}</p><!-- /wp:paragraph -->")
            content = "\n".join(formatted)
            
        return f"{template['prefix']}{content}{template['suffix']}" 