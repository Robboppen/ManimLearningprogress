# Tutorial de Manim - Animaciones 3D

Este documento contiene ejemplos de código Manim para crear animaciones en 3D, transformaciones de superficies y objetos tridimensionales.

---

## 1. Transformación de Esfera a Esferoide Oblato (Simple)

Ejemplo básico de transformación 3D usando objetos predefinidos.

```python
from manim import *

class EsferaAEsferoideOblata(ThreeDScene):
    def construct(self):

        # Cámara
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=45 * DEGREES,
            zoom=0.9
        )

        # Ejes cartesianos 3D
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[-3, 3],
            axis_config={"color": WHITE}
        )

        labels = axes.get_axis_labels(
            Text("x"), Text("y"), Text("z")
        )

        # Esfera
        sphere = Sphere(
            radius=1.5,
            resolution=(32, 32),
            fill_color=BLUE,
            fill_opacity=0.6,
            stroke_color=BLUE_E
        )

        # Animaciones iniciales
        self.play(Create(axes), Write(labels))
        self.play(FadeIn(sphere))
        self.wait(1)

        # Transformación a esferoide oblata
        oblate = sphere.copy().scale([1, 1, 0.5])

        self.play(
            Transform(sphere, oblate),
            run_time=3
        )

        self.wait(2)
```

<p align="center"><img src ="vidios_gifs/EsferaAEsferoideOblata_ManimCE_v0.19.1.gif" /></p>

**Características:**
- Uso de `ThreeDScene` para escenas 3D
- Configuración de cámara con ángulos `phi` (elevación) y `theta` (azimut)
- Objeto `Sphere` predefinido con opacidad y color
- Transformación simple usando `scale()` con factores diferentes por eje
- `ThreeDAxes` para sistema de coordenadas tridimensional

---

## 2. Transformación con Superficies Paramétricas

Ejemplo avanzado usando superficies paramétricas personalizadas con ecuaciones matemáticas.

```python
class SphereToOblate(ThreeDScene):
    def construct(self):
        
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        
        # -------------------- SPHERE --------------------
        sphere = Surface(
            lambda u, v: np.array([
                1.5 * np.cos(u) * np.cos(v),
                1.5 * np.cos(u) * np.sin(v),
                1.5 * np.sin(u)
            ]),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, TAU],
            resolution=(30, 30),
            checkerboard_colors=[RED_D, RED_E]
        )
        
        # -------------------- OBLATE SPHEROID --------------------
        # Parámetros para el esferoide oblato
        a = 1.5  # parámetro de escala
        
        oblate_spheroid = Surface(
            lambda u, v: np.array([
                a * np.cosh(u) * np.cos(v) * np.cos(0),
                a * np.cosh(u) * np.cos(v) * np.sin(TAU * 0.5),
                a * np.sinh(u) * np.sin(v)
            ]),
            u_range=[0, 1.2],
            v_range=[-PI/2, PI/2],
            resolution=(30, 30),
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        
        # Versión completa del esferoide oblato (revolucionando alrededor del eje z)
        oblate_full = Surface(
            lambda u, v: np.array([
                a * np.cosh(0.8) * np.cos(u) * np.cos(v),
                a * np.cosh(0.8) * np.cos(u) * np.sin(v),
                a * np.sinh(0.8) * np.sin(u)
            ]),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, TAU],
            resolution=(30, 30),
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        
        # -------------------- TITLES AND EQUATIONS --------------------
        title_sphere = Text("Sphere", font_size=44).to_corner(UL)
        title_oblate = Text("Oblate Spheroid", font_size=44).to_corner(UL)
        
        # Ecuaciones de la esfera
        eq_sphere = MathTex(
            r"x &= R\cos\theta\cos\varphi\\",
            r"y &= R\cos\theta\sin\varphi\\",
            r"z &= R\sin\theta",
            font_size=32
        ).to_corner(UR)
        
        # Ecuaciones del esferoide oblato
        eq_oblate = MathTex(
            r"x &= a\cosh\mu\cos\nu\cos\varphi\\",
            r"y &= a\cosh\mu\cos\nu\sin\varphi\\",
            r"z &= a\sinh\mu\sin\nu",
            font_size=32
        ).to_corner(UR)
        
        # -------------------- CAMERA SETUP --------------------
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.15)
        
        # -------------------- ANIMATION SEQUENCE --------------------
        self.add(axes)
        
        # Mostrar esfera con su título y ecuaciones
        self.add_fixed_in_frame_mobjects(title_sphere, eq_sphere)
        self.play(
            Create(sphere),
            Write(title_sphere),
            Write(eq_sphere)
        )
        self.wait(2)
        
        # Transformar a esferoide oblato
        self.remove(title_sphere, eq_sphere)
        self.add_fixed_in_frame_mobjects(title_oblate, eq_oblate)
        self.play(
            ReplacementTransform(sphere, oblate_full),
            Write(title_oblate),
            Write(eq_oblate),
            run_time=2
        )
        self.wait(3)
        
        # Fade out
        self.play(
            FadeOut(oblate_full),
            FadeOut(title_oblate),
            FadeOut(eq_oblate),
            FadeOut(axes)
        )
        self.wait()
```


