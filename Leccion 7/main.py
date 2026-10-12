from machine import Pin, ADC
from utime import sleep

# Importar librerías y configurar pines
in1 = Pin(19, Pin.OUT)        # LOZ enrolla (mete el tendedero)
in2 = Pin(18, Pin.OUT)        # LOZ despliega (saca el tendedero)
ldr = ADC(Pin(35))            # fotorresistencia: luz de dia
pot = ADC(Pin(34))            # potenciometro: simula lluvia
ldr.atten(ADC.ATTN_11DB)
pot.atten(ADC.ATTN_11DB)
in1.off()
in2.off()

UMBRAL_LUZ = 1500     # por debajo de esto, se considera "de noche" (ajustar con pruebas)
UMBRAL_LLUVIA = 2500  # por encima de esto, el pot simula "esta lloviendo"
TIEMPO_TORNO = 3       # segundos que gira el torno para enrollar/desplegar

# Definir funciones
def parar():
    in1.off()
    in2.off()

def enrollar():
    in2.off()
    in1.on()

def desplegar():
    in1.off()
    in2.on()

# 1) Medir luz y "lluvia" cada ciclo (habito de dato, como en L3)
# 2) Regla OR: de noche O lloviendo -> mete el tendedero
# 3) De dia y sin lluvia -> lo despliega
# El programa recuerda el estado para no enrollar/desplegar de mas
estado = "AFUERA"
print("=== TENDEDERO LISTO ===")

while True:
    luz = ldr.read()
    lluvia = pot.read()
    de_noche = luz < UMBRAL_LUZ
    esta_lloviendo = lluvia > UMBRAL_LLUVIA

    print("luz=", luz, "lluvia=", lluvia, "-> noche:", de_noche, " lluvia:", esta_lloviendo)

    if (de_noche or esta_lloviendo) and estado == "AFUERA":
        print("metiendo el tendedero")
        enrollar()
        sleep(TIEMPO_TORNO)
        parar()
        estado = "ADENTRO"

    elif (not de_noche) and (not esta_lloviendo) and estado == "ADENTRO":
        print("sacando el tendedero")
        desplegar()
        sleep(TIEMPO_TORNO)
        parar()
        estado = "AFUERA"

    sleep(1)
