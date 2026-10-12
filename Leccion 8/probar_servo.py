from machine import Pin, PWM
from utime import sleep

# SG90: naranja → GPIO 23. Rojo → + de las 4 AA (no el 5V del driver).
# Marrón → GND de las baterías Y GND de la ESP32 (el mismo).
servo = PWM(Pin(23))
servo.freq(50)

def angulo(g):
    # 0° ≈ 0.5 ms, 90° ≈ 1.5 ms, 180° ≈ 2.5 ms  (duty 0–1023)
    us = 500 + (g / 180.0) * 2000
    d = int(us / 20000.0 * 1023)
    if d < 26:
        d = 26
    if d > 128:
        d = 128
    servo.duty(d)
    print("grados=", g, "duty=", d)

print("Prueba SG90 GPIO 23  (GND comun + baterias al rojo)")
sleep(1)

while True:
    for g in (0, 45, 90, 135, 180, 90):
        angulo(g)
        sleep(1.5)
