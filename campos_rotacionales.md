# Campos Vectoriales 2D con Manim

## Código Completo

```python
from manim import *
import numpy as np

class CampoRotacional2D(Scene):
    def construct(self):

        # -----------------------
        # Estilo general
        # -----------------------
        self.camera.background_color = BLACK


        # -----------------------
        # Plano cartesiano
        # -----------------------
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            }
        )

        self.play(Create(plane), run_time=2)

        # -----------------------
        # Parámetro temporal
        # -----------------------
        omega = ValueTracker(0.5)

        # -----------------------
        # Campo vectorial rotacional
        # -----------------------
        def vector_field(pos):
            x, y = pos[:2]
            w = omega.get_value()
            return np.array([-w * y, w * x, 0])

        # -----------------------
        # StreamLines
        # -----------------------

        def color_value(vec):
            mag = np.linalg.norm(vec)
            return np.tanh(mag)   # satura rápido → colores más vivos

        
        stream_lines = StreamLines(
            vector_field,
            x_range=[-4, 4, 0.4],
            y_range=[-4, 4, 0.4],
            stroke_width=2.5,          # más presencia visual
            max_anchors_per_line=40,
            color_scheme=color_value,
        )

        self.add(stream_lines)
        stream_lines.start_animation(
            flow_speed=1.2,
            warm_up=True
        )

        # -----------------------
        # Partículas de prueba
        # -----------------------
        particles = VGroup()

        for r in [1.5, 2.5, 3.5]:
            for theta in np.linspace(0, TAU, 8, endpoint=False):
                dot = Dot(
                    plane.c2p(
                        r * np.cos(theta),
                        r * np.sin(theta)
                    ),
                    radius=0.04,
                    color=YELLOW
                )

                def particle_updater(mob, dt, r=r):
                    pos = mob.get_center()
                    v = vector_field(pos)
                    mob.shift(v * dt)

                dot.add_updater(particle_updater)
                particles.add(dot)

        self.add(particles)

        # -----------------------
        # Texto explicativo
        # -----------------------
        title = MathTex(
            r"\vec{F}(x,y)=\omega(t)(-y,x)",
            color=WHITE
        ).scale(0.9).to_corner(UL)

        omega_text = always_redraw(
            lambda: MathTex(
                rf"\omega(t)={omega.get_value():.2f}",
                color=WHITE
            ).scale(0.8).next_to(title, DOWN, aligned_edge=LEFT)
        )

        self.play(Write(title), FadeIn(omega_text))

        # -----------------------
        # Animación temporal
        # -----------------------
        self.play(
            omega.animate.set_value(2.0),
            run_time=6,
            rate_func=smooth
        )

        self.play(
            omega.animate.set_value(0.3),
            run_time=4,
            rate_func=smooth
        )

        self.wait(2)
```

``` python
class CampoRotacionalNoUniforme(Scene):
    def construct(self):

        # -----------------------
        # Fondo negro
        # -----------------------
        self.camera.background_color = BLACK

        # -----------------------
        # Plano
        # -----------------------
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.35,
            }
        )
        self.add(plane)

        # -----------------------
        # Parámetro temporal
        # -----------------------
        strength = ValueTracker(1.0)

        # -----------------------
        # Campo no uniforme (con cutoff)
        # -----------------------
        r_min = 0.3

        def vector_field(pos):
            x, y = pos[:2]
            r2 = x**2 + y**2
            if r2 < r_min**2:
                return np.array([0.0, 0.0, 0.0])
            s = strength.get_value()
            return s * np.array([-y / r2, x / r2, 0.0])

        # -----------------------
        # Escalar de color (brillante)
        # -----------------------
        def color_value(vec):
            mag = np.linalg.norm(vec)
            return np.tanh(2 * mag)

        # -----------------------
        # StreamLines
        # -----------------------
        stream_lines = StreamLines(
            vector_field,
            x_range=[-4.5, 4.5, 0.35],
            y_range=[-4.5, 4.5, 0.35],
            stroke_width=2.5,
            max_anchors_per_line=45,
            color_scheme=color_value,
        )

        self.add(stream_lines)
        stream_lines.start_animation(
            flow_speed=1.6,
            warm_up=True
        )

        # -----------------------
        # Partículas
        # -----------------------
        particles = VGroup()

        for r in [1.2, 2.0, 3.0]:
            for theta in np.linspace(0, TAU, 10, endpoint=False):
                dot = Dot(
                    plane.c2p(
                        r * np.cos(theta),
                        r * np.sin(theta)
                    ),
                    radius=0.045,
                    color=YELLOW_B
                )

                def particle_updater(mob, dt):
                    pos = mob.get_center()
                    v = vector_field(pos)
                    mob.shift(v * dt)

                dot.add_updater(particle_updater)
                particles.add(dot)

        self.add(particles)

        # -----------------------
        # Texto
        # -----------------------
        title = MathTex(
            r"\vec{F}(x,y)=\frac{1}{x^2+y^2}(-y,x)",
            color=WHITE
        ).scale(0.85).to_corner(UL)

        self.play(Write(title))

        # -----------------------
        # Dinámica temporal
        # -----------------------
        self.play(
            strength.animate.set_value(2.5),
            run_time=6,
            rate_func=smooth
        )

        self.wait(2)
```

