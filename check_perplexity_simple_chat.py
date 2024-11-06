import os
from dotenv import load_dotenv

def simple_content_check(content):
    """
    Verificación básica del contenido
    """
    if not content or len(content.strip()) < 10:
        return False, "Contenido demasiado corto"
    return True, "OK"

def main():
    load_dotenv()
    
    # Configuración básica
    content = input("Ingrese el contenido a verificar: ")
    
    # Verificación simple
    is_valid, message = simple_content_check(content)
    
    if is_valid:
        print("✅ Contenido válido")
    else:
        print(f"❌ Error: {message}")

if __name__ == "__main__":
    main() 