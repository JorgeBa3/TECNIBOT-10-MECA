LECCIÓN 1. Movimiento eficiente: cinemática en la casa

INTRODUCCIÓN

Hoy aprenderás a **mover una parte de la casa con un motor, midiendo el tiempo y el sentido, para no gastar energía de más**. Una puerta automática no es magia: es cinemática. El motor LOZ gira a la derecha un rato (abre), se detiene y gira a la izquierda (cierra). Tú decides cuántos segundos se mueve; cada segundo de más es electricidad que la casa no necesitaba. El driver del LOZ es quien entrega la fuerza: los pines de la ESP32 solo dicen “este lado” o “el otro”, nunca alimentan el motor solos. Comprenderás cómo esta práctica contribuye al **ODS 7: Energía asequible y no contaminante** y al **ODS 13: Acción por el clima**, porque un mecanismo que se mueve solo el tiempo justo consume menos y reduce emisiones sin que nadie esté apagando interruptores a mano.

PUNTO DE PARTIDA

¿Cómo podemos mover partes de la casa usando la menor energía posible?

CONCEPTOS IMPORTANTES

**Cinemática:** Es describir el movimiento sin inventar una historia complicada: qué tan rápido, hacia dónde y durante cuánto tiempo. En la práctica tu puerta no “sabe” que es una puerta; sabe que el motor gira 4 segundos a la derecha y 4 a la izquierda. En un elevador real se mide lo mismo: recorrido, sentido y tiempo de viaje.

**Sentido de giro:** El motor LOZ tiene dos pines en el driver: izquierda y derecha. Un pin en HIGH y el otro en LOW hace girar; los dos en LOW paran. Si los cruzas, la puerta “abre” hacia el lado contrario. En la industria, invertir el sentido es bajar la carga o devolver la cinta.

**Tiempo de actuación:** Es cuánto dejas el motor encendido. Más tiempo no significa “más inteligente”: significa más energía. En la práctica empiezas con 4 segundos fijos. Una casa eficiente corta el movimiento cuando ya llegó; no deja el motor zumbando.

**Driver del motor:** Es el circuito que convierte la orden de la ESP32 en corriente para el LOZ. El GPIO no debe ir al motor. En la práctica conectas el motor a las salidas del driver, el driver a 5 V o a lo que pida el módulo, y GND común con la ESP32. Así la fuerza no pasa por el microcontrolador.

**Energía en reposo:** Parar también es una decisión. Una puerta abierta que ya no se mueve debe tener el motor en 0. En una casa real, el modo reposo es el que más horas dura: si ahí sigues gastando, el ODS 7 se queda en el discurso.

ELECTRÓNICA: LED indicador (GPIO 23)

Además del driver del motor, esta lección suma un LED en el GPIO 23: se enciende mientras la puerta se mueve (abriendo o cerrando) y se apaga en reposo, para que el equipo vea a simple vista cuándo se está gastando energía y cuándo no. Cátodo del LED a GND (cable negro) y ánodo a GPIO 23 (cable rojo), con una resistencia limitadora en la protoboard como en las demás lecciones.

DATO STEAM

¿Sabías que en un edificio de oficinas los motores de puertas, persianas y ventilación pueden ser una fracción enorme de la factura si se dejan en marcha “por si acaso”? Los sistemas que cortan el movimiento al completar el recorrido —el mismo principio de tus 4 segundos y un paro— bajan el consumo sin cambiar el confort. Tu protoboard es esa lógica a escala de aula: sentido, tiempo, reposo.