``` python
class CampoDivergenteRotacional(Scene):
    def construct(self):

        # -----------------------
        # Fondo negro
        # -----------------------
        self.camera.background_color = BLACK

        # -----------------------
        # Plano cartesiano
        # -----------------------
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.35,
            }
        )
        self.add(plane)

        # -----------------------
        # Parámetro de rotación
        # -----------------------
        alpha = ValueTracker(0.0)

        # -----------------------
        # Campo fuente + rotación
        # -----------------------
        def vector_field(pos):
            x, y = pos[:2]
            a = alpha.get_value()
            return np.array([
                x - a * y,
                y + a * x,
                0.0
            ])

        # -----------------------
        # Escalar para color (brillante)
        # -----------------------
        def color_value(vec):
            mag = np.linalg.norm(vec)
            return np.tanh(0.6 * mag)

        # -----------------------
        # StreamLines
        # -----------------------
        stream_lines = StreamLines(
            vector_field,
            x_range=[-4.5, 4.5, 0.4],
            y_range=[-4.5, 4.5, 0.4],
            stroke_width=2.5,
            max_anchors_per_line=45,
            color_scheme=color_value,
        )

        self.add(stream_lines)
        stream_lines.start_animation(
            flow_speed=1.4,
            warm_up=True
        )

        # -----------------------
        # Texto explicativo
        # -----------------------
        title = MathTex(
            r"\vec F(x,y)=(x,y)+\alpha(-y,x)",
            color=WHITE
        ).scale(0.85).to_corner(UL)

        alpha_text = always_redraw(
            lambda: MathTex(
                rf"\alpha={alpha.get_value():.2f}",
                color=WHITE
            ).scale(0.75).next_to(title, DOWN, aligned_edge=LEFT)
        )

        self.play(Write(title), FadeIn(alpha_text))

        # -----------------------
        # Activar la rotación
        # -----------------------
        self.play(
            alpha.animate.set_value(1.5),
            run_time=6,
            rate_func=smooth
        )

        self.wait(2)
```

---

## Explicación del Código

Este código implementa **tres tipos diferentes de campos vectoriales 2D** usando Manim, cada uno con sus propias características físicas y visuales.

---

## 1. Campo Rotacional Uniforme (`CampoRotacional2D`)

### Concepto Físico

Este campo representa un **campo de velocidades rotacional uniforme**, similar al flujo de un fluido en rotación sólida o el campo de velocidades en un disco giratorio.

**Ecuación del campo:**
```
F(x,y) = ω(t)(-y, x)
```

Donde `ω(t)` es la velocidad angular que varía con el tiempo.

### Características del Código

**Plano cartesiano**: Se crea un plano de coordenadas con líneas de cuadrícula sutiles en azul oscuro para proporcionar referencia espacial.

**Campo vectorial**: La función `vector_field(pos)` calcula el vector en cada posición. Para un punto (x,y), el vector resultante es perpendicular al radio y proporcional a la distancia del origen, creando un patrón circular.

**StreamLines (Líneas de flujo)**: Visualizan las trayectorias que seguirían las partículas en el campo. Se colorean según la magnitud del vector usando la función `tanh` para saturación de color.

**Partículas de prueba**: Se colocan 24 partículas amarillas en tres círculos concéntricos (radios 1.5, 2.5 y 3.5). Cada partícula tiene un `updater` que actualiza su posición según el campo vectorial, mostrando el movimiento real.

**Animación temporal**: El parámetro `ω` varía de 0.5 a 2.0 (aceleración) y luego a 0.3 (desaceleración), mostrando cómo cambia la velocidad de rotación.

### Propiedades Físicas

- **Rotacional no nulo**: ∇ × F ≠ 0
- **Divergencia cero**: ∇ · F = 0 (campo incompresible)
- **Trayectorias circulares**: Las partículas siguen órbitas circulares perfectas

---

## 2. Campo Rotacional No Uniforme (`CampoRotacionalNoUniforme`)

### Concepto Físico

Este campo representa un **vórtice con decaimiento radial**, similar a un remolino o torbellino donde la velocidad aumenta hacia el centro.

**Ecuación del campo:**
```
F(x,y) = (1/r²)(-y, x)
```

Donde r² = x² + y².

### Características del Código

**Cutoff en el origen**: Se define `r_min = 0.3` para evitar singularidades matemáticas en el centro (división por cero). Dentro de este radio, el campo se anula.

**Decaimiento 1/r²**: La magnitud del campo es inversamente proporcional al cuadrado de la distancia, creando un efecto de "succión" hacia el centro.

