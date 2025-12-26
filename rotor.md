# Tutorial de Manim - Campos Vectoriales Rotacionales

Este documento contiene ejemplos de código Manim para visualizar campos vectoriales rotacionales (rotacional o curl) con diferentes estilos y animaciones.

---

## 1. Campo Rotacional Básico

Visualización básica de un campo vectorial rotacional con círculos concéntricos y flechas estáticas.

```python
from manim import *
import numpy as np

class CampoRotacional(Scene):
    def construct(self):
        
        # -------------------- TÍTULO --------------------
        title = MathTex(r"\text{rot}\,\vec{F}", font_size=80, color=YELLOW).move_to(ORIGIN)
        
        # -------------------- CÍRCULOS CONCÉNTRICOS --------------------
        circles = VGroup()
        radii = [0.8, 1.6, 2.4, 3.2, 4.0, 4.8]
        
        for r in radii:
            circle = Circle(radius=r, color=GREY, stroke_width=1, stroke_opacity=0.3)
            circles.add(circle)
        
        # -------------------- FLECHAS ESTÁTICAS --------------------
        static_arrows = VGroup()
        
        # Crear flechas en cuadrícula
        x_range = np.arange(-6, 6.5, 0.4)
        y_range = np.arange(-3.5, 4, 0.4)
        
        for x in x_range:
            for y in y_range:
                position = np.array([x, y, 0])
                distance = np.linalg.norm(position)
                
                if distance > 0.5:  # Evitar el centro
                    # Campo rotacional: perpendicular al radio
                    direction = np.array([-y, x, 0])
                    direction = direction / np.linalg.norm(direction)
                    
                    # Longitud de la flecha constante
                    arrow_length = 0.25
                    end_point = position + direction * arrow_length
                    
                    arrow = Arrow(
                        start=position,
                        end=end_point,
                        color=RED,
                        buff=0,
                        stroke_width=2,
                        max_tip_length_to_length_ratio=0.25,
                        max_stroke_width_to_length_ratio=5
                    )
                    
                    static_arrows.add(arrow)
        
        # -------------------- FLECHAS GRANDES ROTATORIAS --------------------
        rotating_arrows = VGroup()
        
        # Crear flechas más largas en posiciones específicas sobre los círculos
        num_arrows_per_circle = [6, 8, 10, 12, 14, 16]
        
        for i, r in enumerate(radii):
            n_arrows = num_arrows_per_circle[i]
            for j in range(n_arrows):
                angle = TAU * j / n_arrows
                position = np.array([r * np.cos(angle), r * np.sin(angle), 0])
                
                # Dirección tangencial (perpendicular al radio)
                direction = np.array([-np.sin(angle), np.cos(angle), 0])
                
                # Flecha más larga
                arrow_length = 0.5
                end_point = position + direction * arrow_length
                
                arrow = Arrow(
                    start=position,
                    end=end_point,
                    color=YELLOW,
                    buff=0,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.2,
                    max_stroke_width_to_length_ratio=6
                )
                
                rotating_arrows.add(arrow)
        
        # -------------------- ANIMACIÓN --------------------
        self.camera.background_color = BLACK
        
        # Mostrar título
        self.play(Write(title))
        self.wait(1)
        
        # Fade out título y mostrar círculos
        self.play(
            FadeOut(title),
            LaggedStart(*[Create(circle) for circle in circles], lag_ratio=0.1),
            run_time=2
        )
        
        # Mostrar flechas estáticas
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in static_arrows], lag_ratio=0.003),
            run_time=3
        )
        self.wait(0.5)
        
        # Mostrar título nuevamente en el centro
        title_center = MathTex(r"\text{rot}\,\vec{F}", font_size=80, color=YELLOW).move_to(ORIGIN)
        self.play(Write(title_center))
        
        # Mostrar flechas rotatorias amarillas
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in rotating_arrows], lag_ratio=0.02),
            run_time=2
        )
        self.wait(1)
        
        # Rotar las flechas amarillas
        self.play(
            Rotate(rotating_arrows, angle=TAU, about_point=ORIGIN, rate_func=linear),
            run_time=4
        )
        
        # Continuar rotando
        self.play(
            Rotate(rotating_arrows, angle=TAU, about_point=ORIGIN, rate_func=linear),
            run_time=4
        )
        
        self.wait(2)
        
        # Fade out
        self.play(
            FadeOut(static_arrows),
            FadeOut(rotating_arrows),
            FadeOut(circles),
            FadeOut(title_center)
        )
```
<p align="center"><img src ="vidios_gifs/CampoRotacional_ManimCE_v0.19.1.gif" /></p>

