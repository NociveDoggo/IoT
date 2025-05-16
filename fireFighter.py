import RPI.GPIO as GPIO
import time
import Adafruit_DHT #para el sensor de humedad/temp
import cv2
import sqlite3 #vamos a usar SQLite!!
import Blynklib

#para conectar con blynk!!
BLYNK_AUTH = "" #aqui el token 
blynk = BlynkLib.Blynk(BLYNK_AUTH)

GPIO.setmode(GPIO.BCM)

#hay que checar si estos pines estan bien!!!
flameSensor1 = 17
flameSensor2 = 27
tempSensor1 = 22
tempSensor2 = 21
waterPump = 5
servo1 = 18
servo2 = 19

#inputs
GPIO.setup(flameSensor1, GPIO.IN)
GPIO.setup(flameSensor2, GPIO.IN)
GPIO.setup(tempSensor1, GPIO.IN)
GPIO.setup(tempSensor2, GPIO.IN)

#outputs
GPIO.setup(waterPump, GPIO.OUT)
GPIO.setup(servo1, GPIO.OUT)
GPIO.setup(servo1, GPIO.OUT)

#PWM usada para simular una señal analógica usando una señal digital
pwm_servo1 = GPIO.PWM(servo1, 50) #esta en 50Hz, hay que ver si se necesita cambiar
pwm_servo2 = GPIO.PWM(servo2, 50)
#inicializar los servos!
pwm_servo1.start(0)
pwm_servo2.start(0)

def readFlame (pin):
    return GPIO.input(pin) == 0 #0 para fuego detectado

def readTemp (pin):
    sensor = Adafruit_DHT.DHT11 #dht11 es el sensor de temp1
    h, t = Adafruit_DHT.read_retry(sensor, pin)
    return h, t

def servoControl (pwm, angle):

def waterControl (pinWaterPump, turnOn = TRUE):
    GPIO.output(pin, GPIO.LOW if encender else GPIO.HIGH)

def videoCapture(duration=5):
    cam = cv2.VideoCapture(0) #inicializa la cámara
    if not cam.isOpened():
        print("no se pudo abrir la cámara :(")
        return
    #generamos el archivo con fecha, hora y nombre
    timestamp = datetime.now()strftime("%Y%m%d_%H%M%S")
    filename = f"video_alerta_{timestamp}.avi"

    #para comprimir el video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #tecnicalidades del video
    fps = 24.0
    frame_size = (int(cam.get(3)), int(cam.get(4)))
    out = cv2.VideoWriter(filename, fourcc, fps, frame_size) #para escribir el video en disco
    print("grabando video---")
    start_time = time.time()
    while time.time() - start_time < duracion_segundos:
        ret, frame = cam.read()  # Captura un frame
        if not ret:
            break  # Si falla la captura, sale del bucle

        out.write(frame)  # Guarda el frame en el archivo de video

    # Libera la cámara y el archivo de salida
    cam.release()
    out.release()

    print("Video guardado :)")

#función para guardar los datos en la base de datos
def saveData(temp1, hum1, temp2, hum2, flame1, flame2, alert):
    #aquí la conexión a SQLite usando sqlite3!!
    #para bases de datos https://randomnerdtutorials.com/sqlite-database-on-a-raspberry-pi/
    connection = sqlite3.connect("datosSensores.db")
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO sensores (temp1, hum1, temp2, hum2, fuego1, fuego2, alerta)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (temp1, hum1, temp2, hum2, int(fuego1), int(fuego2), int(alerta)))
    connection.commit()
    connection.close()

try: #main loop 
    while True:
        blynk.run()
        hum1, temp1 = readTemp(tempSensor1)
        hum2, temp2 = readTemp(tempSensor2)

        fire1 = readFlame(flameSensor1)
        fire2 = readFlame(flameSensor2)

        alert = (fire1 or fire2 or 
            (hum1 is not None and hum1 < 30) or 
            (hum2 is not None and hum2 < 30) or 
            (temp1 is not None and temp1 > 70) or 
            (temp2 is not None and temp2 > 70))
        
        saveData(temp1, hum1, temp2, hum2, fire1, fire2, alert) #para la base de datos!!!

        #guardar datos usando blynk!!
        blynk.virtual_write(0, temp1)
        blynk.virtual_write(1, hum1)
        blynk.virtual_write(0, temp2)
        blynk.virtual_write(1, hum2)

        blynk.virtual_write(1, hum1)
        blynk.virtual_write(1, hum1)
        blynk.virtual_write(1, hum1)

        #ok y que pedo con la alerta? puessss;
        if alert:
            servoControl(pwm_servo1, 90)
            servoControl(pwm_servo2, 90) #el 90 es un ejemplo de ángulo, habrá que calibrar!!            
            waterControl(pinWaterPump, turnOn=True)
            videoCapture()
            saveData(temp1, hum1, temp2, hum2, fire1, fire2, alert)
            
        else:
            servoControl(pwm_servo1, 0)
            servoControl(pwm_servo2, 0)           
            waterControl(pinWaterPump, turnOn=False)

        time.sleep(3) #para no saturarlo, lo mandamos a mimir para 3s
        
finally:
    pwm_servo1.stop()
    pwm_servo2.stop()
    GPIO.cleanup()

