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

INSTRUCCIONES ESPECÍFICAS:
1. Write a completely original, insightful, in-depth article.
2. Title: {row['title']}
3. Primary Keyword: {row['keyword']}
4. Secondary Keywords: {row['secondary_keywords']}

RESEARCH DATA (use as main source of data like facts,values, prices, names, opinions, and all relevant information related to the topic):
{perplexity_data}

SEO REQUIREMENTS:
- MANDATORY LENGTH: Minimum 900 words, maximum 1100 words (strictly enforced)
- Abuse exact keyword matches in strategic places:
  * Title
  * At least one H2 and one H3
  * First paragraph
  * Meta description
  * Image alt text
- Optimize for semantic search intent
- Include rich H2s and H3s (minimum 4 H2s with 2 H3s each)
- Novel and enriching content with specific examples
- Engaging, human-like style
- Web-optimized format:
  * 2-3 sentence paragraphs maximum
  * Bullet points for lists
  * Hard data and figures when possible
  * Practical examples in each section
- Add html tags to the content to make it more readable and structured
- Use html/css resources to make the content more engaging and interactive highlights or charts

MANDATORY STRUCTURE:
- Engaging introduction (120-150 words)
- 6-7 main sections short parragraphs with H2 (180-200 words each)
- 2-3 subsections H3 per H2 (60-75 words each)
- Call-to-action conclusion avoiding using the word conclusions (100-120 words)

At the bottom, include:
1. Meta description (150-160 characters)
2. Image alt text suggestion
3. SEO-friendly permalink

Follow the tone and style from @tone.txt exactly."""
            
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
    csv_file = 'PLAN SEO REAL ESTATE YUCATAN FASE 1 - Hoja 1.csv'
    
    # Leer CSV y eliminar duplicados
    df = pd.read_csv(csv_file)
    df = df.drop_duplicates(subset=['title'])
    
    # Tomar los primeros 3 artículos
    df_filtered = df.head(3).copy()
    
    logger.info(f"Probando {len(df_filtered)} artículos específicos:")
    for title in df_filtered['title']:
        logger.info(f"- {title}")
    
    for _, row in df_filtered.iterrows():
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

INSTRUCCIONES ESPECÍFICAS:
1. Write a completely original, insightful, in-depth article.
2. Title: {row['title']}
3. Primary Keyword: {row['keyword']}
4. Secondary Keywords: {row['secondary_keywords']}

RESEARCH DATA (use as main source of data like facts,values, prices, names, opinions, and all relevant information related to the topic):
{perplexity_data}

SEO REQUIREMENTS:
- MANDATORY LENGTH: Minimum 900 words, maximum 1100 words (strictly enforced)
- Abuse exact keyword matches in strategic places:
  * Title
  * At least one H2 and one H3
  * First paragraph
  * Meta description
  * Image alt text
- Optimize for semantic search intent
- Include rich H2s and H3s (minimum 4 H2s with 2 H3s each)
- Novel and enriching content with specific examples
- Engaging, human-like style
- Web-optimized format:
  * 2-3 sentence paragraphs maximum
  * Bullet points for lists
  * Hard data and figures when possible
  * Practical examples in each section
- Add html tags to the content to make it more readable and structured
- Use html/css resources to make the content more engaging and interactive highlights or charts

MANDATORY STRUCTURE:
- Engaging introduction (120-150 words)
- 6-7 main sections short parragraphs with H2 (180-200 words each)
- 2-3 subsections H3 per H2 (60-75 words each)
- Call-to-action conclusion avoiding using the word conclusions (100-120 words)

At the bottom, include:
1. Meta description (150-160 characters)
2. Image alt text suggestion
3. SEO-friendly permalink

Follow the tone and style from @tone.txt exactly."""
            
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

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 