**Mayor densidad de StreamLines**: Se usa un espaciado de 0.35 (vs 0.4 del anterior) para capturar mejor los detalles del campo cerca del centro.

**Partículas en diferentes radios**: 30 partículas distribuidas en tres anillos (radios 1.2, 2.0 y 3.0) para visualizar el comportamiento a diferentes distancias.

**Parámetro de intensidad**: El valor `strength` varía de 1.0 a 2.5, aumentando la velocidad del vórtice.

### Propiedades Físicas

- **Velocidad inversamente proporcional a r²**: Las partículas más cercanas al centro se mueven más rápido
- **Rotacional concentrado**: La vorticidad es máxima cerca del centro
- **Similar a vórtices reales**: Modela tornados, remolinos y flujos ciclónicos

---

## 3. Campo Divergente-Rotacional (`CampoDivergenteRotacional`)

### Concepto Físico

Este campo combina **expansión radial con rotación**, creando un patrón espiral. Es similar al flujo en una galaxia espiral o en sistemas de fluidos con fuentes rotacionales.

**Ecuación del campo:**
```
F(x,y) = (x, y) + α(-y, x)
```

Donde:
- **(x, y)**: Componente radial (expansión desde el origen)
- **α(-y, x)**: Componente rotacional (giro alrededor del origen)

### Características del Código

**Combinación de efectos**: El campo es la suma de dos componentes:
1. Campo radial (x, y): empuja hacia afuera
2. Campo rotacional α(-y, x): induce rotación

**Parámetro α**: Controla la proporción de rotación vs. expansión:
- α = 0: Solo expansión radial pura
- α > 0: Aparecen espirales que se expanden hacia afuera
- α grande: Dominan las trayectorias curvas

**Animación**: El parámetro α aumenta de 0.0 a 1.5, mostrando la transición desde expansión radial pura hasta un patrón espiral.

**Coloración dinámica**: Usa `tanh(0.6 * mag)` para mapear la magnitud del vector a colores, con un factor más bajo que permite apreciar las variaciones de velocidad.

### Propiedades Físicas

- **Divergencia no nula**: ∇ · F = 2 (fuente de flujo)
- **Rotacional no nulo**: ∇ × F = 2α (vorticidad constante)
- **Trayectorias espirales**: Las partículas se alejan del centro siguiendo trayectorias curvas
- **Modela**: Galaxias espirales, flujos atmosféricos, chorros astrofísicos

---

## Elementos Técnicos Comunes

### StreamLines

Las líneas de flujo son la herramienta principal de visualización:

```python
StreamLines(
    vector_field,           # Función que define el campo
    x_range=[-4, 4, 0.4],  # Rango y densidad en x
    y_range=[-4, 4, 0.4],  # Rango y densidad en y
    stroke_width=2.5,       # Grosor de las líneas
    max_anchors_per_line=40,# Puntos por línea (suavidad)
    color_scheme=color_value,# Función de coloración
)
```

**Animación de flujo**: El método `start_animation()` con `flow_speed` hace que las líneas parezcan moverse, simulando el flujo real del campo.

### Updaters de Partículas

Cada partícula tiene un updater que actualiza su posición en cada frame:

```python
def particle_updater(mob, dt):
    pos = mob.get_center()      # Posición actual
    v = vector_field(pos)       # Vector del campo en esa posición
    mob.shift(v * dt)           # Desplazar según velocidad × tiempo
```

Este método implementa una **integración de Euler simple** para resolver la ecuación diferencial del movimiento.

### ValueTracker

Los `ValueTracker` permiten animar parámetros numéricos suavemente:

```python
omega = ValueTracker(0.5)

# Animación suave
self.play(omega.animate.set_value(2.0), run_time=6)
```

### Coloración por Magnitud

La función `color_value` mapea la magnitud del vector a un valor entre 0 y 1:

```python
def color_value(vec):
    mag = np.linalg.norm(vec)
    return np.tanh(mag)  # Saturación suave
```

La función `tanh` comprime valores grandes, evitando que los colores saturen demasiado rápido.

---

## Aplicaciones Educativas

Estos ejemplos son ideales para enseñar:

1. **Cálculo vectorial**: Divergencia, rotacional, campos conservativos
2. **Mecánica de fluidos**: Flujo incompresible, vórtices, líneas de corriente
3. **Física**: Campos de fuerza, movimiento en campos, ecuaciones diferenciales
4. **Análisis de sistemas dinámicos**: Puntos de equilibrio, trayectorias, estabilidad

---

## Comandos de Renderizado


```bash
# Campo rotacional uniforme
manim -pql vector_fields.py CampoRotacional2D

# Campo rotacional no uniforme
manim -pql vector_fields.py CampoRotacionalNoUniforme

# Campo divergente-rotacional
manim -pql vector_fields.py CampoDivergenteRotacional
```