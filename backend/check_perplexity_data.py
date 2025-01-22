import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
import json
import pandas as pd

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

perplexity_client = OpenAI(
    api_key=os.getenv('PERPLEXITY_API_KEY'),
    base_url="https://api.perplexity.ai"
)

def test_perplexity_query(query: str):
    try:
        response = perplexity_client.chat.completions.create(
            model="llama-3.1-sonar-small-128k-online",
            messages=[{"role": "user", "content": query}],
            temperature=0.2,  # Menor temperatura para respuestas más precisas
            top_p=0.9,       # Núcleo de muestreo para mejor coherencia
            frequency_penalty=1  # Reduce repeticiones
        )
        
        # Guardar respuesta completa
        os.makedirs('logs/perplexity_tests', exist_ok=True)
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        
        with open(f'logs/perplexity_tests/test_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump({
                'query': query,
                'response': response.choices[0].message.content,
                'model': response.model,
                'timestamp': timestamp
            }, f, indent=2)
            
        logger.info(f"Test guardado en logs/perplexity_tests/test_{timestamp}.json")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    test_query = "What are the main advantages and current trends of real estate investment in Yucatan, Mexico?"
    test_perplexity_query(test_query)