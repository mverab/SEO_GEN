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
        response = perplexity_client.chat.completions.create(
            model="llama-3.1-sonar-small-128k-online",
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error Perplexity: {str(e)}")
        raise

async def main(links_file: str = None):
    df = pd.read_csv('data/input/test_articles.csv')
    logger.info(f"Procesando {len(df)} artículos...")
    
    for _, row in df.iterrows():
        try:
            # 1. Obtener datos de Perplexity
            perplexity_data = await get_perplexity_data(row['PerplexityQuery'])
            logger.info(f"✓ Datos obtenidos para: {row['title']}")
            
            # 2. Obtener enlaces relevantes (opcional)
            relevant_links = []
            if links_file:
                relevant_links = link_service.get_relevant_links(row['keyword'], links_file)
                if relevant_links:
                    logger.info(f"✓ Enlaces relevantes encontrados: {len(relevant_links)}")
            
            # 3. Generar contenido con Anthropic
            prompt = f"""You are a News/SEO writer/developer & research expert that speaks and writes in fluent native level spanish. You develop the best blog post & web article pieces ranking on all search engines.

You write with a 40% spartan tone, casual, never too technical. You are specialized in writing for a young male audience (20-40 years old) with 6th grade reading level.

Your style delivers extended paragraphs with extremely detailed information that are never boring, being casual, relatable and practical. You are famous for your slightly witty, yet charming tone.

INSTRUCCIONES ESPECÍFICAS:
1. Escribe un artículo completamente original, profundo, interesante y de alto valor.
2. Título: {row['title']}
3. Keyword principal: {row['keyword']}
4. Keywords secundarias: {row['secondary_keywords']}

DATOS DE INVESTIGACIÓN:
{perplexity_data}

REQUISITOS SEO:
- Longitud: 850-1200 palabras
- Usar coincidencia exacta de keywords donde sea natural
- Optimizar para intención de búsqueda semántica
- Incluir H2s y H3s enriquecidos
- Contenido novedoso y enriquecedor
- Estilo cercano y humano
- Formato web optimizado (párrafos cortos, bullets cuando sea apropiado)

ESTRUCTURA:
- Introducción cautivadora
- Al menos 4 secciones principales con H2
- Subsecciones relevantes con H3
- Conclusión con llamada a la acción
"""
            
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
