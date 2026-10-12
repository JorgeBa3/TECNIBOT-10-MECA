# LED RGB: Ánodo Común vs Cátodo Común

## 🔍 ¿Cuál tienes?

### **Cátodo Común** (lo original en CIRCUITO-REFERENCIA.md)
```
LED RGB con CÁTODO COMÚN
├─ Pata más larga (más larga) = CÁTODO COMÚN → GND (tierra)
├─ Patas más cortas = R, G, B (los colores)
└─ Los colores van a GPIO con resistencias 220Ω → 3.3V/5V
```

### **Ánodo Común** (tu caso)
```
LED RGB con ÁNODO COMÚN
├─ Pata más larga (más larga) = ÁNODO COMÚN → 3.3V o 5V
├─ Patas más cortas = R, G, B (los colores)
└─ Los colores van a GND a través de GPIO + resistencias 220Ω
```

---

## 📌 Cableado para Ánodo Común

### Conexión física:
```
LED RGB (ánodo común)
├─ Pata + (ánodo común) → 3.3V o 5V (máquina VCC)
├─ Pata R (rojo)       → 220Ω → GPIO 12
├─ Pata G (verde)      → 220Ω → GPIO 13
└─ Pata B (azul)       → 220Ω → GPIO 14

GPIO 12, 13, 14 → GND (cuando el LED está encendido en ese color)
```

**Es lo opuesto al cátodo común.**

---

## 💻 Diferencia en el código

### **CÁTODO COMÚN** (original)
```python
def rojo():
    led_r.duty(1023)   # Encendido = duty alto
    led_g.duty(0)
    led_b.duty(0)
```

### **ÁNODO COMÚN** (tu caso) ← INVERTIR
```python
def rojo():
    led_r.duty(1023 - 1023)  # = duty(0)   ← INVERTIR
    led_g.duty(1023)         # = duty(1023)
    led_b.duty(1023)         # = duty(1023)
```

**Regla simple:** Para ánodo común, invierte todos los valores:
```python
duty_invertido = 1023 - duty_original
```

---

## ✅ Archivo a usar

**Para ánodo común, usa:**
```
probar_led_rgb_ANODO.py
```

**Para cátodo común (original), usa:**
```
probar_led_rgb.py
```

---

## 🚀 Cómo actualizar main.py para ánodo común

En **main.py**, solo necesitas cambiar tres funciones:

### Función 1: `leer_luz()` y `leer_distancia()` - SIN CAMBIOS ✓

### Función 2: Cambiar las funciones de color

**ANTES (cátodo común):**
```python
def led_rojo_brillante():
    led_r.duty(1023)
    led_g.duty(0)
    led_b.duty(0)

def led_azul_suave():
    led_r.duty(0)
    led_g.duty(0)
    led_b.duty(300)
```

**DESPUÉS (ánodo común):**
```python
def led_rojo_brillante():
    led_r.duty(1023 - 1023)  # duty(0)
    led_g.duty(1023 - 0)     # duty(1023)
    led_b.duty(1023 - 0)     # duty(1023)

def led_azul_suave():
    led_r.duty(1023 - 0)     # duty(1023)
    led_g.duty(1023 - 0)     # duty(1023)
    led_b.duty(1023 - 300)   # duty(723)
```

O más simple:
```python
def led_rojo_brillante():
    led_r.duty(0)            # Invertido: 1023-1023=0
    led_g.duty(1023)         # Invertido: 1023-0=1023
    led_b.duty(1023)         # Invertido: 1023-0=1023

def led_azul_suave():
    led_r.duty(1023)         # Invertido: 1023-0=1023
    led_g.duty(1023)         # Invertido: 1023-0=1023
    led_b.duty(723)          # Invertido: 1023-300=723
```

---

## 📊 Tabla de referencia rápida

| Tipo | Común conectado a | duty(0) = | duty(1023) = |
|------|------------------|-----------|--------------|
| **Cátodo común** | GND | Máxima intensidad (encendido) | Apagado |
| **Ánodo común** | VCC (3.3V/5V) | Apagado | Máxima intensidad (encendido) |

---

## 🧪 Prueba rápida

1. Usa `probar_led_rgb_ANODO.py` para verificar que funciona
2. Si los colores salen bien, tu LED es ánodo común ✓
3. Si salen invertidos, quizás sea cátodo común (usa `probar_led_rgb.py`)

