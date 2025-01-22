import pandas as pd
import numpy as np
from openai import OpenAI
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class InternalLinkService:
    def __init__(self, openai_client: OpenAI):
        self.openai_client = openai_client

    def get_embedding(self, text: str) -> Optional[List[float]]:
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error al obtener embedding: {str(e)}")
            return None

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Error al obtener embeddings: {str(e)}")
            return []

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.dot(a, b.T) / (np.linalg.norm(a, axis=1, keepdims=True) * np.linalg.norm(b, axis=1))

    def get_relevant_links(self, keyword: str, links_file: str, num_links: int = 3) -> List[Dict]:
        try:
            if not links_file:
                logger.info("No se proporcionó archivo de enlaces internos")
                return []

            links_df = pd.read_csv(links_file)
            
            if not {'URL', 'Descripción'}.issubset(links_df.columns):
                logger.error(f"El archivo {links_file} debe contener las columnas 'URL' y 'Descripción'")
                return []

            descriptions = links_df['Descripción'].fillna('').tolist()
            descriptions_embeddings = self.get_embeddings(descriptions)
            if not descriptions_embeddings:
                return []
                
            keyword_embedding = self.get_embedding(keyword)
            if not keyword_embedding:
                return []

            similarities = self.cosine_similarity(
                np.array(descriptions_embeddings), 
                np.array([keyword_embedding])
            )
            links_df['Similitud'] = similarities.flatten()

            relevant_links = links_df.sort_values(by='Similitud', ascending=False).head(num_links)
            return relevant_links[['URL', 'Descripción']].to_dict('records')

        except Exception as e:
            logger.error(f"Error al procesar {links_file}: {str(e)}")
            return [] 