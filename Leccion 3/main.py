from machine import Pin, ADC, PWM, time_pulse_us
from utime import sleep, ticks_ms

# ============================================================================
# CONFIGURACIÓN DE PINES
# ============================================================================

# LED RGB (PWM para controlar intensidad)
# NOTA: ÁNODO COMÚN - lógica inversa
led_r = PWM(Pin(12))  # Rojo
led_g = PWM(Pin(13))  # Verde
led_b = PWM(Pin(14))  # Azul

# Configurar PWM (frecuencia y resolución)
for pin in [led_r, led_g, led_b]:
    pin.freq(1000)  # 1kHz
    pin.duty(1023)  # Comienza apagado (ánodo común)

# LDR (fotocélula para medir luz ambiental)
ldr = ADC(Pin(35))
ldr.atten(ADC.ATTN_11DB)

# HC-SR04 (sensor ultrasónico)
trig = Pin(16, Pin.OUT)
echo = Pin(17, Pin.IN)
trig.off()

# ============================================================================
# UMBRALES Y CONFIGURACIÓN
# ============================================================================

UMBRAL_LUZ = 30           # Por debajo = oscuro (ajusta mirando consola)
RANGO_DISTANCIA = 100    # Detecta presencia dentro de 100 cm
TIMEOUT_PRESENCIA = 2000 # ms: mantiene luz 2 segundos sin detección

# Estado
ultima_presencia_ms = 0
luz_encendida = False

# ============================================================================
# FUNCIONES DE LECTURA
# ============================================================================

def leer_luz():
    """Lee valor de luz (0-100%)"""
    valor = (ldr.read() / 4095.0) * 100.0
    return valor

def leer_distancia():
    """Lee distancia en cm usando HC-SR04"""
    # Enviar pulso
    trig.on()
    sleep(0.00001)  # 10 microsegundos
    trig.off()
    
    # Medir tiempo del eco
    try:
        duracion = time_pulse_us(echo, 1, 30000)  # Máx 30ms
        if duracion < 0:
            return 999  # Sin respuesta
        # Velocidad del sonido: 343 m/s = 0.0343 cm/us
        # Distancia = duracion * 0.0343 / 2 (ida y vuelta)
        distancia = (duracion * 0.0343) / 2
        return distancia
    except:
        return 999  # Error en lectura

def hay_presencia(distancia):
    """Determina si hay presencia basado en distancia"""
    return distancia <= RANGO_DISTANCIA

def apagar_rgb():
    """Apaga todos los colores (ánodo común = duty alto)"""
    led_r.duty(1023)
    led_g.duty(1023)
    led_b.duty(1023)

def led_rojo_brillante():
    """LED rojo brillante (luz encendida) - ánodo común
    Estado: Presencia + Oscuro"""
    led_r.duty(1023 - 1023)  # Invertir: duty(0) = máxima intensidad rojo
    led_g.duty(1023 - 0)     # Invertir: duty(1023) = apagado
    led_b.duty(1023 - 0)     # Invertir: duty(1023) = apagado

def led_azul_fuerte():
    """LED azul fuerte (presencia pero hay luz) - ánodo común
    Estado: Presencia + Luz"""
    led_r.duty(1023 - 0)     # Invertir: duty(1023) = apagado
    led_g.duty(1023 - 0)     # Invertir: duty(1023) = apagado
    led_b.duty(1023 - 1023)  # Invertir: duty(0) = máxima intensidad azul

def led_verde():
    """LED verde (hay luz pero sin presencia) - ánodo común
    Estado: Sin presencia + Luz"""
    led_r.duty(1023 - 0)     # Invertir: duty(1023) = apagado
    led_g.duty(1023 - 1023)  # Invertir: duty(0) = máxima intensidad verde
    led_b.duty(1023 - 0)     # Invertir: duty(1023) = apagado

# ============================================================================
# LÓGICA PRINCIPAL
# ============================================================================

print("LECCIÓN 3: Iluminación inteligente de la casa")
print("LDR + HC-SR04 + LED RGB (ÁNODO COMÚN)")
print("=" * 50)
print("Colores:")
print("  🔴 Rojo    = Presencia + Oscuro (luz encendida)")
print("  🔵 Azul    = Presencia + Luz (hay presencia)")
print("  🟢 Verde   = Sin presencia + Luz (seguro)")
print("  ⚫ Apagado = Sin presencia + Oscuro")
print("-" * 50)

while True:
    # Leer sensores
    luz = leer_luz()
    distancia = leer_distancia()
    
    # Detectar presencia
    presencia = hay_presencia(distancia)
    
    # Lógica AND: Oscuro Y Presencia
    oscuro = luz < UMBRAL_LUZ
    
    # Imprimir estado
    estado = "PRESENCIA" if presencia else "SIN PRESENCIA"
    condicion_luz = "OSCURO" if oscuro else "LUZ"
    print(f"luz={luz:.1f}% | distancia={distancia:.0f}cm | {estado} | {condicion_luz}")
    
    # Lógica de control con 4 estados
    if presencia:
        # Hay presencia: actualizar timestamp
        ultima_presencia_ms = ticks_ms()
        
        if oscuro:
            # Presencia + Oscuro = ENCIENDE LUZ (LED ROJO)
            if not luz_encendida:
                print("  → 🔴 ROJO: presencia + oscuro (luz encendida)")
                luz_encendida = True
            led_rojo_brillante()
        else:
            # Presencia pero hay luz = AZUL FUERTE
            print("  → 🔵 AZUL: presencia + luz (hay alguien)")
            led_azul_fuerte()
            luz_encendida = False
    else:
        # Sin presencia actual: verificar timeout
        tiempo_sin_presencia = ticks_ms() - ultima_presencia_ms
        
        if tiempo_sin_presencia < TIMEOUT_PRESENCIA and luz_encendida:
            # Mantener luz roja por timeout (gracia de 2 segundos)
            led_rojo_brillante()
        else:
            # Sin presencia y fuera de timeout
            if luz_encendida:
                print("  → Luz apagada (timeout)")
                luz_encendida = False
            
            if oscuro:
                # Sin presencia + Oscuro = APAGADO
                print("  → ⚫ APAGADO: sin presencia + oscuro")
                apagar_rgb()
            else:
                # Sin presencia + Luz = VERDE
                print("  → 🟢 VERDE: sin presencia + luz (seguro)")
                led_verde()
    
    # Pausa antes de siguiente lectura
    sleep(0.3)
