import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

def test_perplexity_connection():
    try:
        client = OpenAI(
            api_key=PERPLEXITY_API_KEY,
            base_url="https://api.perplexity.ai"
        )
        
        response = client.chat.completions.create(
            model="llama-3.1-sonar-small-128k-online",
            messages=[{
                "role": "user",
                "content": "Test connection"
            }],
            stream=False
        )
        
        logger.info("Respuesta recibida:")
        logger.info(response.choices[0].message.content)
        return True
        
    except Exception as e:
        logger.error(f"Error al conectar con Perplexity: {str(e)}")
        return False

if __name__ == "__main__":
    if test_perplexity_connection():
        print("✅ Conexión exitosa con Perplexity API")
    else:
        print("❌ Error al conectar con Perplexity API")