import anthropic
from config import ANTHROPIC_API_KEY

# Inicializar cliente Anthropic
anthropic_client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

# Probar Anthropic
try:
    response = anthropic_client.messages.create(
        model="claude-3-sonnet-20240229",
        messages=[{
            "role": "user",
            "content": "Di hola mundo"
        }],
        max_tokens=50
    )
    print("Anthropic API está funcionando correctamente.")
    print("Respuesta:", response.content[0].text)
except Exception as e:
    print(f"Error con Anthropic API: {e}")
    print(f"API Key utilizada: {ANTHROPIC_API_KEY[:10]}...")  # Muestra solo los primeros 10 caracteres 