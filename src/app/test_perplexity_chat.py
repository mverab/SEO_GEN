import os
from openai import OpenAI
from dotenv import load_dotenv
import asyncio
import logging
import pandas as pd

# Configuración básica
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cliente de Perplexity (igual que en main.py)
perplexity_client = OpenAI(
    api_key=os.getenv('PERPLEXITY_API_KEY'),
    base_url="https://api.perplexity.ai"
)

async def get_perplexity_data(query: str) -> str:
    """Función exacta de main.py"""
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

if __name__ == "__main__":
    print("\nTest de Perplexity (versión main.py)")
    print("Escribe 'salir' para terminar")
    print("-" * 50)
    
    while True:
        query = input("\nQuery: ")
        if query.lower() == 'salir':
            break
            
        print("\nObteniendo datos de Perplexity...")
        perplexity_data = asyncio.run(get_perplexity_data(query))
        
        print("\nDatos que recibiría Claude:")
        print("-" * 50)
        print(perplexity_data)
        print("-" * 50) 