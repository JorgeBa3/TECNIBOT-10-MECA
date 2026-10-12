LECCIÓN 8. El robot barredor de la casa: ficha práctica

Descripción: el robot usa el mismo motor LOZ de siempre (adelante/atrás) para moverse, un servomotor SG90 para dirigir las ruedas delanteras, y el HC-SR04 al frente para medir distancia. El equipo calibra el sensor con 3 rondas (LEJOS, MEDIO, OBSTÁCULO); la ESP32 promedia y guarda 3 centros (K-means a mano). Después el robot avanza solo: derecho si está despejado, gira las ruedas suave si algo se acerca, y para/retrocede/gira fuerte si choca casi con algo.

Electrónica:

Materiales:
ESP32
Protoboard
Chasis con ruedas, motor LOZ con su driver, y ruedas delanteras dirigibles con servo
Servomotor SG90
HC-SR04
LED + resistencia
Batería propia para el LOZ y el servo (4 pilas AA, o LiPo/18650 con su regulador) — NO usar el 5V/3V3 de la ESP32 para ninguno de los dos
Cables jumper

Paso 1: LOZ (igual que en las lecciones anteriores).
IN1 → GPIO 18 (adelante), IN2 → GPIO 19 (atrás)

Paso 2: Servo SG90 para dirigir las ruedas.
Cable naranja (señal) → GPIO 23. Cable rojo → + de las baterías (NO el 5V del driver). Cable marrón → GND de las baterías Y GND de la ESP32 (el mismo GND que todo lo demás).

Paso 3: Alimentación — esta es la parte que suele fallar.
La batería propia alimenta el LOZ (a través de su driver) y el servo. Ninguno de los dos se conecta al pin 5V/3V3 de la ESP32: ahí no hay corriente suficiente y es la causa más común de que "cueste mover el LOZ y el servo juntos". El GND de la batería, el GND del driver del LOZ, el GND del servo y el GND de la ESP32 tienen que quedar unidos en la misma protoboard.

Paso 4: HC-SR04 al frente del chasis.
TRIG → GPIO 4, ECHO → GPIO 5, VCC → 5V, GND → GND común

Paso 5: LED de aviso.
Igual que en lecciones anteriores: LED → GPIO 26 con resistencia, GND común

Antes de armar el robot completo: prueben el servo solo con `probar_servo.py` (ya está en esta carpeta) para confirmar que gira de 0° a 180° sin que tiemble ni se reinicie la ESP32. Si tiembla, revisen el GND común antes de seguir.

Programación:
Sube main.py. En Thonny abre la consola: el programa pide calibrar antes de moverse.

Importar librerías y configurar pines:
in1/in2 para el LOZ, PWM en GPIO 23 para el servo (freq 50 Hz, igual que probar_servo.py), TRIG/ECHO para el ultrasónico, LED en GPIO 26.

Definir funciones:
distancia_cm() mide con el HC-SR04 (igual que en lecciones anteriores). angulo(g) manda el servo a un ángulo de 0° a 180° (igual que probar_servo.py). avanzar()/retroceder()/parar() controlan el LOZ. promedio_de() y vecino_mas_cercano() son las mismas de la lección anterior, aplicadas ahora a LEJOS/MEDIO/OBSTÁCULO.

# 1) Calibración: coloquen el robot en el piso, ruedas centradas (90°). Ronda 1 con el camino despejado (LEJOS), ronda 2 con algo a media distancia como un mueble (MEDIO), ronda 3 con un objeto bien pegado al sensor (OBSTÁCULO). Antes de cada ronda el programa espera Enter.

# 2) El robot arranca solo: avanza con las ruedas centradas mientras el camino está LEJOS despejado.

# 3) Cuando el sensor mide MEDIO, el servo gira las ruedas hacia un lado sin que el LOZ deje de avanzar. Cuando mide OBSTÁCULO, el LOZ para, retrocede, el servo gira las ruedas hacia un lado al azar y el LOZ avanza de nuevo en la nueva dirección. Prueben moviendo un obstáculo al frente para ver los tres comportamientos. El robot avanza a pasitos (empuja PASO segundos y descansa PAUSA segundos) para que no salga disparado: el LOZ no puede ir despacio con PWM. Si va muy rápido, suban PAUSA o bajen PASO.
