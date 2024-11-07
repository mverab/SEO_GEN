import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from anthropic import Anthropic
import pandas as pd
from google_docs_service import GoogleDocsService
from link_service import InternalLinkService

# Configuración básica
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar clientes
anthropic_client = Anthropic()
perplexity_client = OpenAI(
    api_key=os.getenv('PERPLEXITY_API_KEY'),
    base_url="https://api.perplexity.ai"
)
google_docs = GoogleDocsService()
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
link_service = InternalLinkService(openai_client)

async def get_perplexity_data(query: str) -> str:
    """Obtener datos de Perplexity usando el cliente ya probado"""
    try:
        # Asegurar que la query sea un string válido y esté formateada correctamente
        formatted_query = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "user",
                    "content": str(query).strip()  # Asegurar que sea string y eliminar espacios extra
                }
            ]
        }
        
        response = perplexity_client.chat.completions.create(**formatted_query)
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error Perplexity: {str(e)}")
        raise

async def test_articles(csv_file: str, num_articles: int = 2):
    df = pd.read_csv(csv_file).head(num_articles)
    logger.info(f"Probando {len(df)} artículos de {csv_file}")
    
    for _, row in df.iterrows():
        try:
            perplexity_data = await get_perplexity_data(row['PerplexityQuery'])
            logger.info(f"✓ Datos obtenidos para: {row['title']}")
            
            # Prompt mejorado con SEO GUIDELINES
            prompt = f"""You are a News/SEO writer/developer & research expert that speaks and writes in fluent native level spanish and english. 
You automatically detect the language of the title and keywords to write the entire article in that same language.

LANGUAGE DETECTION:
- Title language: {row['title']}
- Main keyword language: {row['keyword']}
Therefore, write this article in: {'Spanish' if any(c in row['title'].lower() for c in ['á','é','í','ó','ú','ñ']) else 'English'}

You are the best professional expert on the market. You have the most accurate and detailed keywords about the real estate market and you are extremely informed about all developments in this niche.

You write with a 40% spartan tone, casual, never too technical. You are specialized in writing for a young male audience (20-40 years old) with 6th grade reading level.

Your style delivers extended paragraphs with extremely detailed information that are never boring, being casual, relatable and practical. You are famous for your slightly witty, yet charming tone.

INSTRUCCIONES ESPECÍFICAS:
1. Escribe un artículo completamente original, profundo e interesante.
2. Título: {row['title']}
3. Keyword principal: {row['keyword']}
4. Keywords secundarias: {row['secondary_keywords']}

DATOS DE INVESTIGACIÓN (usar solo para datos históricos y periodísticos):
{perplexity_data}

REQUISITOS SEO:
- Longitud OBLIGATORIA: Mínimo 800 palabras, máximo 1100 palabras
- Abusa de la coincidencia exacta de keywords con frases de búsqueda
- Optimiza para intención de búsqueda semántica tipo JSON-LD
- Incluir H2s y H3s enriquecidos (mínimo 4 H2 y 2 H3 por H2)
- Contenido novedoso y enriquecedor con ejemplos específicos
- Estilo cercano y humano
- Formato web optimizado:
  * Párrafos de 2-3 oraciones máximo
  * Bullets para listas
  * Datos duros y cifras cuando sea posible
  * Ejemplos prácticos en cada sección

ESTRUCTURA OBLIGATORIA:
- Introducción cautivadora (100-150 palabras)
- 4-5 secciones principales con H2 (150-200 palabras cada una)
- 2-3 subsecciones H3 por cada H2 (50-75 palabras cada una)
- Conclusión con llamada a la acción (100 palabras)

El contenido debe ser extremadamente detallado y útil para el lector."""
            
            completion = anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = completion.content[0].text
            
            # Guardar para comparación
            output_dir = f"output/test_{os.path.splitext(os.path.basename(csv_file))[0]}"
            os.makedirs(output_dir, exist_ok=True)
            
            with open(f"{output_dir}/{row['title'].replace(' ', '_')}.txt", 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✓ Artículo completado: {row['title']}")
            
        except Exception as e:
            logger.error(f"Error procesando {row['title']}: {str(e)}")

async def main():
    # Probar solo con el nuevo CSV y limitar a 3 artículos
    await test_articles('PLAN SEO REAL ESTATE YUCATAN FASE 1 - Hoja 1.csv', num_articles=3)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 