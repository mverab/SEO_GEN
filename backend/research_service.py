from typing import Dict, List, Optional
import asyncio
from datetime import datetime
import logging
import anthropic
from config import LOG_CONFIG, BATCH_CONFIG, SITE_CONFIG
import pandas as pd
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from internal_links_service import InternalLinksService
import os

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

class RateLimiter:
    def __init__(self, calls_per_minute: int = 20):  # Perplexity permite 20 llamadas/min
        self.calls_per_minute = calls_per_minute
        self.calls = []
        self.lock = asyncio.Lock()
        
    async def acquire(self):
        async with self.lock:
            now = datetime.now()
            # Limpiar llamadas antiguas
            self.calls = [call_time for call_time in self.calls 
                         if (now - call_time).seconds < 60]
            
            if len(self.calls) >= self.calls_per_minute:
                # Esperar hasta que podamos hacer otra llamada
                wait_time = 60 - (now - self.calls[0]).seconds
                if wait_time > 0:
                    logger.info(f"Rate limit alcanzado. Esperando {wait_time} segundos")
                    await asyncio.sleep(wait_time)
                self.calls = self.calls[1:]
            
            self.calls.append(now)

class PerplexityResearchService:
    def __init__(self, perplexity_api_key: str, anthropic_api_key: str, openai_api_key: str):
        """Inicializa el servicio de investigación"""
        self.perplexity_client = OpenAI(
            api_key=perplexity_api_key,
            base_url="https://api.perplexity.ai"
        )
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.internal_links = InternalLinksService(openai_api_key)
        self.rate_limiter = RateLimiter()
        self.is_new_site = SITE_CONFIG["IS_NEW_SITE"]
        
    async def get_research_data(self, article_data: Dict) -> Optional[Dict]:
        try:
            # Si es sitio nuevo, omitir búsqueda de enlaces internos
            if self.is_new_site:
                logger.info("Sitio nuevo detectado - omitiendo enlaces internos")
                return await self._get_research_only(article_data)
            else:
                return await self._get_research_with_links(article_data)
                
        except Exception as e:
            logger.error(f"Error en investigación: {str(e)}")
            return None

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
        tone_file: str,
        links_file: str = "links_appsclavitud.csv"
    ) -> Optional[Dict]:
        """Obtiene datos de investigación y genera contenido con enlaces internos"""
        try:
            # Cargar enlaces internos
            self.internal_links.load_links(links_file)
            
            # Obtener enlaces relevantes
            relevant_links = await self.internal_links.find_relevant_links(
                article_data["keyword"]
            )
            
            # Obtener investigación con Perplexity
            research_data = await self._call_perplexity_api(
                self._build_perplexity_prompt(
                    article_data["keyword"],
                    article_data["secondary_keywords"]
                )
            )

            if not research_data:
                logger.error(f"No se obtuvo respuesta de Perplexity para artículo {article_data['id']}")
                return None

            logger.info(f"Investigación completada para artículo {article_data['id']}")
            
            # Formatear enlaces para el prompt
            formatted_links = [
                self.internal_links.format_link_for_content(link)
                for link in relevant_links
            ]
            
            # Generar contenido con Claude incluyendo enlaces
            content_response = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": self._build_content_prompt(
                        article_data,
                        research_data,
                        read_file('tone.txt'),
                        formatted_links
                    )
                }]
            )

            return {
                "id": article_data["id"],
                "research_data": research_data,
                "content": content_response.content[0].text,
                "internal_links": formatted_links,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error en investigación para artículo {article_data['id']}: {str(e)}")
            return None

    def _build_content_prompt(
        self,
        article_data: Dict,
        research_data: str,
        tone_file: str,
        internal_links: List[str]
    ) -> str:
        """Construye el prompt incluyendo enlaces internos"""
        links_section = "\n".join([
            f"- {link}" for link in internal_links
        ])
        
        return f"""Eres un escritor SEO experto que escribe exactamente con este tono y estilo:

{tone_file}

Genera contenido en español siguiendo estrictamente estas reglas:
1. Título: {article_data['title']}
2. Palabra clave principal: {article_data['keyword']}
3. Palabras clave secundarias: {', '.join(article_data['secondary_keywords'])}
4. Datos de investigación: {research_data}

Enlaces internos a incluir naturalmente en el contenido:
{links_section}

El contenido debe:
- Tener 600 palabras mínimo
- Mantener el tono especificado
- Estar optimizado para SEO
- Incluir datos verificables de la investigación
- Ser original y atractivo
- Estar dirigido a hombres de 25-35 años
- Tener un tono casual y 30% espartano
- Incluir los enlaces internos de forma natural y relevante

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

    @retry(
        stop=stop_after_attempt(BATCH_CONFIG["MAX_RETRIES"]),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _call_perplexity_api(self, prompt: str) -> Optional[str]:
        """Realiza llamada a la API de Perplexity"""
        try:
            response = self.perplexity_client.chat.completions.create(
                model="llama-3.1-sonar-small-128k-online",  # Modelo correcto
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                temperature=0.7,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error en llamada a Perplexity API: {str(e)}")
            return None

    async def validate_api_access(self) -> bool:
        """Valida el acceso a las APIs"""
        try:
            test_response = await self._call_perplexity_api("Test")
            return test_response is not None
        except Exception as e:
            logger.error(f"Error validando APIs: {str(e)}")
            return False

    async def _generate_content(self, article_data: Dict, research_data: str) -> str:
        """Genera contenido usando Claude"""
        try:
            # Actualizar la llamada a la API de Claude
            message = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": self._build_content_prompt(article_data, research_data)
                }]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Error generando contenido: {str(e)}")
            raise

def read_file(filename: str) -> str:
    """Lee un archivo y retorna su contenido"""
    try:
        with open(os.path.join(os.path.dirname(__file__), filename), "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"El archivo {filename} no existe.")
        raise