## Codigo que funciona con LED
import datetime
import BlynkLib
from gpiozero import LED
import time
import sqlite3
from datetime import datetime
def saveData(led):
    # Conexión a la base de datos SQLite
    connection = sqlite3.connect("prueba.db")
    cursor = connection.cursor()

    # Insertar el valor en la tabla 'led'
    cursor.execute('''
        INSERT INTO led (ltest1)
        VALUES (?)
    ''', (int(led),))  # Se pasa como una tupla con coma

    # Guardar los cambios y cerrar la conexión
    connection.commit()
    connection.close()

BLYNK_AUTH_TOKEN = "sL86IApPfR656oI-KaC97RTI1RIxELbu"
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN, server='blynk.cloud', port=80)
PIN = 18

led = LED(PIN)

# Add a handler for when V0 changes
@blynk.VIRTUAL_WRITE(0)
def v0_write_handler(value):
    if int(value[0]) == 1:
        led.on()
        print(f"Led Encendido (V0 value changed to: {value})")
    else:
        led.off()
        print(f"Led Apagado (V0 value changed to: {value})")


while True:
    blynk.run()
    time.sleep(0.1)  # Add a small delay to prevent high CPU usage