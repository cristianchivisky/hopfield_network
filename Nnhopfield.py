import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from asciimatics.screen import Screen
import logging

class HopfieldNetwork:
    """
    Implementación de una Red de Hopfield para el reconocimiento de patrones musicales.
    La red puede aprender patrones binarios y recuperarlos incluso cuando están distorsionados con ruido.
    
    Attributes:
        size (int): Tamaño de los patrones de entrada (número de neuronas en la red)
        weights (numpy.ndarray): Matriz de pesos sinápticos de la red
    """
    
    def __init__(self, size):
        """
        Inicializa la red con un tamaño específico.
        
        Args:
            size (int): Número de neuronas en la red
        """
        self.size = size
        self.weights = np.zeros((size, size))
    
    def train(self, patterns):
        """
        Entrena la red con un conjunto de patrones usando la regla de Hebbian.
        La regla de Hebbian establece que "las neuronas que se activan juntas, se conectan más fuertemente".
        En esta implementación, se utiliza el producto exterior para ajustar los pesos sinápticos de la red.

        Args:
            patterns (numpy.ndarray): Matriz donde cada fila es un patrón de entrenamiento
        """
        try:
            for pattern in patterns:
                # Calcula el producto exterior para cada patrón
                self.weights += np.outer(pattern, pattern)
            # Elimina las autoconexiones
            np.fill_diagonal(self.weights, 0)
            # Normaliza los pesos por el número de patrones
            self.weights /= len(patterns)
        except Exception as e:
            logging.error(f"Error durante el entrenamiento: {e}")
            raise e
    
    def recall(self, pattern, max_iter=10):
        """
        Recupera un patrón almacenado a partir de un patrón de entrada.
        El proceso de recuperación sigue iterando hasta que el patrón se estabiliza, es decir,
        no cambia en una iteración completa.

        Args:
            pattern (numpy.ndarray): Patrón de entrada a recuperar
            max_iter (int): Número máximo de iteraciones para la convergencia
        
        Returns:
            numpy.ndarray: Patrón recuperado
        """
        try:
            pattern = pattern.copy()
            for _ in range(max_iter):
                previous_pattern = pattern.copy()
                for i in range(self.size):
                    # Actualiza cada neurona según la regla de activación
                    pattern[i] = 1 if np.dot(self.weights[i], pattern) >= 0 else -1
                # Verifica si el patrón se ha estabilizado
                if np.array_equal(pattern, previous_pattern):
                    break
            return pattern
        except Exception as e:
            logging.error(f"Error durante la recuperación: {e}")
            raise e
    
    def add_noise(self, pattern, noise_level=0.3):
        """
        Añade ruido aleatorio a un patrón.
        
        Args:
            pattern (numpy.ndarray): Patrón original
            noise_level (float): Proporción de bits que serán invertidos (0-1)
        
        Returns:
            numpy.ndarray: Patrón con ruido
        """
        try:
            noisy_pattern = pattern.copy()
            num_noisy_bits = int(self.size * noise_level)
            noise_indices = np.random.choice(range(self.size), num_noisy_bits, replace=False)
            noisy_pattern[noise_indices] *= -1
            return noisy_pattern
        except Exception as e:
            logging.error(f"Error al añadir ruido: {e}")
            raise e

'''def plot_patterns(original, noisy, recovered, title=""):
    """
    Visualiza los patrones original, con ruido y recuperado.
    
    Args:
        original (numpy.ndarray): Patrón original
        noisy (numpy.ndarray): Patrón con ruido
        recovered (numpy.ndarray): Patrón recuperado
        title (str): Título para la visualización
    """
    try:
        fig, ax = plt.subplots(1, 3, figsize=(15, 5))
        ax[0].imshow(original.reshape(8, 8), cmap="bwr")
        ax[0].set_title("Original Pattern")
        ax[1].imshow(noisy.reshape(8, 8), cmap="bwr")
        ax[1].set_title("Noisy Pattern")
        ax[2].imshow(recovered.reshape(8, 8), cmap="bwr")
        ax[2].set_title("Recovered Pattern")
        plt.suptitle(title)
        plt.show()
    except Exception as e:
        logging.error(f"Error al graficar los patrones: {e}")'''

def plot_patterns_ascii(original, noisy, recovered, title=""):
    """
    Visualiza los patrones original, con ruido y recuperado en la consola usando ASCII.
    
    Args:
        original (numpy.ndarray): Patrón original
        noisy (numpy.ndarray): Patrón con ruido
        recovered (numpy.ndarray): Patrón recuperado
        title (str): Título para la visualización
    """
    try:
        # Crear una representación ASCII de los patrones
        def to_ascii(pattern):
            return [''.join(['#' if p == 1 else '_' for p in row]) for row in pattern.reshape(8, 8)]

        original_ascii = to_ascii(original)
        noisy_ascii = to_ascii(noisy)
        recovered_ascii = to_ascii(recovered)

        # Mostrar en la consola
        print("\n" + title)
        print("\nOriginal Pattern       Noisy Pattern       Recovered Pattern")
        print("-" * 55)
        for o_line, n_line, r_line in zip(original_ascii, noisy_ascii, recovered_ascii):
            print(f"{o_line:<20} {n_line:<20} {r_line:<20}")
        print("-" * 55)
    except Exception as e:
        logging.error(f"Error al graficar los patrones en ASCII: {e}")

