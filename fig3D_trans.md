# Animación de Superficies 3D en Manim

## Código Completo
```python
from manim import *
import numpy as np

class SurfacesAnimation(ThreeDScene):
    def construct(self):

        axes = ThreeDAxes()

        # -------------------- CYLINDER --------------------
        cylinder = Surface(
            lambda u, v: np.array([
                np.cos(TAU * v),
                np.sin(TAU * v),
                2 * (1 - u)
            ]),
            u_range=[0, 1],
            v_range=[0, 1],
            resolution=(6, 32),
            fill_opacity=0.5,
            fill_color=GRAY
        )

        # -------------------- PARABOLOID --------------------
        paraboloid = Surface(
            lambda u, v: np.array([
                u * np.cos(v),
                u * np.sin(v),
                u**2
            ]),
            u_range=[0, 2],
            v_range=[0, TAU],
            resolution=(10, 32),
            checkerboard_colors=[PURPLE_D, PURPLE_E]
        ).scale(2)

        # -------------------- HYPERBOLIC PARABOLOID --------------------
        para_hyp = Surface(
            lambda u, v: np.array([
                u,
                v,
                u**2 - v**2
            ]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(15, 32),
            checkerboard_colors=[BLUE_D, BLUE_E]
        )

        # -------------------- CONE --------------------
        cone = Surface(
            lambda u, v: np.array([
                u * np.cos(v),
                u * np.sin(v),
                u
            ]),
            u_range=[0, 2],
            v_range=[0, TAU],
            resolution=(15, 32),
            checkerboard_colors=[GREEN_D, GREEN_E]
        )

        # -------------------- ONE-SHEET HYPERBOLOID --------------------
        hip_one_side = Surface(
            lambda u, v: np.array([
                np.cosh(u) * np.cos(v),
                np.cosh(u) * np.sin(v),
                np.sinh(u)
            ]),
            u_range=[-1.5, 1.5],
            v_range=[0, TAU],
            resolution=(15, 32),
            checkerboard_colors=[YELLOW_D, YELLOW_E]
        )

        # -------------------- ELLIPSOID --------------------
        ellipsoid = Surface(
            lambda u, v: np.array([
                np.cos(u) * np.cos(v),
                2 * np.cos(u) * np.sin(v),
                0.5 * np.sin(u)
            ]),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, TAU],
            resolution=(15, 32),
            checkerboard_colors=[TEAL_D, TEAL_E]
        ).scale(2)

        # -------------------- SPHERE --------------------
        sphere = Surface(
            lambda u, v: np.array([
                1.5 * np.cos(u) * np.cos(v),
                1.5 * np.cos(u) * np.sin(v),
                1.5 * np.sin(u)
            ]),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, TAU],
            resolution=(15, 32),
            checkerboard_colors=[RED_D, RED_E]
        ).scale(2)

        # -------------------- TITLES --------------------
        title_sphere = Text("Sphere", font_size=48).to_corner(UL)
        title_ellipsoid = Text("Ellipsoid", font_size=48).to_corner(UL)
        title_cone = Text("Cone", font_size=48).to_corner(UL)
        title_hyperboloid = Text("Hyperboloid (One Sheet)", font_size=36).to_corner(UL)
        title_para_hyp = Text("Hyperbolic Paraboloid", font_size=40).to_corner(UL)
        title_paraboloid = Text("Paraboloid", font_size=48).to_corner(UL)
        title_cylinder = Text("Cylinder", font_size=48).to_corner(UL)

        # -------------------- CAMERA --------------------
        self.set_camera_orientation(phi=75 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)

        # -------------------- ANIMATION SEQUENCE --------------------
        self.add(axes)

        # Agregar título fijo en el frame
        self.add_fixed_in_frame_mobjects(title_sphere)
        self.play(Create(sphere), Write(title_sphere))
        self.wait()

        self.remove(title_sphere)
        self.add_fixed_in_frame_mobjects(title_ellipsoid)
        self.play(
            ReplacementTransform(sphere, ellipsoid),
            Write(title_ellipsoid)
        )
        self.wait()

        self.remove(title_ellipsoid)
        self.add_fixed_in_frame_mobjects(title_cone)
        self.play(
            ReplacementTransform(ellipsoid, cone),
            Write(title_cone)
        )
        self.wait()

        self.remove(title_cone)
        self.add_fixed_in_frame_mobjects(title_hyperboloid)
        self.play(
            ReplacementTransform(cone, hip_one_side),
            Write(title_hyperboloid)
        )
        self.wait()

        self.remove(title_hyperboloid)
        self.add_fixed_in_frame_mobjects(title_para_hyp)
        self.play(
            ReplacementTransform(hip_one_side, para_hyp),
            Write(title_para_hyp)
        )
        self.wait()

        self.remove(title_para_hyp)
        self.add_fixed_in_frame_mobjects(title_paraboloid)
        self.play(
            ReplacementTransform(para_hyp, paraboloid),
            Write(title_paraboloid)
        )
        self.wait()

        self.remove(title_paraboloid)
        self.add_fixed_in_frame_mobjects(title_cylinder)
        self.play(
            ReplacementTransform(paraboloid, cylinder),
            Write(title_cylinder)
        )
        self.wait()

        self.play(FadeOut(cylinder), FadeOut(title_cylinder))
```

---

<p align="center"><img src ="vidios_gifs/SurfacesAnimation_ManimCE_v0.19.1.gif" /></p>


## Explicación del Código

### Estructura General

Este código crea una animación educativa que muestra siete superficies tridimensionales clásicas de la geometría y el cálculo multivariable. La clase `SurfacesAnimation` hereda de `ThreeDScene` y utiliza parametrizaciones matemáticas para generar cada superficie.

