LECCIÓN 3. Midiendo para decidir: iluminación inteligente de la casa

INTRODUCCIÓN

Hoy aprenderás a **medir dos variables del entorno y actuar solo cuando ambas lo justifican**. Las luces de una casa inteligente no deben encenderse cada vez que cae una nube: necesitan saber si hay **realmente alguien dentro** y si está **realmente oscuro**. 

Lee dos sensores: una **LDR que mide luz** (¿hay luz natural?) y un **HC-SR04 que detecta movimiento/presencia** (¿hay alguien ahí?). Solo cuando está oscuro **Y** hay presencia, la luz se enciende. Si no, espera. Un LED RGB te muestra en color qué está pasando: rojo brillante cuando la luz se enciende (presencia + oscuridad), azul suave cuando hay presencia pero aún hay luz, apagado cuando nadie está o hay luz suficiente.

Comprenderás cómo esta práctica contribuye al **ODS 7: Energía asequible y no contaminante** y al **ODS 13: Acción por el clima**: una casa que solo enciende luz cuando de verdad la necesita ahorra energía real. Basura entra, basura sale: si solo mides oscuridad, la luz se enciende cada vez que pasa una nube; si solo mides presencia, se enciende de día cuando entra alguien. Dos medidas = decisiones inteligentes.

PUNTO DE PARTIDA

¿Cómo podría una casa encender sus luces automáticamente sin desperdiciar energía?

CONCEPTOS IMPORTANTES

**Variable del entorno:** Es una magnitud que cambia y que te importa para decidir. En esta lección: luz ambiental (LDR) y presencia (HC-SR04). No persigues diez números el primer día: dos ya muestran que una sola lectura no cuenta toda la historia.

**Medición:** Es repetir la lectura y mirarla, no adivinar. La consola imprime luz y presencia cada ciclo. Si no ves el número, no puedes defender por qué la luz se encendió.

**Regla AND:** Las dos condiciones deben ser ciertas. Oscuro **y** hay presencia → enciende luz. Oscuro pero sin presencia → espera. Hay presencia de día → tampoco enciende (ya hay luz suficiente). En sistemas de control, AND es "no actuar de más". OR sería más sensible y más gastador; hoy priorizas eficiencia.

**Falsa alarma:** Es actuar por un estímulo que no representa el fenómeno real. Una sombra que pasa no es noche; una mascota que cruza no garantiza que alguien quiera luz. La regla AND lo previene.

**LED RGB:** Es un diodo que emite tres colores (rojo, verde, azul) por separado. Aquí lo usamos para **mostrar el estado** del sistema en color: rojo = luz encendida (presencia + oscuridad), azul = espera (presencia pero hay luz), apagado = nadie o día claro.

**PWM (Modulación por ancho de pulso):** Es una técnica para controlar la intensidad de una luz enviando pulsos rápidos. A más ciclos "encendido" en cada período, más intensa la luz. Aquí modulamos el RGB para mostrar transiciones suaves de color.

DATO STEAM

¿Sabías que los edificios inteligentes modernos gastan 20-30% menos energía que los no automatizados? No porque apaguen más luces, sino porque **no las encienden de más**. Tu hogar inteligente, en miniatura, practica esa misma lógica: dos sensores, una regla AND, y la luz obedece.

HARDWARE

- 1 × LED RGB (cátodo común o ánodo común; usaremos común positivo aquí)
- 3 × Resistencia 220Ω (una por cada pata del LED: rojo, verde, azul)
- 1 × LDR (fotorresistencia) + 1 × Resistencia 10kΩ (divisor de tensión)
- 1 × HC-SR04 (sensor ultrasónico de presencia)
- Cables, protoboard, placa ESP32 o similar

CIRCUITO

- **LED RGB (cátodo común):**
  - Pata R (rojo) → GPIO 12 (con resistencia 220Ω)
  - Pata G (verde) → GPIO 13 (con resistencia 220Ω)
  - Pata B (azul) → GPIO 14 (con resistencia 220Ω)
  - Pata común (GND) → GND

- **LDR:**
  - ADC pin 35 (mismo que en lecciones anteriores)

- **HC-SR04:**
  - TRIG → GPIO 16
  - ECHO → GPIO 17
  - VCC → 5V, GND → GND

ESQUEMA

Ver TB10-L3.fzz (diagrama Fritzing con cableado detallado).

---

PROTOCOLO EXPERIMENTAL

1. **Carga el código** `main.py` en la placa.
2. **Abre la consola** para ver luz y distancia cada 300ms.
3. **Prueba en luz natural:** LED apagado, consola muestra luz alta.
4. **Oscurece lentamente** (tapa la LDR con la mano): LED sigue apagado porque no hay movimiento.
5. **Mueve la mano** frente al HC-SR04: LED se enciende en rojo brillante (presencia + oscuridad).
6. **Deja de moverte:** LED se apaga después de ~2 segundos sin detección (espera de seguridad).
7. **Vuelve a luz natural:** LED vuelve a azul suave (presencia detectada pero luz suficiente).

---

LO QUE DEBE PASAR

- **Presencia + Oscuro** → LED **Rojo brillante** (luz encendida, consume energía porque la necesita)
- **Presencia + Luz** → LED **Azul suave** (presencia detectada, pero día claro; luz innecesaria)
- **Sin presencia + Oscuro** → LED **Apagado** (no hay quién, no enciendas)
- **Sin presencia + Luz** → LED **Apagado** (día claro y nadie; nada que hacer)

El color del LED **es el estado del sistema en tiempo real**. No necesitas consola para saber si la lógica está funcionando: simplemente mira el color.

---

CONEXIÓN CON ODS

- **ODS 7 (Energía asequible y no contaminante):** Tu sistema evita encender luces de más. En un edificio de oficinas, si 100 oficinas hacen esto, el ahorro anual en consumo es notable.
- **ODS 13 (Acción por el clima):** Menos consumo eléctrico = menos emisiones de carbono en la generación de esa energía.

---

DESAFÍOS OPCIONALES

1. **Regulador de sensibilidad:** Cambia los umbrales (UMBRAL_LUZ, RANGO_DISTANCIA) y observa cómo cambia el comportamiento. ¿A qué distancia empieza a detectar? ¿Qué tan oscuro tiene que estar?
2. **Temporización:** Añade un `timeout` después de la última detección. Si no hay movimiento durante 30 segundos, apaga la luz aunque tecnicamente haya oscuridad. (Mejora de eficiencia.)
3. **Color graduado:** En lugar de solo rojo/azul, intenta una **transición de color** basada en la distancia: azul (lejos) → cian (medio) → rojo (cerca).
4. **Dos zonas:** Usa dos HC-SR04 en dos GPIO distintos y dos RGB en otros GPIO. Cada zona se enciende independientemente según su sensor de presencia. (Extensión de la maqueta.)

---

PROTOCOLO DE MEDICIÓN Y DATOS

Abre la consola y guarda el resultado de 30 segundos mientras pruebas. Deberías ver líneas como:

```
luz=85.3 distancia=250 (cm) → LED azul (presencia, pero hay luz)
luz=15.2 distancia=15 (cm) → LED rojo (oscuro + cercano, luz encendida)
luz=92.1 distancia=999 (cm) → LED apagado (luz y sin presencia)
```

Este es el tipo de dato que después vas a usar para entrenar modelos en IA: pares de lecturas reales del mundo, con acciones asociadas. Aquí el "modelo" es una regla simple (AND); después será K-means, rectas o redes neuronales.

