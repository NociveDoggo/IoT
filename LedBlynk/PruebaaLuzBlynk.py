## Prueba de Blynk con LDR usando GPIO Zero + lgpio (en pin 7)
import BlynkLib
import time
import lgpio  # Solo para leer el LDR

BLYNK_AUTH_TOKEN = "5biBY2fS84cyCHbeU_lgTTEe4EFz-DAY"
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN, server='blynk.cloud', port=80)

# Configuración del pin GPIO (BCM)
LDR_PIN = 7  # Asegúrate de estar usando numeración BCM (GPIO7)
chip = lgpio.gpiochip_open(0)

# Función para leer la luz desde el LDR usando método RC
def rc_time(pin):
    count = 0
    lgpio.gpio_claim_output(chip, pin, 0)
    time.sleep(0.1)
    lgpio.gpio_claim_input(chip, pin)
    while lgpio.gpio_read(chip, pin) == 0:
        count += 1
    return count

# Función opcional para mapear el valor
def map_value(x, in_min, in_max, out_min, out_max):
    x = min(max(x, in_min), in_max)  # Clamping
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Bucle principal
while True:
    ldr_raw = rc_time(LDR_PIN)
    ldr_scaled = map_value(ldr_raw, 100, 10000, 0, 100)
    
    print(f"Luz medida (raw): {ldr_raw}  -> mapeado: {ldr_scaled}")
    
    # Enviar a Blynk en V1
    blynk.virtual_write(1, ldr_scaled)
    
    blynk.run()
    time.sleep(1)