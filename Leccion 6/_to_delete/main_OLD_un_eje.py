    from machine import Pin, SoftI2C
    from mpu6050 import MPU6050
    from utime import sleep
    import math

    # Importar librerías y configurar pines
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
    print("I2C scan:", i2c.scan())
    mpu = MPU6050(i2c)

    N_PUNTOS = 4

    # Definir funciones
    def grados():
        ax, ay, az, gx, gy, gz = mpu.leer()
        return math.atan2(ax, az) * 180 / math.pi   # ángulo de inclinación de la vara, en grados

    def leer_grados():
        s = 0.0
        for _ in range(8):
            s += grados()
            sleep(0.05)
        return s / 8.0

    def recta(datos):
        n = len(datos)
        sx = sum(p[0] for p in datos)
        sy = sum(p[1] for p in datos)
        den = n * sum(p[0] * p[0] for p in datos) - sx * sx
        if den == 0:
            return 0.0, sy / n
        m = (n * sum(p[0] * p[1] for p in datos) - sx * sy) / den
        return m, (sy - m * sx) / n

    # 1) Calibración: el grupo coloca la vara (con el MPU6050) en 4 posiciones y dice
    #    en voz alta qué temperatura representa cada una. La ESP32 mide los grados de
    #    inclinación y guarda los 4 pares (grados, temp).
    print("=== TERMOSTATO: calibración con giroscopio ===")
    print("Coloca la vara en", N_PUNTOS, "posiciones distintas.")
    datos = []
    for i in range(N_PUNTOS):
        print("Posición", i + 1, "de", N_PUNTOS, "- coloca la vara y pulsa Enter")
        input()
        g = leer_grados()
        print("grados=", round(g, 1))
        t = float(input("Temperatura que representa (°C): "))
        datos.append((g, t))
        print("guardado:", round(g, 1), "->", t, "°C")

    # 2) Ajustar la recta temp = m * grados + b con los 4 pares (mínimos cuadrados, a mano)
    m, b = recta(datos)
    print("Recta: temp = {:.5f} * grados + {:.2f}".format(m, b))

    # 3) Inferencia: coloca la vara en posiciones NUEVAS (que no calibraste) y el
    #    modelo predice la temperatura sin que tú se la digas.
    print("=== Ahora coloca la vara en posiciones NUEVAS ===")
    while True:
        print("Coloca la vara en una posición nueva y pulsa Enter")
        input()
        g = leer_grados()
        pred = m * g + b
        print("grados=", round(g, 1), " -> temperatura predicha=", round(pred, 1), "°C")
