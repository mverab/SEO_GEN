import os
from typing import Dict, Any
import aiohttp
from dotenv import load_dotenv

class PerplexityResearchService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('PERPLEXITY_API_KEY')
        self.base_url = "https://api.perplexity.ai/research"
        
    async def get_research_data(self, query: str) -> Dict[str, Any]:
        """Obtiene datos de investigación de Perplexity"""
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'query': query,
                'language': 'es'
            }
            
            async with session.post(
                self.base_url,
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Error API: {response.status}")
                    
    async def format_content(self, research_data: Dict, title: str, keyword: str) -> str:
        """Formatea el contenido según el tono y estilo requeridos"""
        # Implementar lógica de formateo aquí
        return formatted_content 