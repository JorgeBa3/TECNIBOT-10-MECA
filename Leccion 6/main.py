from machine import Pin, SoftI2C
from mpu6050 import MPU6050
from utime import sleep
import math

# Importar librerías y configurar pines
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
print("I2C scan:", i2c.scan())
mpu = MPU6050(i2c)

N_PUNTOS = 4
RANGO_MINIMO = 20     # grados: entre la posición más baja y la más alta de la vara

# Definir funciones
def angulos():
    # Inclinación de la vara en los DOS ejes (X e Y), en grados.
    # Así da igual cómo esté pegado el MPU6050: uno de los dos sí va a cambiar.
    ax, ay, az, gx, gy, gz = mpu.leer()
    ang_x = math.atan2(ax, math.sqrt(ay * ay + az * az)) * 180 / math.pi
    ang_y = math.atan2(ay, math.sqrt(ax * ax + az * az)) * 180 / math.pi
    return ang_x, ang_y

def leer_angulos():
    # Promedia 10 lecturas para que el número no tiemble
    sx = 0.0
    sy = 0.0
    for _ in range(10):
        a, b = angulos()
        sx += a
        sy += b
        sleep(0.05)
    return sx / 10, sy / 10

def recta(datos):
    n = len(datos)
    sx = sum(p[0] for p in datos)
    sy = sum(p[1] for p in datos)
    den = n * sum(p[0] * p[0] for p in datos) - sx * sx
    if den == 0:
        return 0.0, sy / n
    m = (n * sum(p[0] * p[1] for p in datos) - sx * sy) / den
    return m, (sy - m * sx) / n

# 1) Calibración: el grupo coloca la vara en 4 posiciones MUY distintas
#    (de acostada a parada) y dice qué temperatura representa cada una.
#    La ESP32 mide la inclinación en los dos ejes y se queda con el que más cambió.
print("=== TERMOSTATO: calibración con giroscopio ===")
while True:
    print("Coloca la vara en", N_PUNTOS, "posiciones MUY distintas (de acostada a parada).")
    medidas = []
    for i in range(N_PUNTOS):
        print("Posición", i + 1, "de", N_PUNTOS, "- coloca la vara y pulsa Enter")
        input()
        gx_, gy_ = leer_angulos()
        print("grados X=", round(gx_, 1), " grados Y=", round(gy_, 1))
        t = float(input("Temperatura que representa (°C): "))
        medidas.append((gx_, gy_, t))

    rango_x = max(p[0] for p in medidas) - min(p[0] for p in medidas)
    rango_y = max(p[1] for p in medidas) - min(p[1] for p in medidas)
    if rango_x >= rango_y:
        EJE = 0
        rango = rango_x
    else:
        EJE = 1
        rango = rango_y
    print("La vara se movió", round(rango, 1), "grados en el eje", "XY"[EJE])

    if rango >= RANGO_MINIMO:
        break
    print("¡Muy poco movimiento! Inclina más la vara entre una posición y otra.")
    print("Repetimos la calibración.\n")

datos = [(p[EJE], p[2]) for p in medidas]
for g, t in datos:
    print("guardado:", round(g, 1), "grados ->", t, "°C")
G_MIN = min(p[0] for p in datos)
G_MAX = max(p[0] for p in datos)

# 2) Ajustar la recta temp = m * grados + b con los 4 pares (mínimos cuadrados, a mano)
m, b = recta(datos)
print("Recta: temp = {:.3f} * grados + {:.2f}".format(m, b))

# 3) Inferencia: coloca la vara en posiciones NUEVAS (que no calibraste) y el
#    modelo predice la temperatura sin que tú se la digas.
print("=== Ahora coloca la vara en posiciones NUEVAS ===")
while True:
    print("Coloca la vara en una posición nueva y pulsa Enter")
    input()
    g = leer_angulos()[EJE]
    pred = m * g + b
    print("grados=", round(g, 1), " -> temperatura predicha=", round(pred, 1), "°C")
    if g < G_MIN - 5 or g > G_MAX + 5:
        print("  ojo: esta posición está fuera de lo que calibraste; la recta está adivinando más allá de sus datos")
