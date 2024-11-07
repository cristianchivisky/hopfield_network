# Red de Hopfield para Reconocimiento de Melodías

Este proyecto implementa una Red de Hopfield para el reconocimiento y recuperación de patrones musicales. La red es capaz de aprender diferentes melodías representadas como patrones binarios y recuperarlas incluso cuando están distorsionadas por ruido. El sistema incluye registro de errores, visualización en ASCII de los patrones y herramientas para añadir ruido a los mismos.

## Descripción General

La Red de Hopfield es un tipo de red neuronal recurrente que puede funcionar como memoria asociativa, permitiendo recuperar patrones completos a partir de versiones incompletas o distorsionadas. En este proyecto, se utiliza para:

1. Almacenar patrones que representan melodías musicales
2. Recuperar melodías originales a partir de versiones con ruido
3. Visualizar el proceso de recuperación de patrones

## Componentes Principales

### 1. Clase HopfieldNetwork

La clase principal que implementa la red neuronal con los siguientes métodos:

- __init__(self, size): Inicializa la red con un número específico de neuronas.
- train(self, patterns): Entrena la red utilizando los patrones de entrada mediante la regla de Hebbian.
- recall(self, pattern, max_iter=10): Recupera un patrón almacenado a partir de un patrón de entrada, utilizando el algoritmo de actualización iterativa.
- add_noise(self, pattern, noise_level=0.3): Añade ruido aleatorio a un patrón, invirtiendo un porcentaje de los bits de acuerdo con el nivel de ruido especificado.

### 2. Funciones de Utilidad

- plot_patterns_ascii(original, noisy, recovered, title=""): Muestra los patrones original, con ruido y recuperado en la consola utilizando caracteres ASCII.
- test_melody_recognition(network, pattern, melody_name, noise_level): Realiza una prueba de reconocimiento para una melodía, aplicando ruido al patrón y luego recuperándolo.
- compare_patterns(recovered, original, all_patterns): Compara el patrón recuperado con el original y con otros patrones conocidos para verificar su exactitud.

### 3. parse_args()

- Función que utiliza la librería argparse para obtener los argumentos de la línea de comandos, incluyendo el archivo CSV que contiene los patrones musicales y el nivel de ruido a aplicar a los patrones.

### 4. load_data(csv_file)

- Función para cargar los datos de melodías desde un archivo CSV. El archivo debe contener las melodías representadas como patrones binarios (una matriz de 1s y -1s).

## Funcionamiento Detallado

### Proceso de Entrenamiento

- La red se entrena con un conjunto de patrones musicales (una matriz de 1s y -1s) utilizando la regla de Hebbian. Esta regla establece que las conexiones entre neuronas se fortalecen si ambas neuronas se activan simultáneamente. En este caso, se calcula el producto exterior de cada patrón de entrada para ajustar los pesos sinápticos de la red.

### Proceso de Recuperación

- Después de entrenar la red, se puede recuperar un patrón a partir de un patrón de entrada distorsionado. El proceso de recuperación sigue un algoritmo iterativo en el que cada neurona se actualiza en función de las entradas de las demás neuronas. El patrón se considera recuperado cuando no cambia más en las iteraciones sucesivas.

### Añadir Ruido

Para simular el reconocimiento de melodías en condiciones ruidosas, se añade ruido a los patrones originales. El nivel de ruido se especifica como un porcentaje de bits que se invertirán aleatoriamente en el patrón.

### Visualización

- Los patrones se visualizan utilizando caracteres ASCII en la consola. El patrón original, el patrón con ruido y el patrón recuperado se muestran en tres columnas, lo que permite una fácil comparación visual.

## Requisitos

- Git
- Docker

## Formato de Datos

El código espera un archivo CSV con el siguiente formato:
- Cada fila representa una melodía diferente
- Los valores deben ser binarios (-1 o 1)
- Se asume que los patrones son cuadrados (por ejemplo, 8x8)

## Limitaciones y Consideraciones

