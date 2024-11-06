import pkg_resources
import sys
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_dependencies(requirements_file: str) -> Tuple[bool, List[str], List[str]]:
    """
    Verifica las dependencias instaladas contra requirements.txt
    Retorna: (todo_instalado, instaladas, faltantes)
    """
    # Leer requirements.txt
    with open(requirements_file) as f:
        required = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    installed = []
    missing = []
    
    for package in required:
        # Separar nombre y versión
        if '==' in package:
            name, version = package.split('==')
        else:
            name = package
            version = None

        try:
            pkg = pkg_resources.working_set.by_key[name]
            if version and pkg.version != version:
                logger.warning(f"⚠️  {name}: instalada {pkg.version}, requerida {version}")
            else:
                logger.info(f"✅ {name}: {pkg.version}")
            installed.append(f"{name}=={pkg.version}")
        except KeyError:
            logger.error(f"❌ {name}: no instalada")
            missing.append(package)

    return len(missing) == 0, installed, missing

def main():
    all_installed, installed, missing = check_dependencies('requirements.txt')
    
    print("\n=== Resumen de Dependencias ===")
    print(f"Total requeridas: {len(installed) + len(missing)}")
    print(f"Instaladas: {len(installed)}")
    print(f"Faltantes: {len(missing)}")
    
    if missing:
        print("\nPaquetes faltantes:")
        for pkg in missing:
            print(f"- {pkg}")
        print("\nPara instalar los paquetes faltantes:")
        print("pip install " + " ".join(missing))
        sys.exit(1)
    else:
        print("\n✅ Todas las dependencias están instaladas correctamente")
        sys.exit(0)

if __name__ == "__main__":
    main() 