**Características:**
- **Campo vectorial rotacional**: Las flechas son perpendiculares al vector de posición
- **Dirección del campo**: `(-y, x, 0)` crea rotación antihoraria
- **Dos capas de flechas**: 
  - Flechas rojas estáticas (campo completo en cuadrícula)
  - Flechas amarillas rotatorias (sobre círculos concéntricos)
- **Animación por etapas**: título → círculos → flechas estáticas → flechas rotatorias
- **Rotación explícita**: Usa `Rotate()` para animar el movimiento circular

---

## 2. Campo Rotacional con Rotación Continua

Misma visualización pero con rotación continua usando `updater`.

```python
class CampoRotacionalContinuo(Scene):
    def construct(self):
        
        # -------------------- TÍTULO --------------------
        title = MathTex(r"\text{rot}\,\vec{F}", font_size=80, color=YELLOW).move_to(ORIGIN)
        
        # -------------------- CÍRCULOS CONCÉNTRICOS --------------------
        circles = VGroup()
        radii = [0.8, 1.6, 2.4, 3.2, 4.0, 4.8]
        
        for r in radii:
            circle = Circle(radius=r, color=GREY, stroke_width=1, stroke_opacity=0.3)
            circles.add(circle)
        
        # -------------------- FLECHAS ESTÁTICAS --------------------
        static_arrows = VGroup()
        
        x_range = np.arange(-6, 6.5, 0.4)
        y_range = np.arange(-3.5, 4, 0.4)
        
        for x in x_range:
            for y in y_range:
                position = np.array([x, y, 0])
                distance = np.linalg.norm(position)
                
                if distance > 0.5:
                    direction = np.array([-y, x, 0])
                    direction = direction / np.linalg.norm(direction)
                    
                    arrow_length = 0.25
                    end_point = position + direction * arrow_length
                    
                    arrow = Arrow(
                        start=position,
                        end=end_point,
                        color=RED,
                        buff=0,
                        stroke_width=2,
                        max_tip_length_to_length_ratio=0.25,
                        max_stroke_width_to_length_ratio=5
                    )
                    
                    static_arrows.add(arrow)
        
        # -------------------- FLECHAS GRANDES ROTATORIAS --------------------
        rotating_arrows = VGroup()
        
        num_arrows_per_circle = [6, 8, 10, 12, 14, 16]
        
        for i, r in enumerate(radii):
            n_arrows = num_arrows_per_circle[i]
            for j in range(n_arrows):
                angle = TAU * j / n_arrows
                position = np.array([r * np.cos(angle), r * np.sin(angle), 0])
                direction = np.array([-np.sin(angle), np.cos(angle), 0])
                
                arrow_length = 0.5
                end_point = position + direction * arrow_length
                
                arrow = Arrow(
                    start=position,
                    end=end_point,
                    color=YELLOW,
                    buff=0,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.2,
                    max_stroke_width_to_length_ratio=6
                )
                
                rotating_arrows.add(arrow)
        
        # -------------------- ANIMACIÓN --------------------
        self.camera.background_color = BLACK
        
        self.play(Write(title))
        self.wait(1)
        
        self.play(
            FadeOut(title),
            LaggedStart(*[Create(circle) for circle in circles], lag_ratio=0.1),
            run_time=2
        )
        
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in static_arrows], lag_ratio=0.003),
            run_time=3
        )
        self.wait(0.5)
        
        title_center = MathTex(r"\text{rot}\,\vec{F}", font_size=80, color=YELLOW).move_to(ORIGIN)
        self.play(Write(title_center))
        
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in rotating_arrows], lag_ratio=0.02),
            run_time=2
        )
        self.wait(1)
        
        # Rotación continua con updater
        def rotate_arrows(mob, dt):
            mob.rotate(dt * 0.5, about_point=ORIGIN)
        
        rotating_arrows.add_updater(rotate_arrows)
        self.wait(10)  # Rota continuamente por 10 segundos
        rotating_arrows.remove_updater(rotate_arrows)
        
        self.wait(1)
        
        self.play(
            FadeOut(static_arrows),
            FadeOut(rotating_arrows),
            FadeOut(circles),
            FadeOut(title_center)
        )
```

