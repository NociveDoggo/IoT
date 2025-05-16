# ????
import gpiod
import time
import BlynkLib

# Configura tu Auth Token aquí
BLYNK_AUTH = 'LLl4IaHQoLIHU_4qe8_9SuBrEcz3WGQ1'

# Inicializa Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Configura el pin GPIO
LED_PIN = 18

chip = gpiod.Chip('gpiochip4')
led_line = chip.get_line(LED_PIN)
led_line.request(consumer='LED', type=gpiod.LINE_REQ_DIR_OUT)

# Cuando cambia el valor del botón en Blynk (por ejemplo en V0)
@blynk.VIRTUAL_WRITE(0)
def v0_write_handler(value):
    if int(value[0]) == 1:
        led_line.set_value(1)
    else:
        led_line.set_value(0)

try:
    while True:
        blynk.run()
        time.sleep(0.1)  # Small delay to prevent CPU overuse
except KeyboardInterrupt:
    # Clean up when the user interrupts the script
    led_line.release()
    chip.close()
    
    # :)
