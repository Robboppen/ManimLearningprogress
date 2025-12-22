from manim import *
import numpy as np

class SchwarzschildPresentation(ThreeDScene):
    def construct(self):
        # ==================================================
        # 1️⃣ TÍTULO
        # ==================================================
        title = Text(
            "Espacio-tiempo de Schwarzschild",
            font_size=48
        )
        subtitle = Text(
            "Colapso radial, horizonte y tiempo propio",
            font_size=32
        ).next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # ==================================================
        # 2️⃣ PARÁMETROS FÍSICOS
        # ==================================================
        R = ValueTracker(3.0)      # radio de la materia
        R_h = 1.5                  # horizonte (2M)

        t_ext = ValueTracker(0.0)  # tiempo externo
        tau = ValueTracker(0.0)    # tiempo propio

        # ==================================================
        # 3️⃣ OBJETOS 3D
        # ==================================================
        matter = always_redraw(
            lambda: Sphere(
                radius=R.get_value(),
                resolution=(24, 48),
                fill_color=BLUE_D,
                fill_opacity=0.6,
                stroke_width=0
            )
        )

        horizon = Sphere(
            radius=R_h,
            resolution=(24, 48),
            fill_color=RED,
            fill_opacity=0.18,
            stroke_width=0
        )

        self.add(horizon, matter)

        # Cámara
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=30 * DEGREES,
            zoom=0.9
        )
        self.begin_ambient_camera_rotation(rate=0.25)

        # ==================================================
        # 4️⃣ FÓRMULA EN PANTALLA
        # ==================================================
        formula = MathTex(
            r"\frac{d\tau}{dt}=\sqrt{1-\frac{2M}{r}}"
        )

        formula.fix_in_frame()
        formula.to_corner()

        self.play(FadeIn(formula))

        # ==================================================
        # 5️⃣ GRÁFICO τ(t)
        # ==================================================
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 4, 1],
            x_length=4,
            y_length=3,
            tips=False
        ).to_corner(DR)

        axes.fix_in_frame()

        

        labels = axes.get_axis_labels(
            MathTex("t"), MathTex(r"\tau")
        )

        graph = always_redraw(
            lambda: axes.plot(
                lambda x: tau.get_value(),
                x_range=[0, t_ext.get_value()],
                color=GREEN
            )
        )

        self.play(FadeIn(axes), FadeIn(labels))

        self.add_fixed_in_frame_mobjects(axes, labels, graph)

        # ==================================================
        # 6️⃣ RELOJES (MANECILLAS)
        # ==================================================
        def make_clock(tracker, label, color):
            face = Circle(radius=0.4)
            hand = always_redraw(
                lambda: Line(
                    face.get_center(),
                    face.get_center() + 0.35 * UP
                ).rotate(
                    -tracker.get_value(),
                    about_point=face.get_center()
                )
            )
            text = Text(label, font_size=22)
            group = VGroup(face, hand, text)
            text.next_to(face, DOWN)
            group.set_color(color)
            return group

        clock_t = make_clock(t_ext, "t externo", YELLOW).to_corner(UL)
        clock_tau = make_clock(tau, "τ propio", GREEN).next_to(clock_t, DOWN)

        self.add_fixed_in_frame_mobjects(clock_t, clock_tau)

        # ==================================================
        # 7️⃣ DINÁMICA TEMPORAL
        # ==================================================
        def clock_updater(dt):
            t_ext.increment_value(dt)

            r = max(R.get_value(), R_h + 1e-3)
            factor = np.sqrt(1 - R_h / r)
            tau.increment_value(factor * dt)

        self.add_updater(clock_updater)

        self.wait(1)

        # ==================================================
        # 8️⃣ COLAPSO CON CONGELACIÓN (OBSERVADOR EXTERNO)
        # ==================================================
        self.play(
            R.animate.set_value(R_h + 0.05),
            run_time=6,
            rate_func=lambda t: 1 - np.exp(-6 * t)
        )

        self.wait(1)

        # ==================================================
        # 9️⃣ CRUCE REAL (TIEMPO PROPIO)
        # ==================================================
        self.play(
            R.animate.set_value(0.3),
            run_time=2,
            rate_func=linear
        )

        self.wait(3)
