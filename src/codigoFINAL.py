
import cv2
import serial
import time
import numpy as np
import RPi.GPIO as GPIO

# ======= CONFIGURACIÓN =======
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)  # Pin del botón (pulldown interno si es necesario)

arduino = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)  # Esperar conexión serial

# ======= VARIABLES =======
verde_detectado = False
naranja_detectado = False
contador_giros = 0
total_giros = 12

# ======= ESPERAR BOTÓN DE INICIO =======
print("Esperando botón...")
while GPIO.input(26):
    time.sleep(0.1)
print("¡Inicio confirmado!")

# ======= FUNCIONES DE DETECCIÓN DE COLOR =======
def detectar_verde(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    verde_bajo = np.array([35, 100, 100])
    verde_alto = np.array([85, 255, 255])
    mascara = cv2.inRange(hsv, verde_bajo, verde_alto)

    alto = frame.shape[0]
    y_inferior = int(2 * alto / 3)
    linea = mascara[y_inferior:y_inferior+5, :]  # Línea horizontal inferior
    return np.sum(linea) > 5000  # Umbral para considerar "detectado"

def detectar_naranja(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    naranja_bajo = np.array([10, 100, 100])
    naranja_alto = np.array([25, 255, 255])
    mascara = cv2.inRange(hsv, naranja_bajo, naranja_alto)

    alto = frame.shape[0]
    y_inferior = int(2 * alto / 3)
    linea = mascara[y_inferior:y_inferior+5, :]  # Línea horizontal inferior
    return np.sum(linea) > 5000

# ======= INICIAR CÁMARA =======
cam = cv2.VideoCapture(0)

# ======= BUCLE PRINCIPAL =======
while True:
    ret, frame = cam.read()
    if not ret:
        print("Error al leer cámara")
        break

    if detectar_verde(frame):
        if not verde_detectado:
            arduino.write(b'V')  # Acción evasiva verde
            verde_detectado = True
            naranja_detectado = False
            print("Verde detectado")
    else:
        verde_detectado = False

    if detectar_naranja(frame):
        if not naranja_detectado:
            arduino.write(b'G')  # Giro por naranja
            naranja_detectado = True
            verde_detectado = False
            contador_giros += 1
            print(f"Naranja detectado. Giro #{contador_giros}")
    else:
        naranja_detectado = False

    # Verificar si se completaron los 12 giros
    if contador_giros >= total_giros:
        print("12 giros completados. Deteniendo todo.")
        arduino.write(b'S')  # Detener motores/servo en Arduino
        break

# ======= FINALIZAR =======
cam.release()
arduino.close()
GPIO.cleanup()
