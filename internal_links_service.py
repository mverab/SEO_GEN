from typing import List, Dict, Optional
import pandas as pd
import numpy as np
from openai import OpenAI
import logging
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

class InternalLinksService:
    def __init__(self, openai_api_key: str):
        """Inicializa el servicio de enlaces internos"""
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.links_data = None
        self.embeddings_cache = {}
        
    def load_links(self, links_file: str):
        """Carga y prepara los enlaces internos"""
        try:
            self.links_data = pd.read_csv(links_file)
            logger.info(f"Enlaces cargados: {len(self.links_data)} registros")
        except Exception as e:
            logger.error(f"Error cargando enlaces: {str(e)}")
            raise
            
    async def get_embedding(self, text: str) -> Optional[List[float]]:
        """Obtiene embedding para un texto"""
        try:
            if text in self.embeddings_cache:
                return self.embeddings_cache[text]
                
            response = await self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            
            embedding = response.data[0].embedding
            self.embeddings_cache[text] = embedding
            return embedding
            
        except Exception as e:
            logger.error(f"Error obteniendo embedding: {str(e)}")
            return None
            
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calcula similitud de coseno entre embeddings"""
        return np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )
        
    async def find_relevant_links(
        self,
        keyword: str,
        num_links: int = 3
    ) -> List[Dict[str, str]]:
        """Encuentra enlaces internos relevantes"""
        try:
            if self.links_data is None:
                logger.error("Enlaces no cargados")
                return []
                
            # Obtener embedding de la palabra clave
            keyword_embedding = await self.get_embedding(keyword)
            if not keyword_embedding:
                return []
                
            similarities = []
            for _, row in self.links_data.iterrows():
                desc_embedding = await self.get_embedding(row['Descripción'])
                if desc_embedding:
                    similarity = self.calculate_similarity(
                        keyword_embedding,
                        desc_embedding
                    )
                    similarities.append({
                        'url': row['URL'],
                        'description': row['Descripción'],
                        'similarity': similarity
                    })
                    
            # Ordenar por similitud y seleccionar los mejores
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            return similarities[:num_links]
            
        except Exception as e:
            logger.error(f"Error encontrando enlaces relevantes: {str(e)}")
            return []
            
    def format_link_for_content(self, link: Dict[str, str]) -> str:
        """Formatea enlace para inserción en contenido"""
        return f"[{link['description'].split('.')[0]}]({link['url']})" 