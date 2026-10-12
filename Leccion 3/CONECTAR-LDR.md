# Cómo conectar la LDR (Fotoresistencia)

## 🔍 ¿Qué es la LDR?

**LDR** = Light Dependent Resistor (Resistencia dependiente de luz)
- Cuando hay luz → baja resistencia (conducción alta)
- Cuando está oscuro → alta resistencia (conducción baja)
- No tiene polaridad (se conecta en cualquier sentido)

---

## 📌 Conexión: Divisor de Tensión

La LDR se conecta en **divisor de tensión** con una resistencia fija de **10kΩ**.

### Esquema:

```
     3.3V (VCC)
      |
      | (LDR)
      |
   ┌──┴──┐
   |  A  |━━━ GPIO 35 (ADC)
   └──┬──┘
      | (Resistencia 10kΩ)
      |
     GND
```

### Paso a paso:

1. **LDR pata 1** → **3.3V** (o 5V del ESP32)
2. **LDR pata 2** → **GPIO 35** (pin ADC del ESP32)
3. **Resistencia 10kΩ pata 1** → **GPIO 35** (mismo punto que LDR pata 2)
4. **Resistencia 10kΩ pata 2** → **GND** (tierra/negativo)

### Diagrama simplificado:

```
3.3V
 |
[LDR]  ← La LDR baja su resistencia con luz
 |
 +━━━━━ GPIO 35 ← Lee el voltaje aquí
 |
[10kΩ] ← Resistencia fija
 |
GND
```

---

## 💡 ¿Por qué divisor de tensión?

El ESP32 tiene **ADC** (conversor analógico-digital) que lee voltaje, no resistencia.

- **Sin luz:** LDR = alta resistencia → más voltaje en GPIO 35 → lectura alta (≈100%)
- **Con luz:** LDR = baja resistencia → menos voltaje en GPIO 35 → lectura baja (≈10%)

---

## 🔗 Tabla de conexiones (Lección 3)

| Componente | Pata 1 | Pata 2 |
|------------|--------|--------|
| **LDR** | 3.3V | GPIO 35 |
| **Resistencia 10kΩ** | GPIO 35 | GND |

---

## 📸 En el protoboard

```
Fila A:  3.3V ━━━━ [LDR arriba]
         |
         └━━━━━ [10kΩ abajo]
              |
Fila B:  GPIO 35 ━━━ [LDR abajo]
         |
         └━━━━━ [10kΩ arriba]

Fila C:  GND ━━━━ [10kΩ abajo]
```

---

## ⚙️ En el código (ya está configurado)

```python
# LDR (fotocélula para medir luz ambiental)
ldr = ADC(Pin(35))
ldr.atten(ADC.ATTN_11DB)

def leer_luz():
    """Lee valor de luz (0-100%)"""
    valor = (ldr.read() / 4095.0) * 100.0
    return valor
```

**Valores esperados:**
- **Luz brillante:** 80-100%
- **Luz normal:** 40-70%
- **Luz tenue:** 20-40%
- **Oscuridad:** 0-20%

---

## 🧪 Prueba rápida

Carga este código en MicroPython para probar la LDR:

```python
from machine import Pin, ADC
from utime import sleep

ldr = ADC(Pin(35))
ldr.atten(ADC.ATTN_11DB)

while True:
    valor = (ldr.read() / 4095.0) * 100.0
    print(f"Luz: {valor:.1f}%")
    sleep(0.5)
```

**Resultado en consola:**
```
Luz: 85.3%   ← Con luz natural
Luz: 12.5%   ← Cubre la LDR con la mano (oscuro)
Luz: 78.2%   ← Quita la mano
```

Si ves números que cambian cuando cubres/descubres la LDR: ✅ **Funcionando**

---

## ⚠️ Cosas importante

- **Resistencia correcta:** Usa **10kΩ** (no 1kΩ ni 100kΩ)
- **Sin polaridad:** La LDR se conecta en cualquier sentido
- **Puerto ADC:** Solo GPIO 35 (o 34, 39) en ESP32 de 30 pines
- **Rango:** 0-3.3V (NO 5V directo en el GPIO)

---

## 🔧 Si no funciona

| Síntoma | Causa | Solución |
|---------|-------|----------|
| Siempre lee 100% | LDR invertida o mal conectada | Verifica conexión a GPIO 35 |
| Siempre lee 0% | Falta resistencia 10kΩ | Añade la resistencia en paralelo |
| Valores raros (>100) | ADC configurado mal | Verifica `ldr.atten(ADC.ATTN_11DB)` |
| No cambia con luz | LDR quemada | Prueba con otra LDR |

