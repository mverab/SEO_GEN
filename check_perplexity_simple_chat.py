import os
from dotenv import load_dotenv
import aiohttp
import asyncio

async def test_perplexity():
    load_dotenv()
    
    api_key = os.getenv('PERPLEXITY_API_KEY')
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [{"role": "user", "content": "What are the main advantages of real estate investment in Yucatan, Mexico?"}]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=data
        ) as response:
            print(f"Status: {response.status}")
            result = await response.json()
            print("\nRespuesta:")
            print(result['choices'][0]['message']['content'])

if __name__ == "__main__":
    asyncio.run(test_perplexity()) 