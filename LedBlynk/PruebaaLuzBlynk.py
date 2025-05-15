import RPi.GPIO as GPIO
import time
from BlynkLib import Blynk

BLYNK_AUTH = 'TU_TOKEN_BLYNK'

# Configura Blynk
blynk = Blynk(BLYNK_AUTH)

# Configura GPIO
LDR_PIN = 18
GPIO.setmode(GPIO.BCM)

def rc_time(pin):
    count = 0

    # Cargar el capacitor
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
    time.sleep(0.1)

    # Medir el tiempo de descarga
    GPIO.setup(pin, GPIO.IN)
    while GPIO.input(pin) == GPIO.LOW:
        count += 1
    return count

try:
    while True:
        ldr_value = rc_time(LDR_PIN)
        print("LDR:", ldr_value)
        blynk.virtual_write(0, ldr_value)
        blynk.run()
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()