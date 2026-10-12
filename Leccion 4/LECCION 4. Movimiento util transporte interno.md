LECCIÓN 4. Movimiento útil: transporte interno eficiente

INTRODUCCIÓN

Hoy aprenderás a **usar el mismo motor LOZ como elevador o plataforma: un sentido sube, el otro baja, y el tiempo es la altura**. No añades otro motor; cambias el relato cinemático. Llevar un objeto de un piso a otro no es girar siempre 4 segundos: si el “piso” es bajo, un segundo basta; si es alto, necesitas más. El potenciómetro elige cuánto subir. El programa traduce ese número a un tiempo de giro: es un mapeo, la semilla de la recta que harás a mano más adelante. Una fotocélula o un umbral puede disparar el viaje para no subir vacío. Comprenderás cómo esta práctica contribuye al **ODS 11: Ciudades y comunidades sostenibles** y al **ODS 12: Producción y consumo responsables**, porque mover cosas dentro de la casa —o de un edificio— sin dosificar el recorrido es desperdicio de energía y de desgaste del mecanismo.

PUNTO DE PARTIDA

¿Cómo podemos mover objetos dentro de la casa sin desperdiciar energía?

CONCEPTOS IMPORTANTES

**Transporte interno:** Es desplazar una carga dentro del sistema, no abrir al exterior. En la práctica el LOZ sigue siendo izquierda/derecha; tú llamas a un lado “subir” y al otro “bajar”. En un almacén, la misma idea es un mini-elevador o una banda corta.

**Altura como tiempo:** Sin encoder, la ESP32 no “sabe” los centímetros. Sabe segundos de HIGH en un pin. Un viaje largo es más tiempo de motor. Por eso un tiempo fijo (lección 1) desperdicia en pisos bajos. Dosificar el tiempo es cinemática aplicada a no gastar.

**Mapeo:** Es convertir un rango en otro. El potenciómetro sale 0–4095 (o 0–100) y tú lo pasas a 1–4 segundos de subida. Aún no calculas m y b como en la recta de IA; es la misma idea en una línea: a mayor pedido, más recorrido. En la lección 7 esa línea se vuelve explícita.

**Viaje, no zumbido:** El elevador sube, para, y si toca bajar, invierte el sentido. Dejar el motor en HIGH “para que se quede arriba” no sostiene la carga y quema energía. El reposo con ambos pines en LOW es parte del diseño. En un ascensor real hay frenos; aquí el tiempo justo y el paro son tu freno de aula.

**Disparo del movimiento:** No subas en bucle eterno. Un umbral de luz o una condición de “hay que transportar” inicia el ciclo. Así el transporte es útil: hay una razón para gastar esos segundos. En logística, la cinta no corre vacía las 24 horas.

DATO STEAM

¿Sabías que en centros de distribución el mayor desperdicio no siempre es el robot “lento”, sino el que viaja de más o corre vacío? Ajustar el recorrido al pedido —tu mapeo de potenciómetro a segundos— es la misma lógica que usa un almacén para no mover torres completas cuando basta un piso. Menos movimiento inútil es menos energía y menos desgaste: ODS 11 y 12 en un protoboard.
