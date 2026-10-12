LECCIÓN 2. La casa percibe: sensores y respuesta

INTRODUCCIÓN

Hoy aprenderás a **conectar un sensor con un mecanismo: la casa “ve” si hay sol y decide si abre o cierra la ventana**. En la lección 1 el motor giraba siempre, en un bucle ciego, aunque nadie lo necesitara. Eso gasta. Una fotorresistencia (LDR) le dice a la ESP32 qué tan claro está afuera. Tú fijas un umbral: por encima hay sol y el LOZ abre la ventana para que entre luz y aire; por debajo no hay sol y el LOZ la cierra. Eso es un clasificador de una sola pregunta: ¿hay sol? No es todavía un modelo que aprenda solo, pero ya no es un temporizador sordo. El LED se enciende mientras el motor se mueve, y el motor solo actúa cuando el cielo cambia. Comprenderás cómo esta práctica contribuye al **ODS 11: Ciudades y comunidades sostenibles** y al **ODS 13: Acción por el clima**, porque una casa que aprovecha la luz del sol y se cierra cuando se va no desperdicia energía en luz artificial ni en movimientos innecesarios.

PUNTO DE PARTIDA

¿Cómo puede la casa darse cuenta de lo que pasa a su alrededor?

CONCEPTOS IMPORTANTES

**Sensor:** Es una entrada: convierte algo del mundo (luz, presión, contacto) en un número que el programa puede leer. La LDR cambia su resistencia con la claridad; la ESP32 lo ve como un valor analógico entre 0 y 4095. En una calle, una fotocélula enciende farolas; aquí abre la ventana.

**Relación sensor–acción:** No basta con medir. Hay que decidir qué hace el actuador. Cadena corta: leer → comparar → abrir o cerrar. Si omites la comparación, vuelves a la lección 1: movimiento por costumbre. En un edificio, el sensor de luz no “es” la persiana; le da la orden al motor.

**Umbral de decisión:** Es la raya que tú dibujas entre dos clases. “Más claro que esto = hay sol; más oscuro = no hay sol.” En la práctica lo ajustas tapando y destapando la LDR mientras miras la consola. Un umbral mal puesto abre la ventana de noche o la deja cerrada con sol: el sensor no falló, falló la raya.

**Clasificador (1D):** Es un modelo mínimo: un número entra, una etiqueta sale. Hoy la etiqueta es HAY SOL o NO HAY SOL, y la acción es abrir o cerrar la ventana. En las lecciones de IA ya viste umbrales de luz; aquí la salida no es un LED de semáforo, es el LOZ. Más adelante el umbral se vuelve una recta o un clustering; hoy basta una comparación.

**Actuador:** Es quien empuja el mundo: el motor, el LED, el buzzer. El sensor no mueve la ventana; el driver sí, cuando el programa se lo pide. Separar “percibir” y “actuar” evita cablear el motor directo al sensor, que sería rígido e inseguro.

**Memoria de estado:** El programa guarda si la ventana está ABIERTA o CERRADA. Así, si sigue habiendo sol, no intenta abrirla otra vez: el motor solo se mueve cuando la clase cambia.

DATO STEAM

¿Sabías que aprovechar la luz del sol que entra por las ventanas puede reducir entre un 20 % y un 60 % el uso de luz artificial durante el día? Por eso muchos edificios modernos tienen persianas y ventanas que se abren y cierran solas según la luz de afuera. Tu casa de protoboard hace lo mismo: percibe, compara con un umbral y solo entonces mueve.

HARDWARE

- 1 × ESP32 + driver del motor LOZ (ya armado en la lección 1)
- 1 × Motor LOZ (mueve la ventana)
- 1 × LED + resistencia (indicador, ya está desde la lección 1)
- 1 × LDR (fotorresistencia) + 1 × resistencia 10 kΩ (divisor de tensión)
- Cables y protoboard

CIRCUITO

- **Driver LOZ (igual que en la lección 1):**
  - IN1 → GPIO 19 (abre la ventana)
  - IN2 → GPIO 18 (cierra la ventana)
- **LED indicador:** GPIO 23 (con su resistencia) → GND
- **LDR (divisor de tensión):**
  - LDR pata 1 → 3.3 V
  - LDR pata 2 → GPIO 35
  - Resistencia 10 kΩ entre GPIO 35 y GND

ESQUEMA

Ver TB10-L2.fzz (diagrama Fritzing con ESP32, driver, motor LOZ, LED y fotorresistencia).

---

PROTOCOLO EXPERIMENTAL

1. **Carga el código** `main.py` en la ESP32 y abre la consola.
2. **Mira el número de luz** con la LDR destapada (hay sol o luz del aula) y luego tapada con la mano. Anota los dos valores.
3. **Ajusta el umbral:** pon `UMBRAL_SOL` en un número intermedio entre los dos valores que anotaste.
4. **Destapa la LDR** o apúntale con una lámpara: el LED se enciende, el LOZ gira y la ventana se abre. La consola dice “hay sol: abriendo la ventana”.
5. **Deja la LDR destapada:** la ventana no se vuelve a mover, porque ya está abierta.
6. **Tapa la LDR:** el LOZ gira al otro lado y la ventana se cierra. La consola dice “no hay sol: cerrando la ventana”.
7. **Ajusta `TIEMPO`** si la ventana no llega a abrir o cerrar por completo (o si se pasa).

---

LO QUE DEBE PASAR

- **Hay sol (luz > umbral)** → la ventana se **abre** (LOZ a la derecha, LED encendido mientras gira).
- **No hay sol (luz < umbral)** → la ventana se **cierra** (LOZ a la izquierda, LED encendido mientras gira).
- **La luz no cambia** → el motor **no se mueve**; la consola solo muestra el número de luz y el estado de la ventana.

---

CONEXIÓN CON ODS

- **ODS 11 (Ciudades y comunidades sostenibles):** Una casa que abre cuando hay sol usa luz natural en vez de luz eléctrica.
- **ODS 13 (Acción por el clima):** Menos luz artificial y menos movimientos inútiles del motor = menos energía gastada y menos emisiones.

---

DESAFÍOS OPCIONALES

1. **Umbral fino:** ¿Qué pasa si una nube tapa el sol un momento? Prueba a pasar la mano rápido sobre la LDR. ¿La ventana abre y cierra de más? Piensa cómo evitarlo.
2. **Dos umbrales:** Usa un umbral para abrir (más alto) y otro para cerrar (más bajo), para que la ventana no “tiemble” cuando la luz está justo en la raya.
3. **Aviso de mediodía:** Si la luz es muy alta (demasiado sol), haz parpadear el LED para avisar que conviene cerrar un poco por el calor.
