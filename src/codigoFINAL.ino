#include <Servo.h>

// ===== SERVO CONFIGURACIÓN =====
const int pinServo = 5;
Servo miServo;

const int anguloMinimo = 0;
const int anguloMaximo = 60;
const int anguloNeutral = anguloMaximo;  // igual a 60
const int anguloDerecha = 120;


const int tiempoTotalMovimientoG = 500;   // 500 ms para comando 'G'
const int pasosServoG = anguloMaximo - anguloMinimo + 1;
const int velocidadMovimientoG = tiempoTotalMovimientoG / pasosServoG;  // ~8 ms por paso

const int tiempoTotalMovimientoV = 1000;  // 1000 ms para comando 'V' (más tiempo)
const int pasosServoV = anguloDerecha - anguloMinimo + 1;
const int velocidadMovimientoV = tiempoTotalMovimientoV / pasosServoV;  // ~8 ms por paso también

const int tiempoTotalMovimientoR = 1000;  // 1000 ms para comando 'R' (más tiempo)
const int pasosServoR = anguloMinimo - anguloDerecha + 1;
const int velocidadMovimientoR = tiempoTotalMovimientoR / pasosServoR;  // ~8 ms por paso también

// ===== MOTOR CONFIGURACIÓN =====
const int ENB = 11;
const int IN3 = A0;
const int IN4 = A1;
const int velocidadMotor = 255;

// ===== CONTROL =====
int contadorMovimientos = 0;
const int totalMovimientos = 12;
bool iniciado = false;
bool terminado = false;

void setup() {
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  miServo.attach(pinServo);
  miServo.write(anguloNeutral);
  delay(500);

  Serial.begin(9600);
  Serial.println("Esperando orden 'S' desde Raspberry Pi...");
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();

    if (!iniciado && comando == 'S') {
      Serial.println("Orden de inicio recibida. Arrancando motor...");
      avanzar();
      iniciado = true;
    }

    if (iniciado && !terminado && comando == 'G') {
      ejecutarGiro();
    }

    if (iniciado && !terminado && comando == 'R') {
      Serial.println("Orden 'R' recibida: evasión de obstáculo R.");
      evadirObstaculoR();
    }
    if (iniciado && !terminado && comando == 'V') {
      Serial.println("Orden 'R' recibida: evasión de obstáculo V.");
      evadirObstaculoV();
    }
  }
}

void avanzar() {
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, velocidadMotor);
}

void detener() {
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 0);
}

void girarServo(int desde, int hasta, int velocidadDelay) {
  int step = (desde < hasta) ? 1 : -1;
  for (int pos = desde; pos != hasta; pos += step) {
    miServo.write(pos);
    delay(velocidadDelay);
  }
  miServo.write(hasta);
  delay(velocidadDelay);
}

void evadirObstaculoV() {
  girarServo(anguloNeutral, anguloMinimo, velocidadMovimientoV);
  girarServo(anguloMinimo, anguloDerecha, velocidadMovimientoV);
  girarServo(anguloDerecha, anguloNeutral, velocidadMovimientoV);
  Serial.println("Evasión completada, servo en posición neutral.");
}

void evadirObstaculoR() {
  girarServo(anguloNeutral, anguloMinimo, velocidadMovimientoV);
  girarServo(anguloDerecha, anguloMinimo, velocidadMovimientoV);
  girarServo(anguloMinimo, anguloNeutral, velocidadMovimientoV);
  Serial.println("Evasión completada, servo en posición neutral.");
}

void ejecutarGiro() {
  if (terminado) return;

  Serial.print("Movimiento ");
  Serial.print(contadorMovimientos + 1);
  Serial.println(" de 12...");

  girarServo(anguloNeutral, anguloMinimo, velocidadMovimientoG);
  girarServo(anguloMinimo, anguloNeutral, velocidadMovimientoG);

  contadorMovimientos++;

  if (contadorMovimientos >= totalMovimientos) {
    Serial.println("Movimientos completados. Deteniendo motor y servo.");
    miServo.write(anguloNeutral);
    delay(500);
    detener();
    miServo.detach();
    terminado = true;
  }
}
