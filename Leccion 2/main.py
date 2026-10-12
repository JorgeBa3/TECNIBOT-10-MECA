from machine import Pin, ADC
from utime import sleep

# Importar librerías y configurar pines
in1 = Pin(19, Pin.OUT)        # LOZ derecha (abre la ventana)
in2 = Pin(18, Pin.OUT)        # LOZ izquierda (cierra la ventana)
led = Pin(23, Pin.OUT)        # LED indicador: encendido mientras el motor se mueve
ldr = ADC(Pin(35))            # fotorresistencia: mide cuánta luz de sol entra
ldr.atten(ADC.ATTN_11DB)      # lectura completa de 0 a 4095
in1.off()
in2.off()
led.off()

UMBRAL_SOL = 1500     # arriba de esto hay sol; abajo, no hay (ajústalo mirando la consola)
TIEMPO = 3            # segundos que gira el LOZ para abrir o cerrar la ventana

# Definir funciones
def parar():
    in1.off()
    in2.off()
    led.off()

def abrir_ventana():
    led.on()
    in2.off()
    in1.on()
    sleep(TIEMPO)
    parar()

def cerrar_ventana():
    led.on()
    in1.off()
    in2.on()
    sleep(TIEMPO)
    parar()

# 1) Medir la luz con la fotorresistencia
# 2) Clasificar con un umbral: ¿hay sol o no hay sol?
# 3) Hay sol -> abre la ventana; no hay sol -> la cierra
#    El programa recuerda si la ventana ya está abierta o cerrada
#    para no mover el motor de más.
estado = "CERRADA"
print("=== VENTANA INTELIGENTE LISTA ===")

while True:
    luz = ldr.read()
    hay_sol = luz > UMBRAL_SOL
    print("luz =", luz, "-> hay sol:", hay_sol, "| ventana:", estado)

    if hay_sol and estado == "CERRADA":
        print("hay sol: abriendo la ventana")
        abrir_ventana()
        estado = "ABIERTA"

    elif (not hay_sol) and estado == "ABIERTA":
        print("no hay sol: cerrando la ventana")
        cerrar_ventana()
        estado = "CERRADA"

    sleep(1)
