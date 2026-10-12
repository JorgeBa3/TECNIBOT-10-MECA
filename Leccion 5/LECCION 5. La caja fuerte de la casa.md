LECCIÓN 5. La caja fuerte de la casa: el dial de la clave

INTRODUCCIÓN

Hoy tu casa protege algo con una clave que no se escribe, se gira. No basta con medir un valor y compararlo contra un número: aquí la clave es una secuencia de 4 posiciones y tiene que coincidir exacta, en el mismo orden. La clave se marca girando un potenciómetro, un dial físico con 4 zonas (1 a 4): el sistema lee la posición del dial una vez por cada dígito de la clave, como una combinación de caja fuerte de verdad. Comprenderás cómo esta práctica contribuye al ODS 9: Industria, innovación e infraestructura y al ODS 16: Paz, justicia e instituciones sólidas, porque proteger objetos con una regla clara y sin depender de una app en la nube es tecnología accesible y también más privada.

PUNTO DE PARTIDA

¿Cómo protege sus cosas una casa sin depender de una aplicación en la nube?

CONCEPTOS IMPORTANTES

Control de acceso: Es decidir quién puede activar un mecanismo. Aquí la condición es una secuencia exacta: las 4 posiciones del dial tienen que coincidir, en orden, con la clave guardada. Si una sola posición falla, la caja no abre.

Regla exacta vs. umbral: Hay decisiones que son cuestión de grado, como qué tan claro está un ambiente. Otras no tienen grados: la clave coincide letra por letra o no coincide. Reconocer la diferencia entre ambos tipos de decisión es parte de diseñar bien un sistema de control.

Dial como sensor de intención: El potenciómetro, leído con el ADC de la ESP32, es la forma más simple de decirle una secuencia a un microcontrolador sin teclado. Su lectura (0 a 4095) se divide en 4 zonas iguales; cada zona es una "posición" de la clave, y un LED distinto para cada zona muestra en vivo dónde está el dial en ese momento. No hace falta un teclado matricial para practicar el concepto de "el usuario declara una intención y el sistema la valida".

ELECTRÓNICA: dial de clave (potenciómetro)

El potenciómetro reemplaza el teclado: su pin central (wiper) va al GPIO 34 (ADC), y los extremos a 3V3 y GND. Se suman 4 LEDs, uno por cada zona del dial (GPIO 12, 14, 27 y 33, cada uno con su resistencia limitadora): mientras el equipo gira el dial, se enciende siempre el LED de la zona en la que está en ese momento, y se apagan los otros tres, así ven en vivo qué posición está marcando el dial. El programa divide la lectura del ADC (0-4095) en 4 zonas iguales, numeradas 1 a 4. El sistema pide la clave dígito por dígito: para cada uno, da unos segundos para que el equipo gire el dial a la posición correcta (viendo el LED encendido) antes de leerla. Si las 4 posiciones leídas coinciden en orden con la clave guardada (`CLAVE = [1, 3, 2, 4]` en el código), la caja abre.

DATO STEAM

¿Sabías que las primeras cajas fuertes de combinación, de hace más de 150 años, funcionan exactamente con esta misma lógica: un dial que giras a varias posiciones exactas, en un orden exacto? No hay electrónica de por medio, solo mecánica de precisión. Hoy construiste la versión electrónica de esa misma idea con un potenciómetro y unos LEDs de menos de $1 cada uno.
