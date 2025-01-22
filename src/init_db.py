from database import engine
import models

def init_db():
    """Inicializa la base de datos"""
    models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creando tablas de base de datos...")
    init_db()
    print("¡Base de datos inicializada!") 