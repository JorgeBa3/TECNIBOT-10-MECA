LECCIÓN 8. El robot barredor de la casa: K-means dirigiendo un servo

INTRODUCCIÓN

Hoy tu robot barredor deja de estar quieto: se pone sobre ruedas y recorre la casa solo, barriendo mientras avanza. El LOZ de siempre sigue haciendo lo mismo que en toda la lección — adelante y atrás — solo que ahora empuja al robot completo en vez de una puerta o un torno. Lo nuevo es un servomotor que gira las ruedas delanteras para dar dirección, como el volante de un carro. El HC-SR04 al frente sigue vigilando la distancia, y el equipo lo calibra igual que en la lección anterior: tres rondas de ejemplos que la ESP32 agrupa en tres centros — LEJOS, MEDIO y OBSTÁCULO — con K-means a mano. Con esa clasificación el robot decide cómo dirigir las ruedas: si el camino está despejado avanza derecho, si algo se acerca gira las ruedas para esquivar sin frenar, y si hay un obstáculo pegado, para, retrocede y gira fuerte antes de seguir. Comprenderás cómo esta práctica contribuye al **ODS 9: Industria, innovación e infraestructura** y al **ODS 12: Producción y consumo responsables**, porque un robot que cubre una habitación completa rebotando y decidiendo con datos, sin mapa ni cámara, es la misma idea barata detrás de una aspiradora robot real.

PUNTO DE PARTIDA

¿Cómo hace un robot para recorrer y limpiar toda una habitación sin que nadie lo esté manejando?

CONCEPTOS IMPORTANTES

**Clustering (agrupamiento):** En vez de un solo umbral fijo, el modelo agrupa distancias parecidas en tres clases: LEJOS, MEDIO, OBSTÁCULO. Es el mismo principio de la lección pasada, aplicado ahora a decidir hacia dónde giran las ruedas, no solo si abrir o cerrar algo.

**Centro (centroide):** Es el promedio de las lecturas de cada ronda de calibración. Si "OBSTÁCULO" dio 4, 5 y 3 cm, el centro es 4. El robot no memoriza los tres números sueltos, memoriza el resumen.

**Vecino más cercano:** Cada lectura nueva se compara con los tres centros y se queda con el más parecido. Es K-means en su versión más simple: un solo cálculo por lectura, sin iterar.

**Un actuador, una tarea:** El LOZ solo controla si el robot avanza o retrocede (adelante/atrás, HIGH/LOW, sin velocidades que ajustar); el servo solo controla el ángulo de las ruedas. Ninguno hace el trabajo del otro, y por eso el robot gira con precisión: el giro depende de un solo ángulo de servo, no de que dos motores arranquen igual. En una fábrica, un transportador y un brazo clasificador tampoco comparten motor: cada actuador hace una sola cosa bien.

**Secuencia, no simultaneidad:** Cuando toca girar fuerte, primero se detiene el LOZ, luego gira el servo, y solo después el LOZ vuelve a avanzar: nunca arrancan los dos a la vez. Arrancar dos actuadores en el mismo instante es lo que más corriente pide de golpe; secuenciarlos evita ese pico, la misma razón por la que un ascensor real no suelta el freno y arranca el motor exactamente al mismo tiempo.

DATO STEAM

¿Sabías que las primeras aspiradoras robot no usaban mapas ni cámaras? Su algoritmo era justo este: avanzar, y cuando el sensor de choque topaba con algo, retroceder y girar hacia un lado al azar. Con suficiente tiempo, ese "rebote con azar" termina cubriendo casi toda la habitación, sin necesitar saber en qué parte del cuarto está el robot. Hoy tu equipo construyó la misma idea, con un sensor de distancia en vez de un sensor de choque, y un servo en vez de dos motores independientes.
