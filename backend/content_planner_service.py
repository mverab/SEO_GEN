import os
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from typing import List, Dict
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class ContentPlanService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def generate_content_plan(self, keywords: List[str]) -> Dict:
        """
        Genera un plan de contenido basado en las keywords proporcionadas
        """
        try:
            # Leer el prompt template
            with open('src/seoplanprompt.md', 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            
            # Construir el prompt
            prompt = f"""Aquí está la lista de palabras clave para generar el plan de contenido:

{chr(10).join(f'- {keyword}' for keyword in keywords)}

{prompt_template}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Convertir la respuesta a formato estructurado
            articles = self._parse_content_to_articles(content)
            
            # Crear DataFrame y exportar a CSV
            df = pd.DataFrame(articles)
            output_path = f'plans/content_plan_{keywords[0].replace(" ", "_")}.csv'
            os.makedirs('plans', exist_ok=True)
            df.to_csv(output_path, index=False)
            
            return {
                "plan": articles,
                "raw_content": content,
                "file_path": output_path
            }
            
        except Exception as e:
            logger.error(f"Error generando plan de contenido: {str(e)}")
            raise

    def _parse_content_to_articles(self, content: str) -> List[Dict]:
        """
        Parsea el contenido de la respuesta a una lista de artículos estructurados
        """
        try:
            # Por ahora retornamos el contenido sin procesar
            # El formato real vendrá de GPT-4 siguiendo el template de seoplanprompt.md
            return [{
                "title": "Título del artículo",
                "keyword": "keyword principal",
                "secondary_keywords": "keywords secundarias",
                "search_intent": "intención de búsqueda"
            }]
        except Exception as e:
            logger.error(f"Error parseando contenido: {str(e)}")
            return []

    async def export_to_csv(self, plan_data: List[Dict], filename: str):
        """
        Exporta el plan a CSV
        """
        try:
            df = pd.DataFrame(plan_data)
            df.to_csv(f'plans/{filename}.csv', index=False)
            return True
        except Exception as e:
            logger.error(f"Error exportando a CSV: {str(e)}")
            return False