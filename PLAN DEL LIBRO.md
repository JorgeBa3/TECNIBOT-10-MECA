# Plan del libro — Tecnibot 10 Mecatrónica (Smart House)

Público: 4.º bachillerato, grupos de 4–5, **40 minutos**, kit TK + **motor LOZ con su driver**.
Todo el código corre en la **ESP32** (MicroPython), igual que la lección 8 de 4.º IA: sin sklearn, sin PC para entrenar, CSV solo dentro del micro cuando haga falta.

La columna de cinemática/sensores/motores se mantiene. El ML entra en **semilla** y crece: primero un umbral, luego una recta, al final clustering. No se copia el libro de IA: aquí el modelo **mueve un mecanismo**.

---

## Cómo se ve una clase (40 min)

| Min | Qué pasa |
|---|---|
| 0–5 | Punto de partida + 1 concepto (voz de estudiante, factory/casa) |
| 5–13 | Electrónica: **2 pasos de armado** (como las fichas de 4.º) |
| 13–35 | Programación en bloques: Importar / Definir / `# 1)` `# 2)` `# 3)` |
| 35–40 | Demo del grupo + 1 frase de ODS |

Roles en el grupo (rotan cada lección): protoboard, código, sensores, prueba, anotar qué pasó.

---

## Progresión de hardware (un extra por clase)

| L | Se añade | Ya está |
|---|---|---|
| 1 | ESP32 + LOZ (I=18, D=19) + LED | — |
| 2 | LDR | L1 |
| 3 | Potenciómetro | L1–2 |
| 4 | (mismo LOZ, otro “mecanismo”: elevador) | L1–3 |
| 5 | 4 LEDs de zona (uno por posición del dial) | L1–4 (potenciómetro ya está desde L3) |
| 6 | MPU6050 (giroscopio/acelerómetro) | L1–5 |
| 7 | Torno de hilos (mismo LOZ, mecanismo nuevo) | L1–6 |
| 8 | Servomotor SG90 (dirige las ruedas) + batería propia para LOZ y servo | L1–7 |

Driver LOZ: **HIGH/LOW a tope**, un pin HIGH y el otro LOW. Sin PWM suave (en 3.3 V el LOZ zumba y no gira). Velocidad en L7 = **tiempo de giro** o ráfagas, no duty bajo.

---

## Progresión de ML (lo que ya hicimos en 4.º, aplicado a mecanismos)

| L | ML (semilla) | Qué decide |
|---|---|---|
| 1 | Ninguno | El motor gira un tiempo fijo (cinemática: t, sentido) |
| 2 | **Umbral / clasificador 1D** (como L2 IA: hay luz / no hay luz) | LDR → hay sol abre la ventana, no hay sol la cierra (LOZ) |
| 3 | Dos umbrales (luz + “viento” con pot) | AND/OR: el mecanismo solo actúa si el entorno lo pide |
| 4 | Mapeo simple `pasos = f(pot)` (proto-recta) | Cuánto sube el elevador |
| 5 | Clave exacta (secuencia de 4 posiciones del dial) | El LOZ abre la caja si las 4 posiciones giradas coinciden, en orden, con la clave guardada |
| 6 | **Recta a mano** `temp = m × grados + b` (regresión lineal, como L6 IA) | Predice la temperatura desde los grados que mide el giroscopio en una vara — solo inferencia, no mueve nada |
| 7 | Regla **OR** de dos variables (luz y “lluvia” simulada) | Enrolla o despliega el tendedero (LOZ + torno de hilos) |
| 8 | **K-means a mano, 3 centros** sobre distancia (clustering, no solo umbral) | LEJOS → avanza derecho; MEDIO → gira suave sin parar; OBSTÁCULO → retrocede y gira fuerte hacia un lado al azar |

No meter visión/YOLO en este libro: ya está en otra línea y no cabe en 40 min con mecanismo.

---

## Las 8 lecciones

### 1. Movimiento eficiente: cinemática en la casa
- **Teoría:** movimiento, tiempo, sentido, fuerza (el driver, no el GPIO, empuja el motor).
- **Práctica:** puerta automática a tiempo fijo: 4 s derecha, paro, 4 s izquierda (el `probar_motor` de 5.º, con historia de casa).
- **ML:** no.
- **ODS:** 7 / 13 — ¿Cómo movemos partes de la casa con la menor energía posible?
- **Salida:** LED ON mientras gira; consola: “abriendo / cerrando”.

