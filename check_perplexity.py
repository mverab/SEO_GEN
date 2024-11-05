import requests
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

def test_perplexity_connection():
    try:
        url = "https://api.perplexity.ai/chat/completions"
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {PERPLEXITY_API_KEY}"
        }
        
        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [{
                "role": "user",
                "content": "What is the capital of France? Give a short answer."
            }],
            "temperature": 0.2,
            "top_p": 0.9
        }
        
        logger.info("Realizando llamada de prueba a Perplexity API...")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            logger.info("Respuesta recibida:")
            logger.info(response.json())
            return True
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error al conectar con Perplexity: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_perplexity_connection()
    if success:
        logger.info("✅ Conexión exitosa con Perplexity API")
    else:
        logger.error("❌ Error al conectar con Perplexity API") 