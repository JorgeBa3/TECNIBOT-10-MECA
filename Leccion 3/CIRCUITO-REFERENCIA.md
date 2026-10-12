# CIRCUITO TB10-L3 - REFERENCIA PARA FRITZING

## CAMBIOS RESPECTO A LA VERSIÓN ANTERIOR

**Antes:** Puerta automatizada con dos motores LOZ (abrir/cerrar) + LDR

**Ahora:** Iluminación inteligente con LED RGB + LDR + HC-SR04

---

## COMPONENTES A USAR

1. **LED RGB (cátodo común)**
   - Pata más larga = cátodo común (se conecta a GND)
   - Patas más cortas = R (rojo), G (verde), B (azul)

2. **Resistencias 220Ω** × 3 (una por cada pata R, G, B del LED RGB)

3. **LDR + Resistencia 10kΩ** (divisor de tensión)

4. **HC-SR04 (sensor ultrasónico)**
   - 4 pines: VCC, GND, TRIG, ECHO

5. **Cables, protoboard**

---

## DISTRIBUCIÓN DE PINES

### LED RGB (con resistencias 220Ω)
```
LED RGB (cátodo común)
├─ R (rojo)       → 220Ω → GPIO 12
├─ G (verde)      → 220Ω → GPIO 13
├─ B (azul)       → 220Ω → GPIO 14
└─ Cátodo común   → GND
```

### LDR (fotorresistencia)
```
LDR + Resistencia 10kΩ
├─ LDR → 3.3V
├─ LDR + 10kΩ → GPIO 35 (ADC)
└─ 10kΩ → GND
```

### HC-SR04 (sensor ultrasónico)
```
HC-SR04
├─ VCC → 5V
├─ GND → GND
├─ TRIG → GPIO 16
└─ ECHO → GPIO 17
```

---

## INSTRUCCIONES PARA ACTUALIZAR TB10-L3.fzz EN FRITZING

1. **Abre Fritzing** y carga `TB10-L3.fzz`

2. **Elimina los componentes antiguos:**
   - Quita ambos motores LOZ (in1, in2, ambos motores)
   - Quita el potenciómetro (si lo hay)
   - Conserva: LDR + resistencia 10kΩ

3. **Añade nuevos componentes:**
   - 1 × LED RGB (búscar "RGB LED" en Fritzing)
   - 3 × Resistencia 220Ω (para las patas R, G, B)
   - 1 × HC-SR04 (búscar "ultrasonic" o "SR04" en Fritzing)

4. **Cablea según la tabla de pines arriba:**
   - GPIO 12 → LED Red (con 220Ω)
   - GPIO 13 → LED Green (con 220Ω)
   - GPIO 14 → LED Blue (con 220Ω)
   - GND → Cátodo común del LED RGB
   - GPIO 35 (ADC) → LDR (divisor de tensión con 10kΩ a GND)
   - GPIO 16 → HC-SR04 TRIG
   - GPIO 17 → HC-SR04 ECHO
   - 5V → HC-SR04 VCC
   - GND → HC-SR04 GND

5. **Guarda como TB10-L3.fzz** (reemplaza el archivo anterior)

---

## NOTAS IMPORTANTES

- El LED RGB es **visual**: los colores muestran el estado del sistema.
- El HC-SR04 mide **distancia** para detectar presencia (< 100 cm).
- La LDR mide **luz ambiental** para saber si es de noche.
- La lógica **AND** es: "Presencia + Oscuro = Luz roja"

---

## PRUEBA RÁPIDA SIN FRITZING (si no tienes acceso)

Si no quieres actualizar el .fzz ahora, el `main.py` funcionará igual. Solo asegúrate de que en la placa física:
- LED RGB en GPIO 12, 13, 14 (con resistencias)
- LDR en GPIO 35
- HC-SR04 en GPIO 16, 17, 5V, GND

