

```python
from manim import *
import numpy as np

class CampoGravitacional(ThreeDScene):
    def construct(self):
        
        # -------------------- EARTH IMAGE --------------------
        earth_image = ImageMobject("earth.jpg")
        earth_image.scale(0.5)
        earth_image.move_to(ORIGIN)
        
        # -------------------- TÍTULOS Y ECUACIONES --------------------
        title = Text("Campo gravitacional", font_size=60, color=BLUE).to_edge(UP)
        
        equation = MathTex(
            r"\vec{g}(\vec{r}) = -\frac{GM}{R^2}\hat{r}",
            font_size=50,
            color=BLUE
        ).to_edge(DOWN)
        
        # -------------------- GRAVITATIONAL FIELD ARROWS --------------------
        arrows = VGroup()
        
        # Crear una cuadrícula de flechas en 2D (vista frontal)
        x_range = np.arange(-6, 7, 0.5)
        y_range = np.arange(-3.5, 4, 0.5)
        
        earth_radius = 1.5  # Radio aproximado de la imagen de la Tierra
        
        for x in x_range:
            for y in y_range:
                position = np.array([x, y, 0])
                distance = np.linalg.norm(position)
                
                # Solo crear flechas fuera de la Tierra
                if distance > earth_radius:
                    # Dirección hacia el centro
                    direction = -position / distance
                    
                    # Longitud de la flecha (más corta lejos, más larga cerca)
                    arrow_length = 0.25 / (distance ** 0.8)
                    
                    # Punto final de la flecha
                    end_point = position + direction * arrow_length
                    
                    # Crear flecha pequeña
                    arrow = Arrow(
                        start=position,
                        end=end_point,
                        color=BLUE_C,
                        buff=0,
                        stroke_width=2,
                        max_tip_length_to_length_ratio=0.3,
                        max_stroke_width_to_length_ratio=4
                    )
                    
                    arrows.add(arrow)
        
        # -------------------- ANIMATION --------------------
        # Fondo negro
        self.camera.background_color = BLACK
        
        # Mostrar título
        self.play(Write(title))
        self.wait(0.5)
        
        # Mostrar la Tierra
        self.play(FadeIn(earth_image), run_time=1)
        self.wait(0.5)
        
        # Mostrar flechas gradualmente
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.01),
            run_time=3
        )
        self.wait(0.5)
        
        # Mostrar ecuación
        self.play(Write(equation))
        self.wait(3)
        
        # Fade out
        self.play(
            FadeOut(title),
            FadeOut(earth_image),
            FadeOut(arrows),
            FadeOut(equation)
        )
```

<p align="center"><img src ="vidios_gifs/CampoGravitacional_ManimCE_v0.19.1.gif" /></p>
