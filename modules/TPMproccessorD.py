import numpy as np
import logging
from typing import Dict, Tuple
import re

class TPMProcessor:
    def __init__(self, file_path: str):
        """Inicializa el procesador TPM con el archivo de datos"""
        self.full_tpm = self.load_tpm(file_path)
        self.system_size = 10  # Para un sistema de 10 nodos (A-J)
        logging.info(f"Sistema inicializado con {self.system_size} nodos")

    def clean_line(self, line: str) -> list:
        """Limpia una línea de texto y extrae los números"""
        try:
            # Remover corchetes, espacios y comas al final
            clean = line.strip('[] \n,')
            # Separar por comas y convertir a float
            numbers = []
            for num in clean.split(','):
                num = num.strip()
                if num:  # Si no está vacío
                    try:
                        numbers.append(float(num))
                    except ValueError:
                        logging.warning(f"Valor no numérico encontrado: {num}")
            return numbers
        except Exception as e:
            logging.error(f"Error limpiando línea: {line}")
            logging.error(str(e))
            return []

    def load_tpm(self, file_path: str) -> np.ndarray:
        """Carga la TPM desde un archivo CSV y limpia los datos"""
        try:
            logging.info(f"Intentando cargar archivo: {file_path}")
            
            # Leer el archivo
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                lines = file.readlines()

            # Procesar líneas
            rows = []
            for i, line in enumerate(lines):
                if line.strip():  # Si la línea no está vacía
                    numbers = self.clean_line(line)
                    if len(numbers) == 10:  # Verificar que tengamos 10 números
                        rows.append(numbers)
                    else:
                        logging.warning(f"Línea {i+1} ignorada: {len(numbers)} valores (se esperaban 10)")

            if not rows:
                raise ValueError("No se pudieron cargar datos válidos del archivo")

            # Convertir a array numpy
            numeric_data = np.array(rows, dtype=np.float64)
            logging.info(f"TPM cargada exitosamente: forma {numeric_data.shape}")
            
            # Verificación adicional
            if numeric_data.shape[1] != 10:
                raise ValueError(f"Se esperaban 10 columnas, se encontraron {numeric_data.shape[1]}")

            return numeric_data

        except Exception as e:
            logging.error(f"Error al cargar TPM: {str(e)}")
            raise

    def marginalize_system(self, candidate_nodes: str) -> np.ndarray:
        """Marginaliza el sistema para los nodos candidatos"""
        try:
            nodes_to_keep = [i for i, node in enumerate('ABCDEFGHIJ') if node in candidate_nodes]
            states = 2 ** len(candidate_nodes)
            
            marginalized_tpm = np.zeros((states, len(candidate_nodes)), dtype=np.float64)
            
            for i in range(len(self.full_tpm)):
                state_binary = format(i, f'0{self.system_size}b')
                new_state = ''.join(state_binary[j] for j in range(self.system_size) 
                                  if 'ABCDEFGHIJ'[j] in candidate_nodes)
                new_state_idx = int(new_state, 2)
                
                values_to_add = self.full_tpm[i][nodes_to_keep].astype(np.float64)
                marginalized_tpm[new_state_idx] += values_to_add

            # Normalizar
            row_sums = marginalized_tpm.sum(axis=1, keepdims=True)
            row_sums[row_sums == 0] = 1
            marginalized_tpm = marginalized_tpm / row_sums
                
            logging.info(f"Sistema marginalizado para nodos: {candidate_nodes}")
            return marginalized_tpm
            
        except Exception as e:
            logging.error(f"Error en marginalización: {str(e)}")
            raise

    def process_subsystem(self, spec: str, marginalized_tpm: np.ndarray) -> Dict:
        """Procesa un subsistema específico como 'ABt+1|ABCt=100'"""
        try:
            # Parsear especificación
            future_part, condition = spec.split('|')
            condition_nodes, state = condition.split('=')
            
            future_nodes = future_part.replace('t+1', '')
            present_nodes = condition_nodes.replace('t', '')
            initial_state = state
            
            # Obtener índice del estado inicial
            state_idx = int(initial_state, 2)
            
            # Obtener índices de los nodos futuros
            future_indices = [ord(n) - ord('A') for n in future_nodes]
            
            # Extraer la TPM del subsistema
            subsystem_tpm = marginalized_tpm[state_idx:state_idx+1, future_indices]
            
            return {
                'tpm': subsystem_tpm,
                'present_nodes': present_nodes,
                'future_nodes': future_nodes,
                'initial_state': initial_state,
                'specification': spec
            }
            
        except Exception as e:
            logging.error(f"Error procesando subsistema: {str(e)}")
            raise

def test_processor():
    """Función de prueba para verificar la carga de datos"""
    logging.basicConfig(level=logging.INFO)
    try:
        processor = TPMProcessor("SistemaCompleto10Nodos.csv")
        print("\nForma de la TPM:", processor.full_tpm.shape)
        print("\nPrimeras 3 filas:")
        print(processor.full_tpm[:3])
        return True
    except Exception as e:
        print(f"Error en prueba: {str(e)}")
        return False

if __name__ == "__main__":
    test_processor()