<p align="center"><img src ="vidios_gifs/CampoRotacionalContinuo_ManimCE_v0.19.1.gif" /></p>

**Características:**
- **Updater para rotación continua**: 
  ```python
  def rotate_arrows(mob, dt):
      mob.rotate(dt * 0.5, about_point=ORIGIN)
  ```
- **Rotación suave**: El updater se ejecuta en cada frame
- **Control de velocidad**: `dt * 0.5` controla la velocidad angular (radianes/segundo)
- **Activar/desactivar**: `add_updater()` y `remove_updater()`

---

## 3. Campo Curl con Gradiente de Color

Visualización avanzada con gradiente de colores y múltiples círculos concéntricos.

```python
class CurlField(Scene):
    def construct(self):
        
        # -------------------- TÍTULO --------------------
        title = Text("Curl", font_size=100, color=WHITE, weight=BOLD).move_to(ORIGIN)
        
        # -------------------- CÍRCULOS CONCÉNTRICOS (LÍNEAS ROTATORIAS) --------------------
        circles = VGroup()
        num_circles = 40
        max_radius = 6
        
        for i in range(num_circles):
            r = max_radius * (i + 1) / num_circles
            circle = Circle(radius=r, color=GREY, stroke_width=1.5, stroke_opacity=0.6)
            circles.add(circle)
        
        # -------------------- FLECHAS CON GRADIENTE DE COLOR --------------------
        arrows = VGroup()
        
        # Parámetros para la distribución de flechas
        num_radii = 25
        arrows_per_radius = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56]
        
        for i in range(num_radii):
            r = max_radius * (i + 1) / num_radii
            n_arrows = arrows_per_radius[min(i, len(arrows_per_radius) - 1)]
            
            for j in range(n_arrows):
                angle = TAU * j / n_arrows
                position = np.array([r * np.cos(angle), r * np.sin(angle), 0])
                
                # Dirección tangencial
                direction = np.array([-np.sin(angle), np.cos(angle), 0])
                
                # Longitud de flecha
                arrow_length = 0.15
                end_point = position + direction * arrow_length
                
                # Gradiente de color basado en el radio
                color_value = i / num_radii
                if color_value < 0.25:
                    color = interpolate_color(RED, ORANGE, color_value * 4)
                elif color_value < 0.5:
                    color = interpolate_color(ORANGE, YELLOW, (color_value - 0.25) * 4)
                elif color_value < 0.75:
                    color = interpolate_color(YELLOW, GREEN, (color_value - 0.5) * 4)
                else:
                    color = interpolate_color(GREEN, TEAL, (color_value - 0.75) * 4)
                
                arrow = Arrow(
                    start=position,
                    end=end_point,
                    color=color,
                    buff=0,
                    stroke_width=2.5,
                    max_tip_length_to_length_ratio=0.3,
                    max_stroke_width_to_length_ratio=5
                )
                
                arrows.add(arrow)
        
        # -------------------- ANIMACIÓN --------------------
        self.camera.background_color = BLACK
        
        # Mostrar título
        self.play(Write(title))
        self.wait(1)
        
        # Fade out título
        self.play(FadeOut(title))
        self.wait(0.3)
        
        # Mostrar círculos y flechas simultáneamente
        self.play(
            LaggedStart(*[Create(circle) for circle in circles], lag_ratio=0.03),
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.002),
            run_time=3
        )
        self.wait(0.5)
        
        # Mostrar título en el centro
        title_center = Text("Curl", font_size=100, color=WHITE, weight=BOLD).move_to(ORIGIN)
        self.play(Write(title_center))
        self.wait(1)
        
        # -------------------- ROTACIÓN CON IMPULSOS --------------------
        # Impulso 1: Rotación rápida
        self.play(
            Rotate(circles, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            Rotate(arrows, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            run_time=0.8
        )
        # Reposo
        self.wait(0.4)
        
        # Impulso 2
        self.play(
            Rotate(circles, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            Rotate(arrows, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            run_time=0.8
        )
        self.wait(0.4)
        
        # Impulso 3
        self.play(
            Rotate(circles, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            Rotate(arrows, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            run_time=0.8
        )
        self.wait(0.4)
        
        # Impulso 4
        self.play(
            Rotate(circles, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            Rotate(arrows, angle=PI/2, about_point=ORIGIN, rate_func=rush_into),
            run_time=0.8
        )
        self.wait(0.5)
        
        # Impulso 5 - más largo
        self.play(
            Rotate(circles, angle=PI, about_point=ORIGIN, rate_func=rush_into),
            Rotate(arrows, angle=PI, about_point=ORIGIN, rate_func=rush_into),
            run_time=1.2
        )
        self.wait(0.6)
        
        # Impulso 6
        self.play(
            Rotate(circles, angle=PI, about_point=ORIGIN, rate_func=rush_into),
            Rotate(arrows, angle=PI, about_point=ORIGIN, rate_func=rush_into),
            run_time=1.2
        )
        self.wait(0.6)
        
        # Rotación continua final
        self.play(
            Rotate(circles, angle=TAU * 2, about_point=ORIGIN, rate_func=linear),
            Rotate(arrows, angle=TAU * 2, about_point=ORIGIN, rate_func=linear),
            run_time=6
        )
        
        self.wait(1)
        
        # Fade out
        self.play(
            FadeOut(circles),
            FadeOut(arrows),
            FadeOut(title_center)
        )
```

