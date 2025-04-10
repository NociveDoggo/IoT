# 1 Importar la biblioteca (compatible con Raspberry Pi 5)
from gpiozero import LED
from time import sleep

# 2 Definir constantes
ESPERA = 0.5
PIN = 3  # Usar número de pin GPIO (BCM), no el número físico (BOARD)

# 3 Configurar el LED (gpiozero maneja el hardware automáticamente)
led = LED(PIN)  # Usa el esquema de numeración BCM por defecto

# 4 Bucle infinito
try:
    while True:
        # 5 Encender el LED
        led.on()
        
        # 6 Esperar tiempo
        sleep(ESPERA)
        
        # 7 Apagar el LED
        led.off()
        sleep(ESPERA)

# 8 Manejar la interrupción (Ctrl+C para salir)
except KeyboardInterrupt:
    print("\nPrograma terminado")
    # gpiozero limpia automáticamente los pines al salir