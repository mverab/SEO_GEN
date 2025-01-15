import requests
from typing import List, Dict
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

class SitemapService:
    def __init__(self):
        self.urls = []
        self.content_cache = {}

    async def load_sitemap(self, sitemap_url: str) -> List[str]:
        """Carga URLs desde un sitemap XML"""
        try:
            response = requests.get(sitemap_url)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            urls = []
            for url in root.findall('.//ns:url', namespace):
                loc = url.find('ns:loc', namespace)
                if loc is not None:
                    urls.append(loc.text)
            
            self.urls = urls
            logger.info(f"Cargadas {len(urls)} URLs del sitemap")
            return urls
            
        except Exception as e:
            logger.error(f"Error cargando sitemap: {str(e)}")
            return []

    async def extract_content(self, url: str) -> Dict[str, str]:
        """Extrae contenido de una URL"""
        try:
            if url in self.content_cache:
                return self.content_cache[url]

            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer título y contenido principal
            title = soup.title.string if soup.title else ''
            
            # Buscar el contenido principal (ajustar selectores según el sitio)
            content = ''
            main_content = soup.find('main') or soup.find('article')
            if main_content:
                content = main_content.get_text(strip=True)
            
            data = {
                'url': url,
                'title': title,
                'content': content
            }
            
            self.content_cache[url] = data
            return data
            
        except Exception as e:
            logger.error(f"Error extrayendo contenido de {url}: {str(e)}")
            return {'url': url, 'title': '', 'content': ''}

    async def find_related_content(self, keyword: str, num_results: int = 3) -> List[Dict[str, str]]:
        """Encuentra contenido relacionado basado en palabras clave"""
        results = []
        
        for url in self.urls:
            content = await self.extract_content(url)
            if keyword.lower() in content['content'].lower():
                results.append(content)
                
        return sorted(
            results, 
            key=lambda x: x['content'].lower().count(keyword.lower()),
            reverse=True
        )[:num_results] 