### Importaciones
```python
from manim import *
import numpy as np
```

Se importa la librería Manim completa y NumPy para las operaciones matemáticas necesarias en las parametrizaciones.

### Definición de las Superficies

El código define siete superficies paramétricas usando la clase `Surface` de Manim. Cada superficie se parametriza mediante una función lambda que toma dos parámetros `u` y `v` y devuelve un array NumPy con las coordenadas `[x, y, z]`.

#### 1. Cilindro (líneas 10-21)

**Parametrización:**
- x = cos(2πv)
- y = sin(2πv)
- z = 2(1 - u)

**Características:**
- Radio circular constante de 1
- Altura de 2 unidades
- Resolución: 6 divisiones en u, 32 en v
- Color gris con 50% de opacidad
- Los parámetros van de 0 a 1 para ambos u y v

#### 2. Paraboloide (líneas 23-33)

**Parametrización:**
- x = u·cos(v)
- y = u·sin(v)
- z = u²

**Características:**
- Forma de tazón parabólico
- Rango: u ∈ [0, 2], v ∈ [0, 2π]
- Patrón de tablero de ajedrez en tonos púrpura
- Escalado 2x para mejor visualización
- Superficie de revolución generada por una parábola

#### 3. Paraboloide Hiperbólico (líneas 35-45)

**Parametrización:**
- x = u
- y = v
- z = u² - v²

**Características:**
- También conocida como "silla de montar"
- Curvatura gaussiana negativa
- Rango: u, v ∈ [-2, 2]
- Colores azules en patrón de tablero
- Superficie doblemente reglada

#### 4. Cono (líneas 47-57)

**Parametrización:**
- x = u·cos(v)
- y = u·sin(v)
- z = u

**Características:**
- Cono circular recto
- Ángulo de apertura de 45° (pendiente = 1)
- Rango: u ∈ [0, 2], v ∈ [0, 2π]
- Colores verdes en patrón de tablero
- Superficie cónica clásica

#### 5. Hiperboloide de Una Hoja (líneas 59-69)

**Parametrización:**
- x = cosh(u)·cos(v)
- y = cosh(u)·sin(v)
- z = sinh(u)

**Características:**
- Utiliza funciones hiperbólicas (cosh, sinh)
- Forma de reloj de arena o torre de enfriamiento
- Rango: u ∈ [-1.5, 1.5], v ∈ [0, 2π]
- Colores amarillos
- Superficie de revolución de una hipérbola

#### 6. Elipsoide (líneas 71-81)

**Parametrización:**
- x = cos(u)·cos(v)
- y = 2·cos(u)·sin(v)
- z = 0.5·sin(u)

**Características:**
- Esfera estirada con diferentes semiejes
- Semiejes: a=1, b=2, c=0.5 (antes del escalado)
- Rango: u ∈ [-π/2, π/2], v ∈ [0, 2π]
- Colores turquesa/verde azulado
- Escalado 2x para mejor visualización

#### 7. Esfera (líneas 83-93)

**Parametrización:**
- x = 1.5·cos(u)·cos(v)
- y = 1.5·cos(u)·sin(v)
- z = 1.5·sin(u)

**Características:**
- Radio base de 1.5
- Rango: u ∈ [-π/2, π/2] (latitud), v ∈ [0, 2π] (longitud)
- Colores rojos
- Escalado 2x (radio final = 3)
- Parametrización esférica estándar

### Títulos (líneas 95-101)

Se crean siete objetos de texto, uno para cada superficie, todos posicionados en la esquina superior izquierda (`UL`). Los tamaños de fuente varían entre 36 y 48 puntos dependiendo de la longitud del nombre.

### Configuración de Cámara (líneas 103-105)
```python
self.set_camera_orientation(phi=75 * DEGREES)
self.begin_ambient_camera_rotation(rate=0.2)
```

- La cámara se posiciona con un ángulo phi de 75° (vista ligeramente desde arriba)
- Se inicia una rotación continua alrededor del eje vertical a una velocidad de 0.2 radianes por segundo
- Esto permite apreciar la forma tridimensional de cada superficie

### Secuencia de Animación (líneas 107-165)

La animación sigue un patrón consistente para cada superficie:

1. Se añaden los ejes 3D al inicio
2. Para cada superficie:
   - Se añade el título correspondiente fijo al marco de la cámara
   - Se crea/transforma la superficie
   - Se escribe el título
   - Se espera un momento para observar
   - Se elimina el título anterior

**Transiciones:**
- La primera superficie (esfera) usa `Create()` para dibujarla desde cero
- Las siguientes usan `ReplacementTransform()` que morfea una superficie en la siguiente
- La última superficie (cilindro) desaparece con `FadeOut()`

### Flujo de la Animación

El orden de presentación es:
1. Esfera → 2. Elipsoide → 3. Cono → 4. Hiperboloide → 5. Paraboloide Hiperbólico → 6. Paraboloide → 7. Cilindro

Este orden permite transiciones visuales suaves entre superficies con formas relacionadas.

### Parámetros Técnicos

**Resolution**: El parámetro `resolution=(a, b)` controla la calidad de la malla:
- Primer valor: divisiones en dirección u
- Segundo valor: divisiones en dirección v
- Valores más altos = superficies más suaves pero mayor costo computacional

**Checkerboard colors**: Crea un patrón visual que ayuda a percibir la curvatura y orientación de la superficie usando dos tonos del mismo color base.

### Conceptos Matemáticos Ilustrados

Este código es excelente para enseñar:
- Superficies paramétricas y su representación computacional
- Coordenadas cilíndricas y esféricas
- Cuadráticas tridimensionales (superficies de segundo grado)
- Diferencias entre superficies de curvatura positiva, negativa y cero
- Visualización de funciones de dos variables