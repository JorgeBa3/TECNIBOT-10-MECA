from machine import Pin, ADC
from utime import sleep

# Configurar pines
ldr = ADC(Pin(35))            # Sensor de carga (LDR)
led = Pin(26, Pin.OUT)        # LED de estado
motor_subir = Pin(19, Pin.OUT)
motor_bajar = Pin(18, Pin.OUT)

# Calibrar ADC
ldr.atten(ADC.ATTN_11DB)

# Apagar todo al inicio
led.off()
motor_subir.off()
motor_bajar.off()

# Constantes
UMBRAL_LUZ = 30       # Oscuridad = hay carga
TIEMPO_VIAJE = 3      # Segundos que tarda en subir/bajar
viajando = False

# Funciones
def parar():
    motor_subir.off()
    motor_bajar.off()
    led.off()

def subir(duracion):
    motor_bajar.off()
    motor_subir.on()
    led.on()
    sleep(duracion)
    parar()

def bajar(duracion):
    motor_subir.off()
    motor_bajar.on()
    led.on()
    sleep(duracion)
    parar()

# Bucle principal
while True:
    # Leer luz (carga presente = oscuro)
    luz_raw = ldr.read()
    luz = (luz_raw / 4095.0) * 100.0
    
    print("luz=", round(luz, 1), "%")
    
    # Si hay carga y no está viajando: hacer viaje completo
    if luz < UMBRAL_LUZ:
        if not viajando:
            print("Carga detectada: subiendo...")
            subir(TIEMPO_VIAJE)
            sleep(1)  # Pausa entre subida y bajada
            print("Bajando...")
            bajar(TIEMPO_VIAJE)
            viajando = True
            print("Viaje completo")
    else:
        # Sin carga, resetea estado
        viajando = False
        print("Sin carga: esperando...")
    
    sleep(0.5)