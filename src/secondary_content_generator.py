import os
import pandas as pd

async def get_perplexity_data(query: str) -> str:
    try:
        response = perplexity_client.chat.completions.create(
            model="llama-3.1-sonar-small-128k-online",
            messages=[{"role": "user", "content": query}]
        )
        data = response.choices[0].message.content
        
        # Guardar la respuesta para revisión
        os.makedirs('logs/perplexity_responses', exist_ok=True)
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        with open(f'logs/perplexity_responses/response_{timestamp}.txt', 'w', encoding='utf-8') as f:
            f.write(f"Query: {query}\n\nResponse:\n{data}")
            
        logger.info(f"Datos de Perplexity guardados en logs/perplexity_responses/response_{timestamp}.txt")
        return data
    except Exception as e:
        logger.error(f"Error Perplexity: {str(e)}")
        raise 