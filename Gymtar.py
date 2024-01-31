import subprocess
import sys

def ejecutar_rasa():
    comando = "rasa run -m models --enable-api --credentials credentials.yml"
    subprocess.run(comando, shell=True)

if __name__ == "__main__":
    ejecutar_rasa()
