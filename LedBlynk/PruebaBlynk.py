## Prueba de Blynk sin Led
import BlynkLib
import time

BLYNK_AUTH_TOKEN = "5biBY2fS84cyCHbeU_lgTTEe4EFz-DAY"

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN, server='blynk.cloud', port=80)


@blynk.VIRTUAL_READ(0)
# def my_read_handler():
#     # Get current value of V0
#     v0_value = blynk.get_pin_value(0)
#     print(f"Current value of V0 (from read): {v0_value}")

# Add a handler for when V0 changes
@blynk.VIRTUAL_WRITE(0)
def v0_write_handler(value):
    print(f"V0 value changed to: {value}")


while True:
    blynk.run()
    time.sleep(0.1)  # Add a small delay to prevent high CPU usage