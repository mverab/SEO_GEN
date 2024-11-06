import os
from dotenv import load_dotenv
import asyncio
import aiohttp
import pandas as pd
from datetime import datetime
import ssl
import certifi
import json

async def test_perplexity():
    """Prueba rápida de integración"""
    load_dotenv(override=True)
    
    api_key = os.getenv('PERPLEXITY_API_KEY')
    print(f"API Key cargada: {api_key[:10]}...")
    
    if not api_key.startswith('pplx-'):
        raise ValueError("API key inválida - debe empezar con 'pplx-'")
    
    df = pd.read_csv('data/input/test_articles.csv')
    test_row = df.iloc[0]
    
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        
        data = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un experto en bienes raíces escribiendo en español."
                },
                {
                    "role": "user",
                    "content": test_row['PerplexityQuery']
                }
            ]
        }
        
        try:
            print("Enviando solicitud...")
            print("URL:", "https://api.perplexity.ai/chat/completions")
            print("Headers:", json.dumps(headers, indent=2))
            print("Data:", json.dumps(data, indent=2))
            
            async with session.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=data
            ) as response:
                print(f"Status Code: {response.status}")
                response_text = await response.text()
                print(f"Response: {response_text}")
                
                if response.status == 200:
                    result = await response.json()
                    
                    # Guardar resultado
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"test_article_{timestamp}.txt"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"# {test_row['title']}\n\n")
                        f.write(f"Keyword: {test_row['keyword']}\n\n")
                        f.write(result['choices'][0]['message']['content'])
                    
                    print(f"✅ Artículo generado en {filename}")
                else:
                    print(f"❌ Error: {response_text}")
                    
        except Exception as e:
            print(f"❌ Error detallado: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_perplexity())
