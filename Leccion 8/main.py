from machine import Pin, PWM, time_pulse_us
from utime import sleep, sleep_us
import urandom

# Importar librerías y configurar pines
led = Pin(26, Pin.OUT)
in1 = Pin(18, Pin.OUT)          # LOZ adelante
in2 = Pin(19, Pin.OUT)          # LOZ atrás
trig = Pin(4, Pin.OUT)          # ultrasónico TRIG
echo = Pin(5, Pin.IN)           # ultrasónico ECHO
servo = PWM(Pin(23))            # servo SG90: dirige las ruedas
servo.freq(50)
led.off()
in1.off()
in2.off()

PASO = 0.2      # segundos que empuja el LOZ en cada pasito (más grande = más rápido)
PAUSA = 0.4     # segundos de descanso entre pasitos (más grande = más lento)
GIRO = 40       # grados que se tuercen las ruedas al esquivar (más de 45 y la rueda arrastra)
PASITOS_GIRO = 4  # pasitos que avanza con las ruedas torcidas después de un obstáculo

# Definir funciones
def distancia_cm():
    trig.on()
    sleep_us(10)
    trig.off()
    t = time_pulse_us(echo, 1, 30000)
    if t < 0:
        return 400              # no llegó el eco: lejos o cable suelto
    return t * 0.0343 / 2

def ruedas(grados):
    # 90 = rectas, 135 = izquierda, 45 = derecha
    servo.duty(int((500 + grados / 180 * 2000) / 20000 * 1023))
    sleep(0.3)                  # deja que el servo termine antes de mover el LOZ

def pasito(pin):
    # El LOZ no puede ir "despacio" con PWM, así que avanza a ratitos
    pin.on()
    sleep(PASO)
    pin.off()
    sleep(PAUSA)

def centro_de(mensaje):
    print(mensaje, "- pulsa Enter")
    input()
    suma = 0
    for i in range(3):
        suma += distancia_cm()
        sleep(0.3)
    print("  centro =", round(suma / 3), "cm")
    return suma / 3

# 1) Calibrar: 3 centros LEJOS / MEDIO / OBSTACULO (K-means a mano)
print("=== CALIBRACION ===")
ruedas(90)
centros = [centro_de("Nada enfrente (LEJOS)"),
           centro_de("Algo a media distancia (MEDIO)"),
           centro_de("Mano pegada al sensor (OBSTACULO)")]
nombres = ["LEJOS", "MEDIO", "OBSTACULO"]
print("=== ROBOT BARREDOR LISTO ===")

while True:
    # 2) Clasificar: ¿a qué centro se parece más la distancia?
    cm = distancia_cm()
    diferencias = [abs(cm - c) for c in centros]
    clase = diferencias.index(min(diferencias))
    print(round(cm), "cm ->", nombres[clase])

    # 3) Reaccionar
    if clase == 0:              # LEJOS: ruedas rectas, un pasito adelante
        led.off()
        ruedas(90)
        pasito(in1)
    elif clase == 1:            # MEDIO: gira suave y sigue avanzando
        led.on()
        ruedas(90 + GIRO // 2)
        pasito(in1)
    else:                       # OBSTACULO: dos pasitos atrás y gira fuerte a un lado al azar
        led.on()
        ruedas(90)
        pasito(in2)
        pasito(in2)
        if urandom.getrandbits(1):
            ruedas(90 + GIRO)   # izquierda
        else:
            ruedas(90 - GIRO)   # derecha
        for i in range(PASITOS_GIRO):
            pasito(in1)         # avanza varios pasitos torcido para que sí dé la vuelta
