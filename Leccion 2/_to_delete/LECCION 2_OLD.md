LECCIÓN 2. La casa percibe: sensores y respuesta

INTRODUCCIÓN

Hoy aprenderás a **conectar un sensor con un mecanismo: la casa “ve” luz y decide si mueve la puerta**. Hasta ahora el motor giraba siempre, en un bucle ciego. Eso gasta. Una fotocélula (LDR) le dice a la ESP32 qué tan claro está el entorno. Tú fijas un umbral: por encima es de día y no vale la pena cerrar; por debajo es de noche y el LOZ cierra. Eso es un clasificador de una sola pregunta: ¿hay luz suficiente? No es todavía un modelo que aprenda solo, pero ya no es un temporizador sordo. El LED puede mostrar el modo (día o noche) mientras el motor solo actúa cuando hace falta. Comprenderás cómo esta práctica contribuye al **ODS 11: Ciudades y comunidades sostenibles** y al **ODS 13: Acción por el clima**, porque una ciudad que apaga o cierra según lo que pasa afuera no desperdicia movimiento ni luz, y reduce el impacto de sistemas que de otro modo correrían las 24 horas.

PUNTO DE PARTIDA

¿Cómo puede la casa darse cuenta de lo que pasa a su alrededor?

CONCEPTOS IMPORTANTES

**Sensor:** Es una entrada: convierte algo del mundo (luz, presión, contacto) en un número que el programa puede leer. En la práctica la LDR cambia su resistencia con la claridad; la ESP32 lo ve como un valor analógico. En una calle, una fotocélula enciende farolas; aquí cierra la puerta.

**Relación sensor–acción:** No basta con medir. Hay que decidir qué hace el actuador. Cadena corta: leer → comparar → girar o parar. Si omites la comparación, vuelves a la lección 1: movimiento por costumbre. En una planta, el sensor de presencia no “es” la puerta; dispara el motor.

**Umbral de decisión:** Es la raya que tú dibujas entre dos clases. “Más claro que esto = día; más oscuro = noche.” En la práctica lo ajustas tapando y destapando la LDR. Un umbral mal puesto cierra de día o deja abierta de noche: el sensor no falló, falló la raya.

**Clasificador (1D):** Es un modelo mínimo: un número entra, una etiqueta sale. Hoy la etiqueta es DÍA o NOCHE y la acción es no gastar o cerrar. En las lecciones de IA ya viste umbrales de luz; aquí la salida no es un LED de semáforo, es el LOZ. Más adelante el umbral se vuelve una recta o un clustering; hoy basta una comparación.

**Actuador:** Es quien empuja el mundo: el motor, el LED, el buzzer. El sensor no mueve la puerta; el driver sí, cuando el programa se lo pide. Separar “percibir” y “actuar” evita cablear el motor directo al sensor, que sería rígido e inseguro.

DATO STEAM

¿Sabías que los semáforos y las luminarias de muchas ciudades usan exactamente esta idea? Un clasificador de luz (día/noche) evita encender de más y puede recortar cerca de un quinto del consumo de alumbrado si se combina con otros sensores. Tu casa de protoboard hace lo mismo: percibe, compara con un umbral y solo entonces mueve.
