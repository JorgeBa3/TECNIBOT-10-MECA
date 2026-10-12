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

ANGULO_CENTRO = 90
ANGULO_ESQUIVE_IZQ = 135
ANGULO_ESQUIVE_DER = 45
T_RETROCESO = 0.6       # segundos que retrocede al toparse con un OBSTACULO
T_GIRO_FUERTE = 0.8     # segundos que avanza girado tras un OBSTACULO

# Definir funciones
def distancia_cm():
    trig.off()
    sleep_us(2)
    trig.on()
    sleep_us(10)             # pulso de 10 us (sleep(0.00001) a veces no alcanza)
    trig.off()
    t = time_pulse_us(echo, 1, 30000)
    if t < 0:
        return 400.0         # no llego el eco: cable, 5V o GND comun
    cm = (t * 0.0343) / 2
    if cm < 2 or cm > 400:
        return 400.0
    return cm

def angulo(g):
    # 0° ≈ 0.5 ms, 90° ≈ 1.5 ms, 180° ≈ 2.5 ms  (duty 0–1023, igual que probar_servo.py)
    us = 500 + (g / 180.0) * 2000
    d = int(us / 20000.0 * 1023)
    if d < 26:
        d = 26
    if d > 128:
        d = 128
    servo.duty(d)

def parar():
    in1.off()
    in2.off()

def avanzar():
    in2.off()
    in1.on()

def retroceder():
    in1.off()
    in2.on()

def lado_al_azar():
    return "izquierda" if urandom.getrandbits(1) == 0 else "derecha"

def girar_ruedas(lado):
    if lado == "izquierda":
        angulo(ANGULO_ESQUIVE_IZQ)
    else:
        angulo(ANGULO_ESQUIVE_DER)

def centrar_ruedas():
    angulo(ANGULO_CENTRO)

def promedio_de(mensaje):
    print(mensaje)
    lecturas = []
    for i in range(3):
        sleep(1)
        cm = distancia_cm()
        print("  lectura", i + 1, "=", round(cm, 1), "cm")
        lecturas.append(cm)
    return sum(lecturas) / len(lecturas)

def vecino_mas_cercano(cm, centros):
    # centros = [c_lejos, c_medio, c_obstaculo]
    mejor_i = 0
    mejor_dif = abs(cm - centros[0])
    for i in range(1, len(centros)):
        dif = abs(cm - centros[i])
        if dif < mejor_dif:
            mejor_dif = dif
            mejor_i = i
    return mejor_i

# 1) Calibrar: 3 rondas de 3 lecturas -> 3 centros LEJOS/MEDIO/OBSTACULO (K-means a mano)
# 2) Clasificar cada lectura nueva por vecino mas cercano
# 3) Reaccionar: LEJOS avanza recto / MEDIO gira ruedas suave sin parar / OBSTACULO para, retrocede y gira fuerte
print("=== CALIBRACION: sigan las instrucciones ===")
centrar_ruedas()
c_lejos = promedio_de("Ronda 1: camino despejado al frente (LEJOS)")
c_medio = promedio_de("Ronda 2: algo a media distancia, como un mueble (MEDIO)")
c_obstaculo = promedio_de("Ronda 3: objeto bien pegado al sensor (OBSTACULO)")
centros = [c_lejos, c_medio, c_obstaculo]
nombres = ["LEJOS", "MEDIO", "OBSTACULO"]
print("Centros:", [round(c, 1) for c in centros])
print("=== ROBOT BARREDOR LISTO ===")

lado_actual = "derecha"
estado = "LEJOS"

while True:
    cm = distancia_cm()
    clase = vecino_mas_cercano(cm, centros)
    print("cm=", round(cm, 1), "->", nombres[clase])

    if clase == 0:
        # LEJOS: ruedas centradas, sigue avanzando
        led.off()
        centrar_ruedas()
        avanzar()
        estado = "LEJOS"

    elif clase == 1:
        # MEDIO: gira las ruedas hacia un lado sin dejar de avanzar (empieza a esquivar)
        led.on()
        if estado != "ESQUIVANDO":
            lado_actual = lado_al_azar()
        girar_ruedas(lado_actual)
        avanzar()
        estado = "ESQUIVANDO"

    else:
        # OBSTACULO: para, retrocede, gira las ruedas fuerte hacia un lado al azar y avanza de nuevo
        led.on()
        parar()
        retroceder()
        sleep(T_RETROCESO)
        parar()
        lado_actual = lado_al_azar()
        print("gira fuerte hacia", lado_actual)
        girar_ruedas(lado_actual)
        avanzar()
        sleep(T_GIRO_FUERTE)
        estado = "ESQUIVANDO"

    sleep(0.15)
