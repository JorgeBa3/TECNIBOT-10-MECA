from machine import Pin, ADC
from utime import sleep, ticks_ms, ticks_diff

# Importar librerías y configurar pines
leds_zona = [Pin(12, Pin.OUT), Pin(14, Pin.OUT),
             Pin(27, Pin.OUT), Pin(33, Pin.OUT)]     # un LED por posición del dial (1, 2, 3, 4)
in1 = Pin(19, Pin.OUT)        # LOZ abrir
in2 = Pin(18, Pin.OUT)        # LOZ cerrar
dial = ADC(Pin(34))           # potenciómetro: el "dial" de la clave
dial.atten(ADC.ATTN_11DB)     # deja leer el rango completo 0 - 3.3V
in1.off()

in2.off()
for l in leds_zona:
    l.off()

CLAVE = [1, 3, 2, 4]          # secuencia correcta de posiciones del dial (1 a 4)
N_DIGITOS = len(CLAVE)
TIEMPO_POR_DIGITO = 3000       # milisegundos para girar el dial a cada posición

# Definir funciones
def leer_posicion():
    # Convierte la lectura del potenciómetro (0-4095) en una posición de 1 a 4
    valor = dial.read()
    zona = valor // 1024       # 0, 1, 2 o 3
    if zona > 3:
        zona = 3
    return zona + 1            # 1, 2, 3, 4

def mostrar_zona(zona):
    # Enciende solo el LED de la posición actual: los 4 LEDs muestran en vivo dónde está el dial
    for i, l in enumerate(leds_zona):
        l.value(1 if (i + 1) == zona else 0)

def apagar_zonas():
    for l in leds_zona:
        l.off()

def parar():
    in1.off()
    in2.off()

def abrir():
    in2.off()
    in1.on()

def cerrar():
    in1.off()
    in2.on()

def pedir_clave():
    secuencia = []
    for i in range(N_DIGITOS):
        print("Posición", i + 1, "de", N_DIGITOS, "- gira el dial...")
        inicio = ticks_ms()
        while ticks_diff(ticks_ms(), inicio) < TIEMPO_POR_DIGITO:
            mostrar_zona(leer_posicion())    # LED en vivo: muestra en qué zona está el dial ahora
            sleep(0.05)
        pos = leer_posicion()
        print("  -> leído: posición", pos)
        secuencia.append(pos)
        apagar_zonas()
        sleep(0.3)
    return secuencia

# 1) Pedir la clave girando el dial en 4 posiciones, una por una
#    (los 4 LEDs muestran en vivo, con cuál se enciende, en qué zona está el dial)
# 2) Clave correcta -> LOZ abre y cierra sola; incorrecta -> se queda cerrada y avisa
print("=== CAJA FUERTE LISTA ===")

while True:
    print("Marca la clave girando el dial...")
    clave_ingresada = pedir_clave()
    print("Secuencia ingresada:", clave_ingresada)

    if clave_ingresada == CLAVE:
        print("ABIERTO")
        abrir()
        sleep(1)
        parar()
        sleep(1)
        break
    else:
        print("CLAVE INCORRECTA")

    sleep(1)
