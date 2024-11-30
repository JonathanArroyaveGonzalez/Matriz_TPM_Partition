from modules.TPMproccessorD import TPMProcessor
import logging

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def test_data_loading():
    try:
        # Cargar y mostrar los primeros datos
        processor = TPMProcessor("SistemaCompleto10Nodos.csv")
        
        print("\nInformación de la TPM cargada:")
        print("-" * 50)
        print(f"Forma de la matriz: {processor.full_tpm.shape}")
        print("\nPrimeras 5 filas:")
        print(processor.full_tpm[:5])
        
        # Probar marginalización
        print("\nProbando marginalización:")
        print("-" * 50)
        candidate_system = "ABCDEFG"
        marginalized = processor.marginalize_system(candidate_system)
        print(f"Forma de la matriz marginalizada: {marginalized.shape}")
        print("\nPrimeras 3 filas de la matriz marginalizada:")
        print(marginalized[:3])
        
        return True
        
    except Exception as e:
        print(f"Error durante la prueba: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_data_loading()
    print("\nPrueba completada:", "Exitosa" if success else "Fallida")