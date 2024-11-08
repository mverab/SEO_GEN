import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from anthropic import Anthropic
import pandas as pd
from google_docs_service import GoogleDocsService
from link_service import InternalLinkService
import asyncio
from datetime import datetime

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

class RateLimiter:
    def __init__(self, calls_per_minute: int = 20):
        self.calls_per_minute = calls_per_minute
        self.calls = []
        self.lock = asyncio.Lock()
        
    async def acquire(self):
        async with self.lock:
            now = datetime.now()
            self.calls = [call_time for call_time in self.calls 
                         if (now - call_time).seconds < 60]
            
            if len(self.calls) >= self.calls_per_minute:
                wait_time = 60 - (now - self.calls[0]).seconds
                if wait_time > 0:
                    logger.info(f"Rate limit alcanzado. Esperando {wait_time} segundos")
                    await asyncio.sleep(wait_time)
                self.calls = self.calls[1:]
            
            self.calls.append(now)

async def get_perplexity_data(query: str) -> str:
    """Obtener datos de Perplexity usando el cliente ya probado"""
    try:
        response = perplexity_client.chat.completions.create(
            model="llama-3.1-sonar-small-128k-online",
            messages=[{"role": "user", "content": query}],
            temperature=0.2,
            top_p=0.9,
            frequency_penalty=1
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error Perplexity: {str(e)}")
        raise

async def main(links_file: str = None):
    rate_limiter = RateLimiter(calls_per_minute=20)
    
    # Usar la misma estructura que test_comparison.py
    df = pd.read_csv('PLAN SEO REAL ESTATE YUCATAN FASE 1 - Hoja 1.csv')
    df = df.drop_duplicates(subset=['title'])
    df_filtered = df.iloc[6:].copy()
    
    logger.info(f"Procesando {len(df_filtered)} artículos...")
    
    for _, row in df_filtered.iterrows():
        try:
            await rate_limiter.acquire()
            # Asegurar que la query sea un string válido
            query = str(row['PerplexityQuery']).strip()
            perplexity_data = await get_perplexity_data(query)
            logger.info(f"✓ Datos obtenidos para: {row['title']}")
            
            # 2. Obtener enlaces relevantes (opcional)
            relevant_links = []
            if links_file:
                relevant_links = link_service.get_relevant_links(row['keyword'], links_file)
                if relevant_links:
                    logger.info(f"✓ Enlaces relevantes encontrados: {len(relevant_links)}")
            
            # 3. Generar contenido con Anthropic
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
3. SEO-friendly permalink"""
            
            if relevant_links:
                prompt += "\nENLACES A INTEGRAR ORGÁNICAMENTE:\n"
                for link in relevant_links:
                    prompt += f"- [{link['Descripción']}]({link['URL']})\n"
            
            completion = anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = completion.content[0].text
            
            # 4. Guardar en Google Docs
            doc_id = await google_docs.save_content(
                content=content,
                title=row['title'],
                article_id=str(pd.Timestamp.now().strftime('%Y%m%d_%H%M%S'))
            )
            
            if doc_id:
                logger.info(f"✓ Artículo guardado en Google Docs: {doc_id}")
            
            # 5. Mantener backup local
            os.makedirs('output', exist_ok=True)
            with open(f"output/{row['title'].replace(' ', '_')}.txt", 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✓ Artículo completado: {row['title']}")
            
        except Exception as e:
            logger.error(f"Error procesando {row['title']}: {str(e)}")

if __name__ == "__main__":
    import asyncio
    # Para probar sin enlaces:
    # asyncio.run(main())
    
    # Para probar con enlaces:
    # asyncio.run(main("links_appsclavitud.csv"))
    
    # Por ahora, mantener la versión sin enlaces para las pruebas
    asyncio.run(main())