<p align="center"><img src ="vidios_gifs/SphereToOblate_ManimCE_v0.19.1.gif" /></p>

**Características:**
- **Superficies paramétricas personalizadas** usando `Surface()`
- **Esfera en coordenadas esféricas**:
  - `x = R·cos(θ)·cos(φ)`
  - `y = R·cos(θ)·sin(φ)`
  - `z = R·sin(θ)`
- **Esferoide oblato en coordenadas esferoidales oblatas**:
  - `x = a·cosh(μ)·cos(ν)·cos(φ)`
  - `y = a·cosh(μ)·cos(ν)·sin(φ)`
  - `z = a·sinh(μ)·sin(ν)`
- **Patrón de tablero de ajedrez** con `checkerboard_colors`
- **Cámara rotando** con `begin_ambient_camera_rotation()`
- **Texto fijo en pantalla** usando `add_fixed_in_frame_mobjects()`
- **Ecuaciones matemáticas** mostradas junto a los objetos 3D

---

## Conceptos Clave de Animaciones 3D

### ThreeDScene
Clase base para todas las escenas 3D:
```python
class MiEscena3D(ThreeDScene):
    def construct(self):
        # Tu código aquí
```

### Configuración de Cámara

#### Orientación estática
```python
self.set_camera_orientation(
    phi=70 * DEGREES,      # Ángulo de elevación (0° = vista lateral, 90° = vista superior)
    theta=45 * DEGREES,    # Ángulo de rotación horizontal
    zoom=0.9               # Factor de zoom
)
```

#### Rotación automática
```python
self.begin_ambient_camera_rotation(
    rate=0.15  # Velocidad de rotación (radianes por segundo)
)

# Detener rotación
self.stop_ambient_camera_rotation()
```

#### Mover cámara durante animación
```python
self.move_camera(
    phi=75 * DEGREES,
    theta=30 * DEGREES,
    run_time=2
)
```

---

### ThreeDAxes
Sistema de coordenadas tridimensional:

```python
axes = ThreeDAxes(
    x_range=[-3, 3, 1],  # [min, max, paso]
    y_range=[-3, 3, 1],
    z_range=[-3, 3, 1],
    x_length=6,          # Longitud visual
    y_length=6,
    z_length=6,
    axis_config={"color": WHITE}
)

# Etiquetas de ejes
labels = axes.get_axis_labels(
    Text("x"), Text("y"), Text("z")
)
```

---

### Objetos 3D Predefinidos

#### Sphere (Esfera)
```python
sphere = Sphere(
    radius=1.5,
    resolution=(32, 32),      # (latitud, longitud)
    fill_color=BLUE,
    fill_opacity=0.6,
    stroke_color=BLUE_E,
    stroke_width=0.5
)
```

#### Cube (Cubo)
```python
cube = Cube(
    side_length=2,
    fill_color=RED,
    fill_opacity=0.7
)
```

#### Cylinder (Cilindro)
```python
cylinder = Cylinder(
    radius=1,
    height=3,
    fill_color=GREEN,
    fill_opacity=0.8
)
```

#### Cone (Cono)
```python
cone = Cone(
    base_radius=1,
    height=2,
    fill_color=YELLOW
)
```

---

### Superficies Paramétricas

