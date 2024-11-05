from typing import Dict, List, Optional
import asyncio
from datetime import datetime
import logging
import anthropic
from config import LOG_CONFIG, BATCH_CONFIG
import pandas as pd
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOG_CONFIG["LEVEL"]),
    format=LOG_CONFIG["FORMAT"],
    handlers=[
        logging.FileHandler(LOG_CONFIG["FILE"]),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class PerplexityResearchService:
    def __init__(self, perplexity_api_key: str, anthropic_api_key: str):
        """Inicializa el servicio de investigación"""
        # Inicializar cliente de Perplexity usando OpenAI client
        self.perplexity_client = OpenAI(
            api_key=perplexity_api_key,
            base_url="https://api.perplexity.ai"
        )
        self.anthropic_client = anthropic.Client(api_key=anthropic_api_key)

    def _build_perplexity_prompt(self, keyword: str, secondary_keywords: List[str]) -> str:
        """
        Construye el prompt para Perplexity siguiendo el template establecido
        """
        question = f"Provide comprehensive information about {keyword} considering these related topics: {', '.join(secondary_keywords)}"
        
        return f"""Please search all relevant sources to give the most accurate, valuable and concrete answer to the following question: 
{question}

Additional instructions:  
Use english written sources please
Order your answer in the most SEO friendly way so it can be used to write a SEO article for a website.
Include all semantic context possible, however, limit yourself to information relevant to answer the question inside a news outlet/blog SEO optimized post perspective.
Your response will be used as a main data source fed to a writing LLM to develop a high quality info about this subject.
Please, at the end give any relevant info about your workflow or frame of reference you believe is relevant in order to get the best output possible.
Avoid leaving blank spaces between lines in your response please
Please give your response in fluid spanish, 40% spartan tone, casual."""

    @retry(
        stop=stop_after_attempt(BATCH_CONFIG["MAX_RETRIES"]),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def get_research_data(
        self, 
        article_data: Dict,
        tone_file: str
    ) -> Optional[Dict]:
        """
        Obtiene datos de investigación usando Perplexity y genera contenido con Claude
        """
        try:
            # Investigación con Perplexity
            prompt = self._build_perplexity_prompt(
                article_data["keyword"],
                article_data["secondary_keywords"]
            )
            research_data = await self._call_perplexity_api(prompt)

            if not research_data:
                logger.error(f"No se obtuvo respuesta de Perplexity para artículo {article_data['id']}")
                return None

            logger.info(f"Investigación completada para artículo {article_data['id']}")

            # Generar contenido con Claude usando los datos de Perplexity
            content_response = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": self._build_content_prompt(
                        article_data,
                        research_data,
                        tone_file
                    )
                }]
            )

            return {
                "id": article_data["id"],
                "research_data": research_data,
                "content": content_response.content[0].text,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error en investigación para artículo {article_data['id']}: {str(e)}")
            return None

    def _build_content_prompt(
        self,
        article_data: Dict,
        research_data: str,
        tone_file: str
    ) -> str:
        """
        Construye el prompt para Claude manteniendo el tono y estilo existente
        """
        return f"""Eres un escritor SEO experto que escribe exactamente con este tono y estilo:

{tone_file}

Genera contenido en español siguiendo estrictamente estas reglas:
1. Título: {article_data['title']}
2. Palabra clave principal: {article_data['keyword']}
3. Palabras clave secundarias: {', '.join(article_data['secondary_keywords'])}
4. Datos de investigación: {research_data}

El contenido debe:
- Tener 600 palabras mínimo
- Mantener el tono especificado
- Estar optimizado para SEO
- Incluir datos verificables de la investigación
- Ser original y atractivo
- Estar dirigido a hombres de 25-35 años
- Tener un tono casual y 30% espartano

Estructura el contenido de forma natural y atractiva, usando los datos de investigación como base."""

    async def process_batch_from_csv(self, csv_file: str) -> List[Dict]:
        """
        Procesa un lote de artículos desde un CSV
        """
        try:
            df = pd.read_csv(csv_file)
            results = []
            
            for _, row in df.iterrows():
                article_data = {
                    "id": f"{datetime.now().strftime('%Y%m%d')}_{len(results)+1}",
                    "title": row['Título'],
                    "keyword": row['Palabra Clave Principal'],
                    "secondary_keywords": row['Palabras Clave Secundarias'].split(','),
                }
                
                result = await self.get_research_data(article_data, read_file('tone.txt'))
                if result:
                    results.append(result)
                    
            return results
            
        except Exception as e:
            logger.error(f"Error procesando CSV {csv_file}: {str(e)}")
            return []

    async def validate_api_access(self) -> bool:
        """Valida el acceso a las APIs"""
        try:
            # Probar Perplexity
            test_response = await self.perplexity_client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            return bool(test_response)
        except Exception as e:
            logger.error(f"Error validando APIs: {str(e)}")
            return False 