import requests
import os
import json
from dotenv import load_dotenv
import logging
from typing import List, Dict, Any
import tiktoken
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

# Configuración de logging y console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
console = Console()

# Cargar variables de entorno
load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

class PerplexityChat:
    def __init__(self):
        self.url = "https://api.perplexity.ai/chat/completions"
        self.model = "llama-3.1-sonar-small-128k-online"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {PERPLEXITY_API_KEY}"
        }
        self.conversation_history: List[Dict[str, str]] = []
        self.total_tokens = 0
        self.total_cost = 0
        self.encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
        
    def calculate_cost(self, tokens: int) -> float:
        """Calcula el costo basado en el uso de tokens"""
        # $5 por 1000 requests + $0.2 por millón de tokens
        return (5/1000) + (tokens * 0.2 / 1_000_000)
        
    def display_metrics(self, metrics: Dict[str, Any]):
        """Muestra las métricas en una tabla formateada"""
        table = Table(title="Métricas de la Conversación")
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="magenta")
        
        table.add_row("Tokens en esta respuesta", str(metrics['tokens_this_request']))
        table.add_row("Total de tokens", str(metrics['total_tokens']))
        table.add_row("Turnos de conversación", str(metrics['conversation_turns']))
        table.add_row("Temperatura", str(metrics['temperature']))
        table.add_row("Costo estimado ($)", f"${metrics['estimated_cost']:.6f}")
        table.add_row("Costo total ($)", f"${metrics['total_cost']:.6f}")
        
        console.print(table)

    def send_message(self, message: str, temperature: float = 0.2) -> Dict[str, Any]:
        try:
            messages = self.prepare_messages(message)
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "top_p": 0.9
            }
            
            response = requests.post(self.url, json=payload, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                tokens_used = data["usage"]["total_tokens"]
                self.total_tokens += tokens_used
                
                # Calcular costos
                request_cost = self.calculate_cost(tokens_used)
                self.total_cost += request_cost
                
                # Guardar respuesta
                self.conversation_history.append({
                    "role": "assistant",
                    "content": data["choices"][0]["message"]["content"]
                })
                
                return {
                    "response": data["choices"][0]["message"]["content"],
                    "metrics": {
                        "tokens_this_request": tokens_used,
                        "total_tokens": self.total_tokens,
                        "conversation_turns": len(self.conversation_history) // 2,
                        "temperature": temperature,
                        "estimated_cost": request_cost,
                        "total_cost": self.total_cost
                    }
                }
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error en la comunicación: {str(e)}")
            return None

def main():
    chat = PerplexityChat()
    console.print(Panel.fit(
        "[yellow]Perplexity AI Chat[/yellow]\n"
        "Comandos disponibles:\n"
        "- [cyan]temp X[/cyan]: Cambia temperatura (0-1)\n"
        "- [cyan]clear[/cyan]: Limpia el historial\n"
        "- [cyan]salir[/cyan]: Termina el chat\n"
        "- [cyan]metrics[/cyan]: Muestra métricas actuales",
        title="Bienvenido"
    ))
    
    temperature = 0.2
    
    while True:
        try:
            user_input = console.input("\n[bold green]Usuario:[/bold green] ").strip()
            
            if user_input.lower() == 'salir':
                console.print("\n[yellow]¡Hasta luego![/yellow]")
                break
                
            elif user_input.lower() == 'clear':
                chat.conversation_history = []
                chat.total_tokens = 0
                chat.total_cost = 0
                console.print("[yellow]Historial limpiado[/yellow]")
                continue
                
            elif user_input.lower() == 'metrics':
                if chat.conversation_history:
                    chat.display_metrics({
                        "tokens_this_request": 0,
                        "total_tokens": chat.total_tokens,
                        "conversation_turns": len(chat.conversation_history) // 2,
                        "temperature": temperature,
                        "estimated_cost": 0,
                        "total_cost": chat.total_cost
                    })
                continue
                
            elif user_input.lower().startswith('temp '):
                try:
                    new_temp = float(user_input.split()[1])
                    if 0 <= new_temp <= 1:
                        temperature = new_temp
                        console.print(f"[yellow]Temperatura ajustada a: {temperature}[/yellow]")
                    else:
                        console.print("[red]La temperatura debe estar entre 0 y 1[/red]")
                except:
                    console.print("[red]Formato inválido. Usa 'temp 0.7' por ejemplo[/red]")
                continue
            
            response = chat.send_message(user_input, temperature)
            if response:
                console.print("\n[bold blue]Asistente:[/bold blue]", response["response"])
                chat.display_metrics(response["metrics"])
            else:
                console.print("[red]Error en la comunicación. Intenta de nuevo.[/red]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]¡Hasta luego![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    main()