<p align="center"><img src ="vidios_gifs/CurlField_ManimCE_v0.19.1.gif" /></p>


**Características:**
- **40 círculos concéntricos** para mayor densidad visual
- **Gradiente de color automático**: Rojo → Naranja → Amarillo → Verde → Turquesa
- **Interpolación de colores**: 
  ```python
  color = interpolate_color(COLOR1, COLOR2, factor)
  ```
- **Distribución variable de flechas**: Más flechas en círculos externos
- **Animación por impulsos**: Usa `rush_into` para efecto de aceleración
- **Secuencia de rotaciones**: Impulsos cortos (π/2) seguidos de impulsos largos (π, 2π)

---

## 4. Campo Curl con Efecto Pulsante

Variación con efecto de aceleración y desaceleración más dramático.

```python
class CurlFieldPulse(Scene):
    def construct(self):
        
        # -------------------- TÍTULO --------------------
        title = Text("Curl", font_size=100, color=WHITE, weight=BOLD).move_to(ORIGIN)
        
        # -------------------- CÍRCULOS CONCÉNTRICOS --------------------
        circles = VGroup()
        num_circles = 40
        max_radius = 6
        
        for i in range(num_circles):
            r = max_radius * (i + 1) / num_circles
            circle = Circle(radius=r, color=GREY, stroke_width=1.5, stroke_opacity=0.6)
            circles.add(circle)
        
        # -------------------- FLECHAS CON GRADIENTE --------------------
        arrows = VGroup()
        num_radii = 25
        arrows_per_radius = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56]
        
        for i in range(num_radii):
            r = max_radius * (i + 1) / num_radii
            n_arrows = arrows_per_radius[min(i, len(arrows_per_radius) - 1)]
            
            for j in range(n_arrows):
                angle = TAU * j / n_arrows
                position = np.array([r * np.cos(angle), r * np.sin(angle), 0])
                direction = np.array([-np.sin(angle), np.cos(angle), 0])
                
                arrow_length = 0.15
                end_point = position + direction * arrow_length
                
                color_value = i / num_radii
                if color_value < 0.25:
                    color = interpolate_color(RED, ORANGE, color_value * 4)
                elif color_value < 0.5:
                    color = interpolate_color(ORANGE, YELLOW, (color_value - 0.25) * 4)
                elif color_value < 0.75:
                    color = interpolate_color(YELLOW, GREEN, (color_value - 0.5) * 4)
                else:
                    color = interpolate_color(GREEN, TEAL, (color_value - 0.75) * 4)
                
                arrow = Arrow(
                    start=position,
                    end=end_point,
                    color=color,
                    buff=0,
                    stroke_width=2.5,
                    max_tip_length_to_length_ratio=0.3,
                    max_stroke_width_to_length_ratio=5
                )
                
                arrows.add(arrow)
        
        # -------------------- ANIMACIÓN --------------------
        self.camera.background_color = BLACK
        
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        self.wait(0.3)
        
        self.play(
            LaggedStart(*[Create(circle) for circle in circles], lag_ratio=0.03),
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.002),
            run_time=3
        )
        self.wait(0.5)
        
        title_center = Text("Curl", font_size=100, color=WHITE, weight=BOLD).move_to(ORIGIN)
        self.play(Write(title_center))
        self.wait(1)
        
        # -------------------- IMPULSOS CON EFECTO DE ACELERACIÓN/DESACELERACIÓN --------------------
        angles = [PI/3, PI/2, 2*PI/3, PI, PI, 3*PI/2, TAU]
        times = [0.6, 0.7, 0.8, 1.0, 1.0, 1.2, 1.5]
        rests = [0.5, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2]
        
        for angle, time, rest in zip(angles, times, rests):
            # Impulso con aceleración y desaceleración
            self.play(
                Rotate(circles, angle=angle, about_point=ORIGIN, rate_func=there_and_back_with_pause),
                Rotate(arrows, angle=angle, about_point=ORIGIN, rate_func=there_and_back_with_pause),
                run_time=time
            )
            # Reposo
            self.wait(rest)
        
        self.wait(1)
        
        self.play(
            FadeOut(circles),
            FadeOut(arrows),
            FadeOut(title_center)
        )
```