Crear superficies personalizadas con ecuaciones matemáticas:

```python
surface = Surface(
    lambda u, v: np.array([
        # Función de x(u, v)
        # Función de y(u, v)
        # Función de z(u, v)
    ]),
    u_range=[u_min, u_max],
    v_range=[v_min, v_max],
    resolution=(30, 30),
    checkerboard_colors=[COLOR1, COLOR2]
)
```

#### Ejemplo: Paraboloide
```python
paraboloid = Surface(
    lambda u, v: np.array([
        u * np.cos(v),
        u * np.sin(v),
        u**2
    ]),
    u_range=[0, 2],
    v_range=[0, TAU],
    checkerboard_colors=[BLUE_D, BLUE_E]
)
```

#### Ejemplo: Toro
```python
torus = Surface(
    lambda u, v: np.array([
        (2 + np.cos(u)) * np.cos(v),
        (2 + np.cos(u)) * np.sin(v),
        np.sin(u)
    ]),
    u_range=[0, TAU],
    v_range=[0, TAU],
    checkerboard_colors=[RED_D, RED_E]
)
```

---

### Texto en Escenas 3D

Para que el texto permanezca fijo frente a la cámara:

```python
title = Text("Mi Título").to_corner(UL)
equation = MathTex(r"E = mc^2").to_corner(UR)

# Agregar como elementos fijos en el frame
self.add_fixed_in_frame_mobjects(title, equation)

# Animarlos
self.play(Write(title), Write(equation))
```

---

### Transformaciones 3D

#### Escalar (con factores diferentes por eje)
```python
# Escalar solo en z (aplanar)
obj.scale([1, 1, 0.5])

# Escalar uniformemente
obj.scale(2)
```

#### Rotar
```python
obj.rotate(PI/4, axis=OUT)    # Rotar alrededor del eje z
obj.rotate(PI/3, axis=RIGHT)  # Rotar alrededor del eje x
obj.rotate(PI/6, axis=UP)     # Rotar alrededor del eje y
```

#### Mover
```python
obj.shift(UP * 2)
obj.move_to([1, 2, 3])
```

---

## Coordenadas Matemáticas Comunes

### Coordenadas Esféricas
```python
x = r * np.cos(theta) * np.cos(phi)
y = r * np.cos(theta) * np.sin(phi)
z = r * np.sin(theta)
```

### Coordenadas Cilíndricas
```python
x = r * np.cos(theta)
y = r * np.sin(theta)
z = z
```

### Coordenadas Esferoidales Oblatas
```python
x = a * np.cosh(mu) * np.cos(nu) * np.cos(phi)
y = a * np.cosh(mu) * np.cos(nu) * np.sin(phi)
z = a * np.sinh(mu) * np.sin(nu)
```

### Coordenadas Esferoidales Prolatas
```python
x = a * np.sinh(mu) * np.sin(nu) * np.cos(phi)
y = a * np.sinh(mu) * np.sin(nu) * np.sin(phi)
z = a * np.cosh(mu) * np.cos(nu)
```

---

## Comandos de Renderizado 3D

```bash
# Calidad baja (rápido)
manim -pql archivo.py NombreDeLaClase

# Calidad media
manim -pqm archivo.py NombreDeLaClase

# Calidad alta (recomendado para 3D)
manim -pqh archivo.py NombreDeLaClase

# Alta calidad con 60 fps
manim -pqk archivo.py NombreDeLaClase
```

---

## Tips y Buenas Prácticas

1. **Resolución**: Mayor resolución = renderizado más lento pero más suave
   - Para pruebas: `resolution=(15, 15)`
   - Para producción: `resolution=(30, 30)` o más

2. **Opacidad**: Usar `fill_opacity` entre 0.5 y 0.8 para ver profundidad

3. **Colores con patrón**: `checkerboard_colors` ayuda a visualizar la curvatura

4. **Rotación de cámara**: `begin_ambient_camera_rotation()` añade dinamismo

5. **Texto fijo**: Siempre usar `add_fixed_in_frame_mobjects()` para texto/ecuaciones

6. **Ejes**: Ayudan a orientar al espectador en el espacio 3D

7. **Iluminación**: Manim usa iluminación por defecto, pero se puede personalizar

---

