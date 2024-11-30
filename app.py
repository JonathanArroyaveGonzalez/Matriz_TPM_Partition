from modules.TPMproccessorD import TPMProcessor
from modules.partitionAnalyzerD import PartitionAnalyzer
import logging

# Configurar logging
logging.basicConfig(
    filename='analysis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def analyze_subsystem(processor, marginalized_tpm, subsystem_spec):
    """Analiza un subsistema específico"""
    try:
        result = processor.process_subsystem(subsystem_spec, marginalized_tpm)
        
        print(f"\nAnálisis del Subsistema: {subsystem_spec}")
        print("-" * 50)
        print(f"Nodos presentes: {result['present_nodes']}")
        print(f"Nodos futuros: {result['future_nodes']}")
        print(f"Estado inicial: {result['initial_state']}")
        print("\nTPM del subsistema:")
        print(result['tpm'])
        
        return result
        
    except Exception as e:
        print(f"Error analizando subsistema: {str(e)}")
        return None

def main():
    try:
        # 1. Procesar la TPM
        processor = TPMProcessor("SistemaCompleto10Nodos.csv")
        candidate_system = "ABCDEFG"
        marginalized_tpm = processor.marginalize_system(candidate_system)

        # 2. Analizar subsistema específico
        subsystem_spec = "ABt+1|ABCt=101"
        subsystem_result = analyze_subsystem(processor, marginalized_tpm, subsystem_spec)

        # 3. Analizar particiones si se desea
        analyzer = PartitionAnalyzer(marginalized_tpm, "ABC", "AB")
        partition_results = analyzer.analyze_partitions()

        # 4. Visualizar resultados de partición
        analyzer.visualize_partition("resultado_particion.png")

        # 5. Imprimir resultados de partición
        print("\nResultados del análisis de partición:")
        print(f"Mejor partición: {partition_results['best_partition']}")
        print(f"Pérdida mínima: {partition_results['min_loss']}")
        print(f"Tiempo de ejecución: {partition_results['execution_time']} segundos")

    except Exception as e:
        logging.error(f"Error en la ejecución: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()