def test_melody_recognition(network, pattern, melody_name, noise_level):
    """
    Prueba la capacidad de la red para reconocer una melodía con ruido.
    
    Args:
        network (HopfieldNetwork): Red de Hopfield entrenada
        pattern (numpy.ndarray): Patrón de melodía original
        melody_name (str): Nombre de la melodía para la visualización
        noise_level (float): Nivel de ruido a aplicar
    
    Returns:
        numpy.ndarray: Patrón recuperado
    """
    try:
        noisy_pattern = network.add_noise(pattern, noise_level)
        recovered_pattern = network.recall(noisy_pattern)
        plot_patterns_ascii(pattern, noisy_pattern, recovered_pattern, 
                     title=f"Reconstrucción de {melody_name}")
        return recovered_pattern
    except Exception as e:
        logging.error(f"Error durante la prueba de reconocimiento de la melodía: {e}")
        raise e

def compare_patterns(recovered, original, all_patterns):
    """
    Compara el patrón recuperado con el original y todos los patrones conocidos.
    
    Args:
        recovered (numpy.ndarray): Patrón recuperado
        original (numpy.ndarray): Patrón original
        all_patterns (numpy.ndarray): Todos los patrones de entrenamiento
    """
    try:
        if np.array_equal(recovered, original):
            print("La melodía recuperada coincide con la melodía original")
        else:
            similar_found = False
            for idx, pattern in enumerate(all_patterns):
                if np.array_equal(recovered, pattern):
                    print(f"La melodía recuperada coincide con otra melodía en el dataset (índice {idx})")
                    similar_found = True
                    break
            if not similar_found:
                print("La melodía recuperada no coincide completamente con ninguna de las melodías conocidas")
    except Exception as e:
        logging.error(f"Error al comparar los patrones: {e}")

# Función para validar niveles de ruido
def positive_float(value):
    val = float(value)
    if val < 0 or val > 1:
        raise argparse.ArgumentTypeError(f"{value} no está en el rango [0, 1]")
    return val

# Configuración de argparse para recibir el archivo CSV y el nivel de ruido
def parse_args():
    parser = argparse.ArgumentParser(description="Red de Hopfield para reconocimiento de patrones musicales")
    parser.add_argument('csv_file', type=str, help="Ruta al archivo CSV de melodías, opciones: 'melodias.csv' y 'melodias_dos.csv'")
    parser.add_argument('--noise_level_1', type=positive_float, default=0.4, help="El nivel de ruido a aplicarle al primer patrón. Es un valor entre 0 y 1")  
    parser.add_argument('--noise_level_2', type=positive_float, default=0.3, help="El nivel de ruido a aplicarle al segundo patrón. Es un valor entre 0 y 1")
    return parser.parse_args()

# Carga y preprocesamiento de datos
def load_data(csv_file):
    try:
        data = pd.read_csv(csv_file, header=None)
        data = data.iloc[1:, 1:]  # Elimina la primera fila (cabecera) y la primera columna
        patterns = data.values.astype(int)  # Convierte el DataFrame a una matriz de numpy
        return patterns
    except Exception as e:
        logging.error(f"Error al cargar los datos desde el archivo CSV: {e}")
        raise e

def main():
    # Configurar el logging
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Obtener el nombre del archivo CSV y el nivel de ruido desde los argumentos de la línea de comandos
        args = parse_args()
        patterns = load_data(args.csv_file)

        # Inicialización y entrenamiento de la red
        hopfield_net = HopfieldNetwork(size=patterns.shape[1])
        hopfield_net.train(patterns)
        print("Red de Hopfield entrenada exitosamente.")

        # Ejemplo de uso
        print("Probando recuperación de melodías con ruido")

        # Prueba con el primer patrón usando el nivel de ruido recibido
        recovered_pattern_1 = test_melody_recognition(hopfield_net, patterns[0], 
                                                     "Melodía 1", noise_level=args.noise_level_1)
        compare_patterns(recovered_pattern_1, patterns[0], patterns)

        # Prueba con el segundo patrón usando el nivel de ruido recibido
        recovered_pattern_2 = test_melody_recognition(hopfield_net, patterns[25], 
                                                     "Melodía 2", noise_level=args.noise_level_2)
        compare_patterns(recovered_pattern_2, patterns[25], patterns)
        print("Pruebas de reconocimiento completadas")
    except Exception as e:
        logging.critical(f"Ocurrió un error crítico: {e}")
        print("Ocurrió un error. Por favor, revisa los registros para más información.")

if __name__ == "__main__":
    main()