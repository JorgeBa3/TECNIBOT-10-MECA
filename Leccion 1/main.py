from machine import Pin
from utime import sleep

# Importar librerías y configurar pines
in1 = Pin(19, Pin.OUT)        # LOZ derecha (abrir)
in2 = Pin(18, Pin.OUT)        # LOZ izquierda (cerrar)
led = Pin(23, Pin.OUT)        # LED indicador: encendido mientras el motor se mueve
in1.off()
in2.off()
led.off()
TIEMPO = 4                    # segundos de giro; más tiempo = más energía

# Definir funciones
def parar():
    in1.off()
    in2.off()
    led.off()               # en reposo el LED también se apaga: cero energía de más

def abrir():
    led.on()                # el LED avisa que el motor está en movimiento
    in2.off()
    in1.on()
    sleep(TIEMPO)
    parar()

def cerrar():
    led.on()
    in1.off()
    in2.on()
    sleep(TIEMPO)
    parar()

# 1) Abre un tiempo fijo
# 2) Para (el reposo también gasta cero)
# 3) Cierra el mismo tiempo y vuelve a reposo
while True:
    print("abriendo")
    abrir()
    print("espera")
    sleep(2)
    print("cerrando")
    cerrar()
    print("espera")
    sleep(2)
