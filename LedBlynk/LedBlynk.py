## Codigo que funciona con LED

# Determinar si es local o raspberry
import platform
import datetime
import BlynkLib
import time
import sqlite3
from datetime import datetime

if platform.system() == 'Linux':
    from gpiozero import LED
else:
    # Mock LED class for non-Raspberry Pi environments
    class LED:
        def __init__(self, pin):
            self.pin = pin
            self.state = False
            
        def on(self):
            self.state = True
            print(f"Mock LED on pin {self.pin} turned ON")
            
        def off(self):
            self.state = False
            print(f"Mock LED on pin {self.pin} turned OFF")


BLYNK_AUTH_TOKEN = "sL86IApPfR656oI-KaC97RTI1RIxELbu"
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN, server='blynk.cloud', port=80)
PIN = 18

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

# Configuración SQLite
DATABASE_NAME = 'led_control.db'

def init_database():
    """Inicializa la base de datos y crea la tabla si no existe"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS led_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            led_state INTEGER NOT NULL,
            action_source TEXT NOT NULL,
            blynk_value TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_led_event(state, source, value=None):
    """Registra un evento de cambio de estado del LED"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO led_log (led_state, action_source, blynk_value)
            VALUES (?, ?, ?)
        ''', (1 if state else 0, source, str(value)))
        conn.commit()
        conn.close()
        print(f"Evento registrado en DB: LED {'ON' if state else 'OFF'} desde {source}")
    except Exception as e:
        print(f"Error al registrar en la base de datos: {e}")

def show_history(limit=5):
    """Muestra los últimos eventos registrados"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT timestamp, led_state, action_source
        FROM led_log
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    
    print("\nHistorial de eventos:")
    print("{:<20} {:<10} {:<15}".format("Fecha/Hora", "Estado", "Origen"))
    for row in cursor.fetchall():
        state = 'ON' if row[1] else 'OFF'
        print("{:<20} {:<10} {:<15}".format(
            row[0],
            state,
            row[2]
        ))
    conn.close()

# Inicializar la base de datos al inicio
init_database()

led = LED(PIN)

# Add a handler for when V0 changes
@blynk.VIRTUAL_WRITE(0)
def v0_write_handler(value):
    if int(value[0]) == 1:
        led.on()
        log_led_event(True, 'Blynk', value)
        print(f"Led Encendido (V0 value changed to: {value})")
    else:
        led.off()
        log_led_event(False, 'Blynk', value)
        print(f"Led Apagado (V0 value changed to: {value})")

# Bucle principal
try:
    print("Sistema iniciado. Esperando comandos de Blynk...")
    while True:
        blynk.run()
        time.sleep(0.1)
        
        # Opcional: Mostrar historial cada 30 segundos (solo para depuración)
        if int(time.time()) % 30 == 0:
            show_history()

except KeyboardInterrupt:
    print("\nSistema detenido")
    show_history(10)  # Mostrar últimos 10 eventos al salir