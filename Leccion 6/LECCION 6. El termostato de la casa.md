LECCIÓN 6. El termostato de la casa: la recta que aprende a predecir

INTRODUCCIÓN

Hoy tu casa deja de decidir con un solo número fijo: aprende una recta a partir de ejemplos. Un giroscopio (MPU6050) mide los grados de inclinación de una vara: el equipo la coloca en 4 posiciones y dice qué temperatura representa cada una. La ESP32 ajusta `temp = m × grados + b` a mano, sin sklearn, y con esa recta predice la temperatura en posiciones nuevas de la vara que nadie le dice de antemano. Comprenderás cómo esta práctica contribuye al **ODS 7: Energía asequible y no contaminante** y al **ODS 13: Acción por el clima**, porque medir bien y predecir con pocos datos, en vez de necesitar un sensor de temperatura para cada punto, es la base de cualquier sistema que después decida cuándo climatizar sin desperdiciar.

PUNTO DE PARTIDA

¿Cómo puede una casa estimar una temperatura que no está midiendo directamente?

CONCEPTOS IMPORTANTES

**Regresión lineal:** En vez de un umbral (sí/no), la recta predice un número continuo a partir de otro. `temp = m × grados + b` convierte cualquier ángulo de la vara en una temperatura estimada, no solo "caliente o frío".

**Calibración con 4 puntos:** Cuatro pares (grados medidos por el giroscopio, temperatura dicha por el grupo) bastan para ajustar la recta con mínimos cuadrados. Menos de tres puntos no alcanza para confiar en la pendiente; con cuatro, ya se nota si el ajuste es razonable.

**Predecir vs. memorizar:** El modelo no guarda las cuatro temperaturas originales: guarda `m` y `b`. Con eso predice temperaturas en posiciones de la vara que nunca calibraste: esa es la diferencia entre una tabla y un modelo.

**Generalizar:** Probar la recta en posiciones nuevas, distintas a las cuatro calibradas, es la única forma de saber si el modelo realmente aprendió una relación y no solo repitió lo que el grupo le dictó.

DATO STEAM

¿Sabías que muchos sensores de bajo costo no miden directamente lo que reportan? Calibran una recta contra un instrumento de referencia unas pocas veces, y después esa recta hace todo el trabajo. La misma idea de "cuatro puntos y una recta" que usaste hoy es, a escala mayor, cómo empieza cualquier sistema de medición barato que necesita ser preciso.
