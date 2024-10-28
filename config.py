import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde el archivo .env

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_DOC_ID = os.getenv("GOOGLE_DOC_ID")
FOLDER_ID = os.getenv("FOLDER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

api_key = os.getenv('OPENAI_API_KEY')
