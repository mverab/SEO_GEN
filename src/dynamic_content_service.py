import os
import json
import logging
import requests
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import markdown2

logger = logging.getLogger(__name__)

class DynamicContentService:
    def __init__(self):
        """
        Get your Jina AI API key for free: https://jina.ai/?sui=apikey
        """
        self.jina_api_key = os.getenv('JINA_API_KEY')
        if not self.jina_api_key:
            raise ValueError("JINA_API_KEY no encontrada en variables de entorno")

        self.headers = {
            "Authorization": f"Bearer {self.jina_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
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
            # 1. Buscar referencias relevantes
            references = await self._search_references(keyword, reference_urls)
            
            # 2. Extraer contenido relevante
            enriched_content = await self._extract_content(references)
            
            # 3. Formatear contenido
            formatted_content = self._format_content(content, enriched_content, format)
            
            return {
                "content": formatted_content,
                "references": references,
                "format": format
            }
            
        except Exception as e:
            logger.error(f"Error enriqueciendo contenido: {str(e)}")
            return {"error": str(e)}

    async def _search_references(
        self,
        keyword: str,
        reference_urls: Optional[List[str]] = None
    ) -> List[Dict]:
        """Busca referencias usando Jina Search API"""
        try:
            headers = {**self.headers}
            if reference_urls:
                headers["X-Site"] = ",".join(reference_urls)
            
            response = requests.post(
                "https://s.jina.ai/",
                headers=headers,
                json={
                    "q": keyword,
                    "options": "Markdown"
                }
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get("data", [])[:3]  # Limitamos a 3 referencias
            
        except Exception as e:
            logger.error(f"Error en búsqueda: {str(e)}")
            return []

    async def _extract_content(self, references: List[Dict]) -> List[Dict]:
        """Extrae contenido relevante usando Jina Reader API"""
        enriched_content = []
        
        for ref in references:
            try:
                headers = {
                    **self.headers,
                    "X-With-Links-Summary": "true",
                    "X-With-Images-Summary": "true"
                }
                
                response = requests.post(
                    "https://r.jina.ai/",
                    headers=headers,
                    json={"url": ref["url"]}
                )
                response.raise_for_status()
                
                data = response.json()
                enriched_content.append({
                    "url": ref["url"],
                    "title": data["data"]["title"],
                    "content": data["data"]["content"],
                    "images": data["data"].get("images", {}),
                    "links": data["data"].get("links", {})
                })
                
            except Exception as e:
                logger.error(f"Error extrayendo contenido: {str(e)}")
                continue
                
        return enriched_content

    def _format_content(
        self,
        original_content: str,
        enriched_content: List[Dict],
        format: str
    ) -> str:
        """Formatea el contenido según el formato requerido"""
        # Base template con estilos
        template = """
        <style>
            .seo-article {
                max-width: 800px;
                margin: 0 auto;
                font-family: Arial, sans-serif;
                line-height: 1.6;
            }
            .seo-article img {
                max-width: 100%;
                height: auto;
                margin: 20px 0;
            }
            .seo-article blockquote {
                border-left: 4px solid #ccc;
                margin: 20px 0;
                padding: 10px 20px;
                background: #f9f9f9;
            }
            .references {
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #eee;
            }
        </style>
        """

        # Contenido principal
        main_content = original_content

        # Agregar citas y referencias
        quotes = []
        references = []
        for content in enriched_content:
            if content.get("content"):
                quotes.append(f"> {content['title']}\n\n{content['content'][:300]}...")
            references.append(f"- [{content['title']}]({content['url']})")

        # Formatear según el formato solicitado
        if format == "markdown":
            return f"{main_content}\n\n## Referencias\n{''.join(quotes)}\n\n### Fuentes\n{''.join(references)}"
            
        elif format == "html":
            html_content = f"{template}<div class='seo-article'>"
            html_content += markdown2.markdown(main_content)
            html_content += "<div class='references'><h2>Referencias</h2>"
            html_content += "<blockquote>" + "</blockquote><blockquote>".join(quotes) + "</blockquote>"
            html_content += "<h3>Fuentes</h3><ul>"
            html_content += "".join([f"<li>{ref}</li>" for ref in references])
            html_content += "</ul></div></div>"
            return html_content
            
        elif format == "wordpress":
            # Formato específico para WordPress
            wp_content = f"<!-- wp:paragraph -->\n<p>{main_content}</p>\n<!-- /wp:paragraph -->\n"
            wp_content += "<!-- wp:heading -->\n<h2>Referencias</h2>\n<!-- /wp:heading -->\n"
            wp_content += "".join([f"<!-- wp:quote -->\n<blockquote>{q}</blockquote>\n<!-- /wp:quote -->\n" for q in quotes])
            return wp_content
            
        else:
            return main_content  # Formato plano por defecto 