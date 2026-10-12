"""
PRUEBA DEL LED RGB - Lección 3 TECNIBOT-10-MECA
Este script prueba cada color y función del LED RGB sin necesidad de sensores.
Útil para verificar que el LED está funcionando correctamente antes de usar el main.py
"""

from machine import Pin, PWM
from utime import sleep

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# LED RGB (PWM en GPIO 12, 13, 14)
led_r = PWM(Pin(12))  # Rojo
led_g = PWM(Pin(13))  # Verde
led_b = PWM(Pin(14))  # Azul

# Configurar PWM (1kHz, duty 0-1023)
for pin in [led_r, led_g, led_b]:
    pin.freq(1000)
    pin.duty(0)

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def apagar():
    """Apaga todos los colores"""
    led_r.duty(0)
    led_g.duty(0)
    led_b.duty(0)

def rojo(intensidad=1023):
    """Enciende rojo a cierta intensidad (0-1023)"""
    led_r.duty(intensidad)
    led_g.duty(0)
    led_b.duty(0)

def verde(intensidad=1023):
    """Enciende verde a cierta intensidad (0-1023)"""
    led_r.duty(0)
    led_g.duty(intensidad)
    led_b.duty(0)

def azul(intensidad=1023):
    """Enciende azul a cierta intensidad (0-1023)"""
    led_r.duty(0)
    led_g.duty(0)
    led_b.duty(intensidad)

def blanco(intensidad=1023):
    """Enciende blanco (todos los colores)"""
    led_r.duty(intensidad)
    led_g.duty(intensidad)
    led_b.duty(intensidad)

def color_rgb(r, g, b):
    """Enciende un color RGB personalizado (0-1023 cada uno)"""
    led_r.duty(r)
    led_g.duty(g)
    led_b.duty(b)

def pulseo(color_func, duracion=2, ciclos=3):
    """Hace un pulseo: enciende y apaga un color suavemente"""
    print(f"Pulseo durante {duracion*ciclos}s...")
    for _ in range(ciclos):
        # Aumentar intensidad
        for i in range(0, 1024, 32):
            color_func(i)
            sleep(0.02)
        # Disminuir intensidad
        for i in range(1024, -1, -32):
            color_func(i)
            sleep(0.02)
    apagar()

def transicion(color1_func, color2_func, duracion=2):
    """Transición suave entre dos colores"""
    print(f"Transición {duracion}s...")
    pasos = 50
    for i in range(pasos):
        valor1 = int(1023 * (1 - i/pasos))
        valor2 = int(1023 * (i/pasos))
        color1_func(valor1)
        color2_func(valor2)
        sleep(duracion/pasos)
    apagar()

def arco_iris(duracion=3):
    """Ciclo de colores: rojo → verde → azul → rojo"""
    print(f"Arco iris durante {duracion}s...")
    pasos = 50
    delay = duracion / (pasos * 3)
    
    # Rojo a Verde
    for i in range(pasos):
        color_rgb(1023-int(1023*i/pasos), int(1023*i/pasos), 0)
        sleep(delay)
    
    # Verde a Azul
    for i in range(pasos):
        color_rgb(0, 1023-int(1023*i/pasos), int(1023*i/pasos))
        sleep(delay)
    
    # Azul a Rojo
    for i in range(pasos):
        color_rgb(int(1023*i/pasos), 0, 1023-int(1023*i/pasos))
        sleep(delay)
    
    apagar()

# ============================================================================
# MENÚ DE PRUEBAS
# ============================================================================

def menu():
    print("\n" + "="*60)
    print("PRUEBA DE LED RGB - Lección 3 TECNIBOT-10-MECA")
    print("="*60)
    print("\nOpciones:")
    print("1. Prueba individual de colores (rojo, verde, azul)")
    print("2. Prueba de blanco (todos los colores juntos)")
    print("3. Prueba de intensidad (dimmer: de apagado a brillante)")
    print("4. Pulseo rojo (enciende y apaga suavemente)")
    print("5. Pulseo azul")
    print("6. Transición rojo → verde")
    print("7. Transición verde → azul")
    print("8. Ciclo arco iris")
    print("9. Valores personalizados (RGB manual)")
    print("0. Salir")
    print("-"*60)

def prueba_individual():
    """Prueba cada color por 2 segundos"""
    print("\nPrueba de colores individuales:")
    print("Rojo...")
    rojo()
    sleep(2)
    print("Verde...")
    verde()
    sleep(2)
    print("Azul...")
    azul()
    sleep(2)
    print("Apagando...")
    apagar()

def prueba_intensidad():
    """De apagado a brillante y viceversa"""
    print("\nPrueba de intensidad (rojo):")
    print("Aumentando intensidad...")
    for i in range(0, 1024, 50):
        rojo(i)
        print(f"  Intensidad: {i}")
        sleep(0.1)
    
    print("Disminuyendo intensidad...")
    for i in range(1024, -1, -50):
        rojo(i)
        print(f"  Intensidad: {i}")
        sleep(0.1)
    
    apagar()

def prueba_personalizada():
    """Permite al usuario ingresar valores RGB"""
    print("\nPrueba de color personalizado:")
    try:
        r = int(input("Valor Rojo (0-1023): "))
        g = int(input("Valor Verde (0-1023): "))
        b = int(input("Valor Azul (0-1023): "))
        
        # Validar rangos
        r = max(0, min(1023, r))
        g = max(0, min(1023, g))
        b = max(0, min(1023, b))
        
        print(f"Color RGB({r}, {g}, {b}):")
        color_rgb(r, g, b)
        sleep(3)
        apagar()
    except ValueError:
        print("Error: ingresa números entre 0 y 1023")

# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\nEspera 2 segundos para que se estabilice...")
    sleep(2)
    
    while True:
        try:
            menu()
            opcion = input("Selecciona una opción (0-9): ").strip()
            
            if opcion == "1":
                prueba_individual()
            elif opcion == "2":
                print("\nPrueba de blanco (máxima intensidad):")
                blanco()
                sleep(3)
                apagar()
            elif opcion == "3":
                prueba_intensidad()
            elif opcion == "4":
                pulseo(rojo, duracion=1, ciclos=3)
            elif opcion == "5":
                pulseo(azul, duracion=1, ciclos=3)
            elif opcion == "6":
                transicion(rojo, verde, duracion=2)
            elif opcion == "7":
                transicion(verde, azul, duracion=2)
            elif opcion == "8":
                arco_iris(duracion=3)
            elif opcion == "9":
                prueba_personalizada()
            elif opcion == "0":
                print("Apagando LED...")
                apagar()
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")
        
        except KeyboardInterrupt:
            print("\n\nPrueba interrumpida por el usuario.")
            apagar()
            break
        except Exception as e:
            print(f"Error: {e}")
            apagar()

