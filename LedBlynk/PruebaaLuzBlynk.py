## Prueba de Blynk con LDR (sin MCP3008)
import BlynkLib
import RPi.GPIO as GPIO
import time

BLYNK_AUTH_TOKEN = "5biBY2fS84cyCHbeU_lgTTEe4EFz-DAY"
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN, server='blynk.cloud', port=80)

LDR_PIN = 7  # Usamos el mismo pin que en tu ejemplo

GPIO.setmode(GPIO.BCM)

def rc_time(pin):
    count = 0

    # Cargar el condensador
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
    time.sleep(0.1)

    # Medir el tiempo de descarga (mientras el pin esté en bajo)
    GPIO.setup(pin, GPIO.IN)
    while GPIO.input(pin) == GPIO.LOW:
        count += 1
    return count

try:
    while True:
        ldr_value = rc_time(LDR_PIN)
        print(f"LDR Value: {ldr_value}")

        # Enviar a Blynk en V0
        blynk.virtual_write(1, ldr_value)

        blynk.run()
        time.sleep(1)

except KeyboardInterrupt:
    print("Programa interrumpido por el usuario")
    GPIO.cleanup()