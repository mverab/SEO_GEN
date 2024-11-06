from typing import Dict, List, Tuple
import pandas as pd
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class DataValidator:
    def __init__(self):
        self.required_columns = [
            'title',
            'keyword',
            'secondary_keywords',
            'PerplexityQuery'
        ]
        self.validation_results = {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "errors": []
        }
        
    def validate_csv_structure(self, df: pd.DataFrame) -> bool:
        """Valida la estructura del CSV"""
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        if missing_columns:
            logger.error(f"Columnas faltantes: {missing_columns}")
            return False
        return True
        
    def validate_row(self, row: pd.Series, index: int) -> Tuple[bool, List[str]]:
        """Valida una fila individual"""
        errors = []
        
        # Validar título
        if not row['title'] or pd.isna(row['title']):
            errors.append(f"Título vacío en fila {index}")
        elif len(str(row['title'])) > 150:
            errors.append(f"Título demasiado largo en fila {index}")
            
        # Validar palabra clave principal
        if not row['keyword'] or pd.isna(row['keyword']):
            errors.append(f"Palabra clave vacía en fila {index}")
            
        # Validar palabras clave secundarias
        if not row['secondary_keywords'] or pd.isna(row['secondary_keywords']):
            errors.append(f"Palabras clave secundarias vacías en fila {index}")
        else:
            keywords = str(row['secondary_keywords']).split(',')
            if len(keywords) < 2:
                errors.append(f"Se requieren al menos 2 palabras clave secundarias en fila {index}")
                
        return len(errors) == 0, errors
        
    def validate_csv(self, file_path: str) -> Tuple[bool, Dict]:
        """Valida el archivo CSV completo"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
                
            df = pd.read_csv(file_path)
            self.validation_results["total"] = len(df)
            
            if not self.validate_csv_structure(df):
                return False, self.validation_results
                
            invalid_rows = []
            for index, row in df.iterrows():
                is_valid, errors = self.validate_row(row, index)
                if not is_valid:
                    invalid_rows.append({
                        "row": index + 1,
                        "errors": errors
                    })
                    self.validation_results["invalid"] += 1
                    self.validation_results["errors"].extend(errors)
                else:
                    self.validation_results["valid"] += 1
                    
            # Generar reporte
            self.generate_validation_report(invalid_rows)
            
            return self.validation_results["invalid"] == 0, self.validation_results
            
        except Exception as e:
            logger.error(f"Error validando CSV: {str(e)}")
            self.validation_results["errors"].append(str(e))
            return False, self.validation_results
            
    def generate_validation_report(self, invalid_rows: List[Dict]):
        """Genera reporte de validación"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"validation_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=== Reporte de Validación ===\n\n")
            f.write(f"Total de filas: {self.validation_results['total']}\n")
            f.write(f"Filas válidas: {self.validation_results['valid']}\n")
            f.write(f"Filas inválidas: {self.validation_results['invalid']}\n\n")
            
            if invalid_rows:
                f.write("Errores encontrados:\n")
                for row in invalid_rows:
                    f.write(f"\nFila {row['row']}:\n")
                    for error in row['errors']:
                        f.write(f"- {error}\n")
                        
        logger.info(f"Reporte de validación generado: {report_file}") 