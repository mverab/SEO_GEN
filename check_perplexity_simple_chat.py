import requests
import os
from dotenv import load_dotenv
import logging
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel

# Configuración de logging y console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
console = Console()

# Cargar variables de entorno
load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

class SimpleChat:
    def __init__(self):
        self.url = "https://api.perplexity.ai/chat/completions"
        self.model = "llama-3.1-sonar-small-128k-online"  # Modelo a utilizar
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {PERPLEXITY_API_KEY}"
        }
        self.conversation_history: List[Dict[str, str]] = []
        self.total_tokens = 0

    def send_message(self, message: str, temperature: float = 0.2) -> Dict[str, Any]:
        """Envía un mensaje y retorna la respuesta con métricas"""
        try:
            # Preparar el payload
            payload = {
                "model": self.model,
                "messages": self.conversation_history + [{"role": "user", "content": message}],
                "temperature": temperature,
                "top_p": 0.9
            }
            
            # Realizar la solicitud POST
            response = requests.post(self.url, json=payload, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                # Guardar la respuesta en el historial
                self.conversation_history.append({
                    "role": "assistant",
                    "content": data["choices"][0]["message"]["content"]
                })
                # Actualizar el conteo de tokens
                self.total_tokens += data["usage"]["total_tokens"]
                
                return {
                    "response": data["choices"][0]["message"]["content"],
                    "tokens_used": data["usage"]["total_tokens"],
                    "total_tokens": self.total_tokens
                }
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error en la comunicación: {str(e)}")
            return None

def main():
    chat = SimpleChat()
    console.print(Panel.fit(
        "[yellow]Perplexity AI Simple Chat[/yellow]\n"
        "Comandos disponibles:\n"
        "- [cyan]salir[/cyan]: Termina el chat",
        title="Bienvenido"
    ))
    
    while True:
        try:
            user_input = console.input("\n[bold green]Usuario:[/bold green] ").strip()
            
            if user_input.lower() == "salir":
                console.print("[bold red]Chat terminado[/bold red]")
                break
            
            response = chat.send_message(user_input)
            
            if response:
                console.print(f"\n[bold green]Respuesta:[/bold green] {response['response']}")
                console.print(f"[bold blue]Tokens usados:[/bold blue] {response['tokens_used']}")
                console.print(f"[bold yellow]Tokens totales:[/bold yellow] {response['total_tokens']}")
                
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
            break

if __name__ == "__main__":
    main() 