1. Capacidad de Almacenamiento:
   - La red tiene una capacidad limitada de almacenamiento
   - Para N neuronas, se pueden almacenar aproximadamente 0.15N patrones

2. Estabilidad:
   - No se garantiza la convergencia a un patrón almacenado
   - Pueden existir estados espurios (mínimos locales)

3. Patrones Similares:
   - La red puede confundirse con patrones muy similares
   - Es importante que los patrones de entrenamiento sean suficientemente diferentes

## Instalación

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/cristianchivisky/hopfield_network.git
   ```

2. **Navega al directorio**

   ```bash
   cd hopfield_network
   ```

3. **Construir la Imagen Docker**

Construye la imagen Docker utilizando el comando:

   ```bash
   docker build -t hopfield_app .
   ```

Esto creará una imagen llamada **hopfield-network** a partir del archivo **Dockerfile** en el directorio actual.

## Uso

Los archivos de entrada, como melodias.csv y melodias_dos.csv, ya están proporcionados en el contenedor. Cada archivo contiene patrones binarios que representen melodías.

1. **Ejecutar el Contenedor Docker**

Para ejecutar la aplicación en un contenedor Docker:

   ```bash
   docker run -it --rm hopfield_app
   ```
Se ejecutará por defecto usando el archivo melodias.csv, --noise_level_1 = 0.4 y --noise_level_2 = 0.3

**Parámetros que admite:**

- melodias.csv o melodias_dos.csv: Archivo CSV de entrada que contiene los patrones de melodías.
- --noise_level_1: Nivel de ruido para probar el primer patrón (entre 0 y 1).
- --noise_level_2: Nivel de ruido para probar el segundo patrón (entre 0 y 1).

Para ejecutar la aplicación con los parametros anteriores:

   ```bash
   docker run -it --rm hopfield_app melodias_dos.csv --noise_level_1 0.2 --noise_level_2 0.4
   ```

La red cargará los datos, entrenará con los patrones proporcionados y probará la recuperación en patrones específicos con ruido.

## Interpretación de Resultados

Después de ejecutar el programa, verás en la consola los resultados de las pruebas de reconocimiento de melodías. Para cada melodía probada:

1. Se mostrarán en formato ASCII los patrones original, con ruido y recuperado.
2. La consola indicará si la melodía recuperada coincide con el original, con otra melodía conocida o con ninguna melodía conocida.

Este resultado ayuda a verificar si la red de Hopfield reconoce las melodías con precisión a pesar del ruido.

## Solución de Problemas

Si encuentras problemas al ejecutar el programa, consulta esta guía de solución de problemas.

### Manual para Corridas Infructuosas

Esta sección proporciona orientación sobre errores comunes y cómo resolverlos.

1. **Error: "Error al cargar datos desde CSV"**

- Causa: El archivo CSV de entrada puede estar mal formateado o no encontrado.
- Solución: Asegúrate de que tu archivo CSV sigue el formato esperado descrito arriba y que existe en el directorio.

2. **Error: "Error durante el entrenamiento"**

- Causa: Ocurrió un problema durante el cálculo de los pesos.
- Solución: Verifica los datos de entrada para encontrar inconsistencias, como valores que no sean binarios o filas de longitud variable.

3. **Error: "Error durante la recuperación"**

- Causa: Falló el proceso de recuperación de patrones.
- Solución: Verifica que la red se haya entrenado correctamente con patrones de la longitud correcta. Intenta reducir el nivel de ruido.

4. **Error: "Error al añadir ruido"**

- Causa: El nivel de ruido especificado puede ser demasiado alto.
- Solución: Ajusta el nivel de ruido dentro de un rango razonable (por ejemplo, de 0.1 a 0.4) e intenta nuevamente.

5. **Errores críticos (por ejemplo, "Ocurrió un error. Por favor, revisa los registros para más información.")**

- Solución: Consulta el archivo de registro o el mensaje de la consola para obtener detalles sobre el error. Estos mensajes suelen proporcionar pistas sobre problemas en la carga de datos, el procesamiento o la configuración de la red.
