import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from anthropic import Anthropic
import pandas as pd
from google_docs_service import GoogleDocsService

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

async def get_perplexity_data(query: str) -> str:
    """Obtener datos de Perplexity usando el cliente ya probado"""
    try:
        response = perplexity_client.chat.completions.create(
            model="llama-3.1-sonar-small-128k-online",
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error Perplexity: {str(e)}")
        raise

async def main():
    df = pd.read_csv('data/input/test_articles.csv')
    logger.info(f"Procesando {len(df)} artículos...")
    
    for _, row in df.iterrows():
        try:
            perplexity_data = await get_perplexity_data(row['PerplexityQuery'])
            logger.info(f"✓ Datos obtenidos para: {row['title']}")
            
            completion = anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": f"""
                    Título: {row['title']}
                    Keyword: {row['keyword']}
                    Keywords secundarias: {row['secondary_keywords']}
                    
                    Información de investigación:
                    {perplexity_data}
                    
                    Genera un artículo SEO optimizado en español.
                    """
                }]
            )
            
            content = completion.content[0].text
            
            # Guardar en Google Docs
            doc_id = await google_docs.save_content(
                content=content,
                title=row['title'],
                article_id=str(pd.Timestamp.now().strftime('%Y%m%d_%H%M%S'))
            )
            
            if doc_id:
                logger.info(f"✓ Artículo guardado en Google Docs: {doc_id}")
            
            # Mantener backup local
            os.makedirs('output', exist_ok=True)
            with open(f"output/{row['title'].replace(' ', '_')}.txt", 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✓ Artículo completado: {row['title']}")
            
        except Exception as e:
            logger.error(f"Error procesando {row['title']}: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
