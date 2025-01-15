import uvicorn
import logging

def main():
    """Ejecuta el servidor FastAPI"""
    uvicorn.run(
        "api:app", 
        host="0.0.0.0", 
        port=8001, 
        reload=True
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main() 