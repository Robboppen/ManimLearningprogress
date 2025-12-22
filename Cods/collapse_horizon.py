from manim import *
import numpy as np

class RadialCollapseWithHorizon(ThreeDScene):
    def construct(self):
        # Parámetros físicos
        R = ValueTracker(3.0)      # radio inicial de la materia
        R_h = 1.5                  # horizonte (2M)

        # Materia colapsante
        matter = always_redraw(
            lambda: Sphere(
                radius=R.get_value(),
                resolution=(24, 48),
                fill_color=BLUE_D,
                fill_opacity=0.6,
                stroke_width=0
            )
        )

        # Horizonte de eventos (fijo)
        horizon = Sphere(
            radius=R_h,
            resolution=(24, 48),
            fill_color=RED,
            fill_opacity=0.18,
            stroke_width=0
        )

        # Ejes (opcional)
        axes = ThreeDAxes(
            x_range=(-4,4),
            y_range=(-4,4),
            z_range=(-4,4)
        )

        self.add(axes, horizon, matter)

        # Cámara
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=30 * DEGREES,
            zoom=0.9
        )
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(1)

        # --------------------------------------------------
        # 1️⃣ COLAPSO VISTO DESDE INFINITO (CONGELACIÓN)
        # --------------------------------------------------

        self.play(
            R.animate.set_value(R_h + 0.05),
            run_time=6,
            rate_func=lambda t: 1 - np.exp(-6 * t)
        )

        self.wait(1)

        # --------------------------------------------------
        # 2️⃣ CRUCE REAL (TIEMPO PROPIO)
        # --------------------------------------------------

        self.play(
            R.animate.set_value(0.3),
            run_time=2,
            rate_func=linear
        )

        self.wait(2)


        
      