<p align="center"><img src ="vidios_gifs/CurlFieldPulse_ManimCE_v0.19.1.gif" /></p>

**Características:**
- **Efecto pulsante**: Usa `there_and_back_with_pause` para crear movimiento de ida y vuelta
- **Secuencia de impulsos progresiva**: Ángulos y tiempos variables
- **Arrays de control**:
  ```python
  angles = [PI/3, PI/2, 2*PI/3, PI, PI, 3*PI/2, TAU]
  times = [0.6, 0.7, 0.8, 1.0, 1.0, 1.2, 1.5]
  rests = [0.5, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2]
  ```
- **Efecto visual**: Simula un campo que "respira" o pulsa

---

## Conceptos Clave

### Campo Vectorial Rotacional

El campo rotacional (o curl) se define como:
```python
# Para un punto (x, y):
direction = np.array([-y, x, 0])  # Perpendicular al vector posición
direction = direction / np.linalg.norm(direction)  # Normalizar
```

**Interpretación física:**
- **Rotacional positivo**: Rotación antihoraria
- **Rotacional negativo**: Rotación horaria (usar `[y, -x, 0]`)
- **Campo solenoidal**: El campo rota alrededor del origen

---

### Gradiente de Colores

Crear transiciones suaves entre colores:

```python
# Interpolación simple entre dos colores
color = interpolate_color(RED, BLUE, 0.5)  # 50% entre rojo y azul

# Gradiente multi-color (4 segmentos)
color_value = i / num_items  # Valor entre 0 y 1

if color_value < 0.25:
    color = interpolate_color(RED, ORANGE, color_value * 4)
elif color_value < 0.5:
    color = interpolate_color(ORANGE, YELLOW, (color_value - 0.25) * 4)
elif color_value < 0.75:
    color = interpolate_color(YELLOW, GREEN, (color_value - 0.5) * 4)
else:
    color = interpolate_color(GREEN, TEAL, (color_value - 0.75) * 4)
```

