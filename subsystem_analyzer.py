import numpy as np
import logging
from typing import Dict, List, Tuple
from modules.TPMproccessorD import TPMProcessor
from modules.partitionAnalyzerD import PartitionAnalyzer

class SubsystemAnalyzer:
    def __init__(self, tpm: np.ndarray, system_size: int = 7):  # 7 para ABCDEFG
        self.tpm = tpm
        self.system_size = system_size
        
    def parse_subsystem(self, spec: str) -> Dict:
        """
        Parsea una especificación de subsistema de la forma 'ABt+1|ABCt=100'
        y extrae la información relevante.
        """
        try:
            # Separar la parte futura y la condición
            future_part, condition = spec.split('|')
            condition_nodes, state = condition.split('=')
            
            # Extraer información
            future_nodes = future_part.replace('t+1', '')
            present_nodes = condition_nodes.replace('t', '')
            initial_state = state
            
            return {
                'future_nodes': future_nodes,
                'present_nodes': present_nodes,
                'initial_state': initial_state
            }
        except Exception as e:
            logging.error(f"Error parseando subsistema: {str(e)}")
            raise

    def get_subsystem_tpm(self, spec: str) -> np.ndarray:
        """
        Obtiene la TPM para el subsistema especificado.
        """
        try:
            # Parsear especificación
            info = self.parse_subsystem(spec)
            
            # Convertir estado binario a índice
            state_index = int(info['initial_state'], 2)
            
            # Obtener índices de los nodos futuros
            future_indices = [ord(n) - ord('A') for n in info['future_nodes']]
            
            # Extraer la fila correspondiente al estado inicial
            subsystem_tpm = self.tpm[state_index][:, future_indices]
            
            return subsystem_tpm
            
        except Exception as e:
            logging.error(f"Error obteniendo TPM del subsistema: {str(e)}")
            raise
            
    def analyze_subsystem(self, spec: str) -> Dict:
        """
        Analiza un subsistema específico y retorna información relevante.
        """
        try:
            info = self.parse_subsystem(spec)
            subsystem_tpm = self.get_subsystem_tpm(spec)
            
            analysis = {
                'specification': spec,
                'present_nodes': info['present_nodes'],
                'future_nodes': info['future_nodes'],
                'initial_state': info['initial_state'],
                'tpm': subsystem_tpm,
                'shape': subsystem_tpm.shape
            }
            
            return analysis
            
        except Exception as e:
            logging.error(f"Error analizando subsistema: {str(e)}")
            raise

def main():
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Primero cargamos y marginalizamos el sistema candidato
        from TPMProcessor import TPMProcessor
        
        # Cargar sistema completo
        processor = TPMProcessor("ResultadosEsperados10nodos1.csv")
        
        # Marginalizar para sistema candidato ABCDEFG
        candidate_system = "ABCDEFG"
        marginalized_tpm = processor.marginalize_system(candidate_system)
        
        # Analizar subsistema específico
        analyzer = SubsystemAnalyzer(marginalized_tpm)
        spec = "ABt+1|ABCt=100"
        
        result = analyzer.analyze_subsystem(spec)
        
        # Mostrar resultados
        print("\nAnálisis del Subsistema:")
        print("-" * 40)
        print(f"Especificación: {result['specification']}")
        print(f"Nodos presentes: {result['present_nodes']}")
        print(f"Nodos futuros: {result['future_nodes']}")
        print(f"Estado inicial: {result['initial_state']}")
        print(f"Forma de la TPM: {result['shape']}")
        print("\nTPM del subsistema:")
        print(result['tpm'])
        
    except Exception as e:
        logging.error(f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    main()