### 2. La casa percibe: sensores y respuesta
- **Teoría:** sensor → decisión → actuador. Fotocélula (LDR).
- **Práctica:** ventana inteligente: si hay sol (LDR > umbral) el LOZ abre la ventana; si no hay sol, la cierra. El programa recuerda si está abierta o cerrada para no mover el motor de más.
- **ML:** clasificador supervisado de un umbral (tú lo fijas, como L2 de IA).
- **ODS:** 11 / 13 — ¿Cómo se da cuenta la casa de lo que pasa alrededor?

### 3. Midiendo para decidir: variables del entorno
- **Teoría:** dos variables (luz + “viento”/pedido = pot). Medir para no actuar de más.
- **Práctica:** el LOZ solo cierra si está oscuro **y** el pot pasa un segundo umbral. El molino/tacómetro no va aquí: es la L5 de 5.º MECA.
- **ML:** regla AND; se imprimen los dos números (hábito de dato, como L5 IA).
- **ODS:** 7 / 13 — ¿Qué hay que medir para que la casa funcione mejor?

### 4. Movimiento útil: transporte interno
- **Teoría:** cinemática del elevador: un sentido = subir, el otro = bajar; el tiempo es la “altura”.
- **Práctica:** potenciómetro elige cuánto subir (map 1–4 s); botón o umbral de LDR dispara el viaje.
- **ML:** `tiempo = map(pot)` — primera función continua, aún sin llamar “recta”.
- **ODS:** 11 / 12 — ¿Cómo movemos objetos dentro de la casa sin desperdiciar energía?

### 5. La caja fuerte de la casa: el dial de la clave
- **Teoría:** no toda decisión es un umbral de sensor: a veces la casa necesita una regla exacta. Aquí la clave no se escribe, se gira: el equipo reutiliza el potenciómetro que ya armó en L3-L4 como un dial físico de 4 posiciones, y la ESP32 lo lee un dígito a la vez.
- **Práctica:** al arrancar, el sistema pide la clave dígito por dígito. Para cada uno, da unos segundos para que el equipo gire el dial a la posición correcta; mientras gira, 4 LEDs (uno por zona) muestran en vivo en qué posición está el dial. Si las 4 posiciones leídas coinciden en orden con la clave guardada, el LOZ abre la caja unos segundos y se cierra sola; si no coinciden, la consola avisa y el ciclo vuelve a empezar.
- **ML:** no es un umbral aprendido, es una regla exacta (secuencia == secuencia) — control de acceso, no clasificación.
- **ODS:** 9 / 16 — ¿Cómo protege sus cosas una casa sin depender de una app en la nube?
- **Salida:** consola imprime cada posición leída mientras se marca la clave, y al final "ABIERTO" o "CLAVE INCORRECTA"; los 4 LEDs muestran en vivo la posición del dial durante toda la captura.

### 6. El termostato de la casa
- **Teoría:** un solo número (como en L2) no basta para decidir con confianza: hay que **calibrar** con varios puntos y ajustar una recta, igual que hiciste con clustering en L8 pero ahora con una función continua. Un giroscopio (MPU6050) mide los grados de inclinación de una vara que hace de "dial de temperatura" simulado.
- **Práctica:** el grupo coloca la vara en 4 posiciones distintas y dice en voz alta qué temperatura representa cada una (p. ej. 15, 20, 25, 30 °C); la ESP32 guarda los 4 pares (grados, temperatura) y ajusta `temp = m × grados + b` a mano (mínimos cuadrados, sin sklearn). Luego, colocando la vara en posiciones nuevas, predice la temperatura según la regresión lineal hecha.
- **ML:** regresión lineal a mano — la misma técnica de "recta" que ya estaba reservada en este libro, aplicada ahora a temperatura con el giroscopio. Nota: esta es la misma técnica y el mismo sensor que la L7 de 5.º MECA (que también calibra con el MPU y solo predice, sin mover nada) — se reutiliza aquí a pedido, sin buscar diferenciarla con un actuador.
- **ODS:** 7 / 13 — ¿Cómo estima una casa una temperatura que no está midiendo directamente?
- **Salida:** consola imprime los 4 pares de calibración, la recta (m, b) y la temperatura predicha cada vez que colocas la vara en una posición nueva.

### 7. El tendedero de la casa: torno de hilos
- **Teoría:** el LOZ no siempre abre una puerta: hoy mueve un torno que enrolla o despliega un hilo, el mismo principio (HIGH/LOW a tope) aplicado a un mecanismo distinto. Dos variables independientes —luz de día (LDR) y "lluvia" simulada (potenciómetro)— decidyen juntas, pero con una regla **OR**, no AND como en L3: basta con que se cumpla una condición para proteger la ropa.
- **Práctica:** si es de noche (LDR) **o** el potenciómetro marca "lluvia" por encima de un umbral, el LOZ gira para enrollar el hilo y meter el tendedero. Si es de día y no llueve, gira al otro sentido y lo despliega. Se imprime luz y lluvia cada ciclo, igual que en L3.
- **ML:** regla OR de dos variables (distinta de la AND de L3) — mismo hábito de medir dos números antes de mover el mecanismo.
- **ODS:** 12 / 13 — ¿Cómo evitamos mojar o desperdiciar energía secando ropa que no necesitaba secadora?
- **Salida:** consola imprime luz, lluvia y si el tendedero está "AFUERA" o "ADENTRO".