---

### LaggedStart

Animar múltiples objetos con retraso entre ellos:

```python
# Crear todos los círculos con retraso
LaggedStart(
    *[Create(circle) for circle in circles],
    lag_ratio=0.1  # Retraso entre cada objeto (0-1)
)

# Retrasos típicos:
# 0.003 - Muchos objetos pequeños (flechas)
# 0.02  - Objetos medianos
# 0.1   - Pocos objetos grandes
```

---

### Rate Functions (Funciones de Velocidad)

Controlan cómo cambia la velocidad de una animación:

```python
# Velocidad constante
rate_func=linear

# Acelerar al principio, desacelerar al final
rate_func=smooth

# Aceleración rápida
rate_func=rush_into

# Desaceleración rápida
rate_func=rush_from

# Ida y vuelta con pausa
rate_func=there_and_back_with_pause

# Rebote
rate_func=there_and_back

# Personalizada
rate_func=lambda t: t**2  # Aceleración cuadrática
```

---

### Updaters para Animación Continua

Crear movimiento que se actualiza cada frame:

```python
def rotate_continuously(mob, dt):
    """
    mob: El objeto a animar
    dt: Delta time (tiempo desde el último frame)
    """
    mob.rotate(dt * 0.5, about_point=ORIGIN)  # 0.5 rad/s

# Activar
rotating_arrows.add_updater(rotate_continuously)

# La animación continúa durante todos los wait()
self.wait(10)

# Desactivar
rotating_arrows.remove_updater(rotate_continuously)
```

**Otros ejemplos de updaters:**

```python
# Mover en círculo
def move_in_circle(mob, dt):
    mob.shift(RIGHT * 2 * dt).rotate(dt)

# Cambiar color gradualmente
def fade_color(mob, dt):
    current_opacity = mob.get_fill_opacity()
    mob.set_fill_opacity(current_opacity - dt * 0.1)

# Escalar con el tiempo
def grow(mob, dt):
    mob.scale(1 + dt * 0.05)
```

---

### VGroup y Manipulación de Múltiples Objetos

Agrupar objetos para aplicarles transformaciones:

```python
# Crear grupo vacío
arrows = VGroup()

# Agregar objetos
for i in range(10):
    arrow = Arrow(...)
    arrows.add(arrow)

# Aplicar transformación a todo el grupo
self.play(Rotate(arrows, angle=PI))

# Aplicar a cada elemento individualmente
self.play(*[arrow.animate.shift(UP) for arrow in arrows])
```

---

### Parámetros de Arrow

Controlar la apariencia de las flechas:

```python
arrow = Arrow(
    start=start_point,              # Punto inicial [x, y, z]
    end=end_point,                  # Punto final [x, y, z]
    color=RED,                      # Color
    buff=0,                         # Espacio antes/después
    stroke_width=2,                 # Grosor de la línea
    max_tip_length_to_length_ratio=0.25,  # Tamaño máximo de punta (relativo)
    max_stroke_width_to_length_ratio=5    # Grosor máximo (relativo)
)
```

---

## Tips y Buenas Prácticas

1. **Campos vectoriales densos**: Usar `lag_ratio` pequeño (0.002-0.005) en `LaggedStart`

2. **Evitar el origen**: Filtrar puntos muy cercanos al centro para evitar divisiones por cero:
   ```python
   if distance > 0.5:  # Umbral mínimo
   ```

3. **Normalizar vectores**: Siempre normalizar vectores de dirección:
   ```python
   direction = direction / np.linalg.norm(direction)
   ```

4. **Optimización**: Para muchas flechas, considerar reducir la resolución en pruebas

5. **Colores y opacidad**: Usar opacidad baja (0.3-0.6) para círculos de guía

6. **Rate functions**: Experimentar con diferentes `rate_func` para efectos dramáticos