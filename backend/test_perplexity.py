import os
from openai import OpenAI
from dotenv import load_dotenv
import asyncio
import logging
import pandas as pd
from datetime import datetime

# Configuración básica
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cliente de Perplexity
perplexity_client = OpenAI(
    api_key=os.getenv('PERPLEXITY_API_KEY'),
    base_url="https://api.perplexity.ai"
)

async def test_perplexity_response(query: str, title: str) -> dict:
    """Prueba simple de respuesta de Perplexity"""
    try:
        response = perplexity_client.chat.completions.create(
            model="llama-3.1-sonar-small-128k-online",
            messages=[{"role": "user", "content": query}],
            temperature=0.2,
            top_p=0.9,
            frequency_penalty=1
        )
        
        content = response.choices[0].message.content
        
        # Crear directorio si no existe
        os.makedirs('perplexity_data', exist_ok=True)
        
        # Guardar respuesta con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"perplexity_data/{title.lower().replace(' ', '_')}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Query: {query}\n\n")
            f.write(f"Response:\n{content}")
        
        quality_check = {
            "longitud": len(content.split()) > 100,
            "datos_especificos": any(char.isdigit() for char in content),
            "contenido": content,
            "palabras": len(content.split()),
            "archivo_guardado": filename
        }
        
        logger.info(f"Respuesta guardada en: {filename}")
        return quality_check
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    df = pd.read_csv('PLAN SEO REAL ESTATE YUCATAN FASE 1 - Hoja 1.csv')
    print("\nRevisando contenido del CSV:")
    print(f"Columnas disponibles: {df.columns.tolist()}")
    print("\nLínea 24 específicamente:")
    print(f"Título: {df['title'][23]}")
    print(f"Query: {df['PerplexityQuery'][23]}") 