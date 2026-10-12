LECCIÓN 6. El termostato de la casa: ficha práctica

Descripción: el MPU6050 va sobre una vara que hace de "dial de temperatura". El equipo la coloca en 4 posiciones y dice qué temperatura representa cada una; la ESP32 mide los grados de inclinación y ajusta la recta. Luego colocan la vara en posiciones nuevas y el modelo predice la temperatura sin que se la digan.

Electrónica:

Materiales:
ESP32
Protoboard
MPU6050
Cables jumper
Vara o soporte donde montar el MPU6050

Paso 1: MPU6050 a la ESP32.
VCC → 3V3, GND → GND, SDA → GPIO 21, SCL → GPIO 22

Programación:
Sube main.py y mpu6050.py. En Thonny abre la consola: el programa espera Enter y las temperaturas que escribas.

Importar librerías y configurar pines:
SoftI2C con SCL en GPIO 22 y SDA en GPIO 21. N_PUNTOS = 4.

Definir funciones:
angulos() lee el acelerómetro y calcula la inclinación de la vara en los dos ejes (X e Y) con atan2, en grados; así no importa de qué lado esté pegado el MPU6050. leer_angulos() promedia 10 lecturas para que no tiemble. recta() calcula m y b con mínimos cuadrados.

# 1) Cuatro posiciones conocidas. Coloca la vara en una posición, pulsa Enter, escribe la temperatura que representa (ej. 15, 20, 25, 30 °C). Usen posiciones MUY distintas, de acostada a parada. Al final el programa elige solo el eje que más cambió y, si entre la posición más baja y la más alta hay menos de 20 grados, pide repetir la calibración (con muy poco movimiento la recta sale exagerada y predice temperaturas absurdas, como -17 °C).

# 2) Recta temp = m × grados + b. Se imprime con m y b.

# 3) Posiciones NUEVAS: coloca la vara en un ángulo que no calibraste, pulsa Enter, y la consola predice la temperatura sin que la escribas. Compara si tiene sentido con la posición.