### 8. El robot barredor de la casa (K-means a mano)
- **Teoría:** el robot deja de estar fijo: usa el LOZ de siempre (adelante/atrás, HIGH/LOW) para moverse, y suma un servomotor que dirige las ruedas delanteras como un volante. El grupo sigue **calibrando** el HC-SR04 igual que antes, pero ahora los 3 centros son LEJOS, MEDIO y OBSTÁCULO — la misma técnica de K-means a mano y vecino más cercano, aplicada a decidir hacia dónde giran las ruedas. Hardware nuevo: un servomotor SG90 (un solo pin PWM), alimentado con batería propia — nunca desde el 5V/3V3 de la ESP32, que es lo que suele costar al mover el LOZ y el servo a la vez.
- **Práctica:** *Calibración* (en grupo, ~2 min): 3 rondas de 3 lecturas — camino despejado (LEJOS), algo a media distancia como un mueble (MEDIO), objeto bien pegado al sensor (OBSTÁCULO) — la ESP32 promedia cada ronda y guarda 3 centros. *Robot*: cada lectura nueva se compara con los 3 centros. LEJOS → ruedas centradas, avanza derecho barriendo. MEDIO → el servo gira las ruedas hacia un lado sin que el LOZ deje de avanzar, corrigiendo el rumbo antes de chocar. OBSTÁCULO → el LOZ para, retrocede, el servo gira las ruedas fuerte hacia un lado al azar y el LOZ avanza de nuevo en la nueva dirección.
- **ML:** K-means a mano de 3 centros sobre distancia (clustering aprendido de datos, no un umbral escrito a mano) — mismo modelo que la versión anterior de L8, ahora dirigiendo un servo en vez de solo una reacción.
- **ODS:** 9 / 12 — ¿Cómo recorre y "limpia" un robot toda una habitación sin mapa ni cámara, solo con datos?
- **Salida:** consola imprime los 3 centros tras calibrar y la clase detectada en cada ciclo (“LEJOS” / “MEDIO” / “OBSTACULO”), además del lado hacia el que gira cuando esquiva o retrocede.

---

## Qué reutilizar de 4.º IA (no reescribir de cero)

- Fichas: Descripción, Electrónica (materiales + 2 pasos), Programación en `# 1)` `# 2)` `# 3)`.
- `mpu6050.py`, `distancia_cm()` con timeout, K-means a mano, HIGH/LOW del LOZ (`probar_motor.py` de 5.º).
- Voz: INTRODUCCIÓN, PUNTO DE PARTIDA, CONCEPTOS con ejemplo de casa, DATO STEAM, ODS.
- Código ~80–110 líneas.

## Qué no hacer en este libro

- Puente H / transistor al GPIO para el LOZ (el LOZ ya trae driver).
- PWM suave al LOZ en ESP32 3.3 V.
- sklearn, YOLO, gráficas en PC (rompen los 40 min y el grupo).
- Tres mecanismos distintos el mismo día (en L8: 3 LEDs + 1 LOZ + 2 sensores basta).
- Arrancar el LOZ y el servo exactamente al mismo instante (L8 primero para el LOZ, luego mueve el servo, y solo entonces vuelve a avanzar — evita el pico de corriente simultáneo que daba problemas de alimentación en versiones anteriores del armado).
- Alimentar el LOZ y el servo desde el pin 5V/3V3 de la ESP32 (L8 usa una fuente de baterías propia para los dos, con GND común; por ahí falla si cuesta moverlos juntos).

## Orden de escritura (cuando pases de plan a material)

1. L1 ficha + `probar_motor` con historia de puerta.  
2. L2 umbral LDR → LOZ.  
3. L5 MPU STOP (seguridad; se reusa en 7 y 8).  
4. L6 ultrasónico.  
5. L7 recta.  
6. L8 = L8 de IA + LOZ.  
7. L3 y L4 (rellenan medición y elevador con lo ya armado).

Así el libro es mecatrónica de verdad (el LOZ se ve desde L1) y el ML no es un capítulo pegado al final: cada clase deja una decisión un poco más inteligente que la anterior.
