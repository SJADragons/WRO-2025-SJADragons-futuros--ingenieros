import cv2 # Vista camara
import numpy as np # Lee colores
import serial # Conexion con arduino
import RPi.GPIO as GPIO # Usa boton START
import time # Tiempos

# Configura conexion con arduino
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2) # Tiempo para estabilizar

# Funcion Boton 
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Esperando que presiones el boton para iniciar...")
while GPIO.input(26):
    time.sleep(0.1)
    
print("Boton presionado. Iniciando programa...")
arduino.write(b'S')

with open("/home/alisson/inicio.log", "a") as f:
    f.write("Script arranco correctamente\n")

# Iniciar camara
cam = cv2.VideoCapture(0, cv2.CAP_V4L2)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320) # AJUSTAN RESOLUCION
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

if not cam.isOpened():
    print("No se pudo abrir la camara.")
    cam = None # Desactiva el uso de la camara
    
print("Camara abierta. Presiona 'q' para salir.")

# Guia de colores
naranja_detectado_anterior = False
rojo_detectado_anterior = False
naranja_activo = False
rojo_activo = False
verde_detectado_anterior = False
verde_activo = False


rojo_detectado = False
naranja_detectado = False
verde_detectado = False


# Mostrar video en vivo
while True:
    if cam:
        ret, frame = cam.read()
    if not ret:
            print("No se pudo leer la imagen.")
            continue
    
    # Obtener dimensiones
    alto, ancho = frame.shape[:2]
    
    # Calcula posiciones de las lineas
    y_superior = int(alto / 3)
    x_central = int(alto / 1.5)
    y_inferior = int(2 * alto / 3)
    
    color = (255, 255, 0 ) # Azul claro (BGR)
    grosor = 2
    
    # Dibuja las lineas horizontales
    cv2.line(frame, (0, y_superior), (ancho, y_superior), color, grosor)
    cv2.line(frame, (0, y_inferior), (ancho, y_inferior), color, grosor)
    
    # Dibuja la linea vertical
    cv2.line(frame, (x_central, 0), (x_central, alto), color, grosor)
    
    # Convertir a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Detectar NARANJA
    naranja_bajo = np.array([10, 100, 100])
    naranja_alto = np.array([25, 255, 255])
    
    # Detectar NARANJA
    mascara_naranja = cv2.inRange(hsv, naranja_bajo, naranja_alto)
    pixeles_naranjas = cv2.countNonZero(mascara_naranja) # basura
    
    # Buscar contornos NARANJA
    contornos_naranjas, _ = cv2.findContours(mascara_naranja, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contorno_naranja_detectado = False # Bandera
    
    for contorno in contornos_naranjas:
        area = cv2.contourArea(contorno)
        if area > 500:
            x, y, w, h = cv2.boundingRect(contorno)
            centro_y = y + h // 2
            
            # Dibuja rectangulo
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 140, 255,), 2)
            
            if centro_y > y_inferior:
                contorno_naranja_detectado = True
                if not naranja_detectado:
                    arduino.write(b'G') # Envia orden de giro
                    print("NARANJA DEBAJO DE LINEA GIRAR")
                    naranja_detectado = True
                    rojo_detectado = False
                    verde_detectado = False
                break
    
    # Si no se detecto contorno valido
    if not contorno_naranja_detectado:
        naranja_detectado = False
        
    # GIROS Control de deteccion NARANJA
    contador_giros = 0
    total_giros = 12
    deteccion_anterior = False
    
    # GIROS
    print("Sistema de deteccion iniciando...")
        
    # Detectar ROJO
    rojo_bajo1 = np.array([0, 120, 70])
    rojo_alto1 = np.array([10, 255, 255])
    rojo_bajo2 = np.array([170, 120, 70])
    rojo_alto2 = np.array([180, 255, 255])
    
    mascara_roja_1 = cv2.inRange(hsv, rojo_bajo1, rojo_alto1)
    mascara_roja_2 = cv2.inRange(hsv, rojo_bajo2, rojo_alto2)
    mascara_roja = cv2.bitwise_or(mascara_roja_1, mascara_roja_2)
    
    # Buscar contornos ROJO
    contornos_rojos, _ = cv2.findContours(mascara_roja, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contorno_rojo_detectado = False # Bandera
    
    for contorno in contornos_rojos:
        area = cv2.contourArea(contorno)
        if area > 500:
            x, y, w, h = cv2.boundingRect(contorno)
            centro_y = y + h // 2
            
            # Dibuja rectangulo
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255,), 2)
            
            if centro_y > y_inferior:
                contorno_rojo_detectado = True
                if not rojo_detectado:
                    arduino.write(b'R') # Comando para rojo
                    print("ROJO DEBAJO DE LINEA CHIFEA")
                    rojo_detectado = True
                    naranja_detectado = False
                    verde_detectado = False
                break # solo actua con el primer contorno valido
            
    # Si no se detecto ningun contorno valido, reiniciar estado
    if not contorno_rojo_detectado:
        rojo_detectado = False
                
                
                
    # Detectar VERDE
    verde_bajo = np.array([35, 100, 100])
    verde_alto = np.array([85, 255, 255])
    mascara_verde = cv2.inRange(hsv, verde_bajo, verde_alto)
    
    # Buscar contornos VERDE
    contornos_verdes, _ = cv2.findContours(mascara_verde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contorno_verde_detectado = False # Bandera
    
    for contorno in contornos_verdes:
        area = cv2.contourArea(contorno)
        if area > 500:
            x, y, w, h = cv2.boundingRect(contorno)
            centro_y = y + h // 2
            
            # Dibuja rectangulo
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0,), 2)
            
            if centro_y > y_inferior:
                contorno_verde_detectado = True
                if not verde_detectado:
                    arduino.write(b'V') # Comando para rojo
                    print("VERDE DEBAJO DE LINEA CHIFEA")
                    verde_detectado = True
                    naranja_detectado = False
                    rojo_detectado = False
                break # solo actua con el primer contorno valido
            
    # Si no se detecto ningun contorno valido, reiniciar estado
    if not contorno_verde_detectado:
        verde_detectado = False         
    # Si se detecta mucho rojo
    if cv2.countNonZero(mascara_roja) > 1000:
        cv2.putText(frame, "ROJO DETECTADO", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
    # Si se detecta mucho verde
    if cv2.countNonZero(mascara_verde) > 1000:
        cv2.putText(frame, "VERDE DETECTADO", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Si se detecta mucho naranja
    if cv2.countNonZero(mascara_naranja) > 1000:
        cv2.putText(frame, "NARANJA DETECTADO", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 140, 255), 2)
    
    # Vista del robot
    if cam:
        cv2.imshow("Vista", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): # Detiene con 'q'
            arduino.write(b'X') # Apaga motores
            break
    
# Finalizacion
arduino.write(b'X') # Orden de detener arduino
print("12 GIROS completados. Sistema detenido.")
# Apagar todo y salir
cam.release()
arduino.close()
cv2.destroyAllWindows()

