import time
from rasa.nlu.model import Interpreter

# Carga el modelo de Rasa NLU desde la raíz
modelo_rasa = "./20240207-095927.tar.gz"
interpreter = Interpreter.load(modelo_rasa)

# Frase de ejemplo para la detección de intenciones
frase_ejemplo = "Buenos días"

# Mide el tiempo de ejecución
start_time = time.time()

# Realiza la detección de intenciones
result = interpreter.parse(frase_ejemplo)

# Calcula el tiempo de ejecución
end_time = time.time()
elapsed_time = end_time - start_time

# Imprime el resultado y el tiempo de ejecución
print("Resultado de la detección de intenciones:", result)
print("Tiempo de ejecución:", elapsed_time, "segundos")
