# 1 importar las bibliotecas
import RPi.GPIO as GPIO
import time

# 2 Definir constantes
ESPERA = 0.5
PIN = 3

# 3 Configurar los pines GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)

# 4 Bucle infinito
while True:

    # 5 Encender el LED
    GPIO.output(PIN, GPIO.HIGH)

    # 6 Esperar tiempo
    time.sleep(ESPERA)

    # 7 Apagar el LED
    GPIO.output(PIN, GPIO.LOW)
    time.sleep(ESPERA)
