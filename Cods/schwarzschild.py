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

        self.add_fixed_in_frame_mobjects(title, subtitle)
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
        # 3️⃣ OBJETOS 3D - ESFERA Y HORIZONTE
        # ==================================================
        matter = always_redraw(
            lambda: Sphere(
                radius=R.get_value(),
                resolution=(24, 48),
                fill_color=BLUE_D,
                fill_opacity=0.7,
                stroke_width=0
            )
        )

        horizon = Sphere(
            radius=R_h,
            resolution=(24, 48),
            fill_color=RED,
            fill_opacity=0.2,
            stroke_width=1,
            stroke_color=RED
        )

        # ==================================================
        # 🌀 CURVATURA DEL ESPACIO-TIEMPO (GRILLA DEFORMADA)
        # ==================================================
        def create_curved_grid():
            grid_group = VGroup()
            
            # Círculos concéntricos deformados por la curvatura
            for i in range(1, 8):
                r_nominal = i * 0.8
                
                # Factor de curvatura: más deformación cerca del horizonte
                if r_nominal > R_h:
                    curvature_factor = 1 + 0.3 * (R_h / r_nominal)**2
                else:
                    curvature_factor = 1.5
                
                r_curved = r_nominal * curvature_factor
                
                circle = Circle(
                    radius=r_curved,
                    color=BLUE_E if r_nominal > R_h else RED_E,
                    stroke_width=1,
                    stroke_opacity=0.4 if r_nominal > R_h else 0.6
                )
                grid_group.add(circle)
            
            # Líneas radiales
            for angle in np.linspace(0, 2*PI, 16, endpoint=False):
                line = Line(
                    ORIGIN,
                    6 * np.array([np.cos(angle), np.sin(angle), 0]),
                    color=BLUE_E,
                    stroke_width=0.8,
                    stroke_opacity=0.3
                )
                grid_group.add(line)
            
            return grid_group

        curved_grid = always_redraw(create_curved_grid)
        curved_grid.rotate(90*DEGREES, axis=RIGHT)  # Hacerla horizontal
        
        self.add(curved_grid, horizon, matter)

        # Cámara
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=30 * DEGREES,
            zoom=0.9
        )
        self.begin_ambient_camera_rotation(rate=0.2)

        # ==================================================
        # 4️⃣ FÓRMULA EN PANTALLA (FIJA, SIN ROTAR)
        # ==================================================
        formula_box = VGroup(
            MathTex(
                r"\frac{d\tau}{dt}=\sqrt{1-\frac{2M}{r}}",
                font_size=40
            ),
            MathTex(
                r"R_\text{horizonte} = 2M",
                font_size=32
            ).shift(DOWN*0.6)
        ).arrange(DOWN, buff=0.3)
        
        formula_bg = BackgroundRectangle(
            formula_box,
            color=BLACK,
            fill_opacity=0.7,
            buff=0.2
        )
        
        formula_group = VGroup(formula_bg, formula_box).to_corner(UL)
        
        self.add_fixed_in_frame_mobjects(formula_group)
        self.play(FadeIn(formula_group))

        # ==================================================
        # 5️⃣ GRÁFICO τ(t) - FIJO EN PANTALLA
        # ==================================================
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 5, 1],
            x_length=4.5,
            y_length=3,
            tips=False,
            axis_config={"color": GREY}
        ).to_corner(DR).shift(LEFT*0.3 + UP*0.3)

        labels = axes.get_axis_labels(
            MathTex("t", color=YELLOW), 
            MathTex(r"\tau", color=GREEN)
        )

        # Línea del gráfico con historial
        graph_dots = VGroup()
        
        def update_graph(mob):
            if t_ext.get_value() > 0:
                new_dot = Dot(
                    axes.c2p(t_ext.get_value(), tau.get_value()),
                    radius=0.02,
                    color=GREEN
                )
                mob.add(new_dot)
                # Limitar número de puntos para performance
                if len(mob) > 200:
                    mob.remove(mob[0])
        
        graph_dots.add_updater(update_graph)

        axes_bg = BackgroundRectangle(
            VGroup(axes, labels),
            color=BLACK,
            fill_opacity=0.7,
            buff=0.2
        )

        self.add_fixed_in_frame_mobjects(axes_bg, axes, labels, graph_dots)
        self.play(FadeIn(axes_bg), FadeIn(axes), FadeIn(labels))

        # ==================================================
        # 6️⃣ RELOJES (MANECILLAS) - FIJOS EN PANTALLA
        # ==================================================
        def make_clock(tracker, label, color):
            face = Circle(radius=0.4, color=color, stroke_width=2)
            center_dot = Dot(face.get_center(), radius=0.03, color=color)
            hand = always_redraw(
                lambda: Line(
                    face.get_center(),
                    face.get_center() + 0.3 * UP,
                    color=color,
                    stroke_width=3
                ).rotate(
                    -tracker.get_value() * 0.5,  # Escalar para visualización
                    about_point=face.get_center()
                )
            )
            text = Text(label, font_size=20, color=color)
            group = VGroup(face, center_dot, hand, text)
            text.next_to(face, DOWN, buff=0.15)
            return group

        clock_t = make_clock(t_ext, "t externo", YELLOW).to_corner(UL).shift(DOWN*2.5)
        clock_tau = make_clock(tau, "τ propio", GREEN).next_to(clock_t, RIGHT, buff=1)

        clock_bg = BackgroundRectangle(
            VGroup(clock_t, clock_tau),
            color=BLACK,
            fill_opacity=0.7,
            buff=0.15
        )

        self.add_fixed_in_frame_mobjects(clock_bg, clock_t, clock_tau)
        self.play(FadeIn(clock_bg), FadeIn(clock_t), FadeIn(clock_tau))

        # ==================================================
        # 7️⃣ INDICADOR DE RADIO ACTUAL
        # ==================================================
        radius_label = always_redraw(
            lambda: MathTex(
                f"r = {R.get_value():.2f}M",
                font_size=32,
                color=BLUE_B
            ).to_corner(UR).shift(LEFT*0.5 + DOWN*0.5)
        )
        
        radius_bg = always_redraw(
            lambda: BackgroundRectangle(
                radius_label,
                color=BLACK,
                fill_opacity=0.7,
                buff=0.15
            )
        )
        
        self.add_fixed_in_frame_mobjects(radius_bg, radius_label)
        self.play(FadeIn(radius_bg), FadeIn(radius_label))

        # ==================================================
        # 8️⃣ DINÁMICA TEMPORAL (CORREGIDA)
        # ==================================================
        class ClockUpdater:
            def __init__(self):
                self.last_time = 0
            
            def __call__(self, mob, dt):
                t_ext.increment_value(dt * 0.5)  # Escalar para mejor visualización
                
                r = max(R.get_value(), R_h + 1e-3)
                factor = np.sqrt(max(0, 1 - R_h / r))
                tau.increment_value(factor * dt * 0.5)

        # Usamos un objeto dummy para el updater
        dummy = Dot(ORIGIN, radius=0)
        dummy.add_updater(ClockUpdater())
        self.add(dummy)

        self.wait(2)

        # ==================================================
        # 9️⃣ COLAPSO CON CONGELACIÓN (OBSERVADOR EXTERNO)
        # ==================================================
        freeze_text = Text(
            "Vista del observador externo:\nse congela en el horizonte",
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN)
        freeze_bg = BackgroundRectangle(freeze_text, color=BLACK, fill_opacity=0.8, buff=0.2)
        
        self.add_fixed_in_frame_mobjects(freeze_bg, freeze_text)
        self.play(FadeIn(freeze_bg), FadeIn(freeze_text))
        
        self.play(
            R.animate.set_value(R_h + 0.05),
            run_time=8,
            rate_func=lambda t: 1 - np.exp(-4 * t)
        )

        self.wait(2)
        self.play(FadeOut(freeze_text), FadeOut(freeze_bg))

        # ==================================================
        # 🔟 CRUCE REAL (TIEMPO PROPIO)
        # ==================================================
        cross_text = Text(
            "Para el observador cayendo:\ncruza el horizonte normalmente",
            font_size=28,
            color=GREEN
        ).to_edge(DOWN)
        cross_bg = BackgroundRectangle(cross_text, color=BLACK, fill_opacity=0.8, buff=0.2)
        
        self.add_fixed_in_frame_mobjects(cross_bg, cross_text)
        self.play(FadeIn(cross_bg), FadeIn(cross_text))
        
        self.play(
            R.animate.set_value(0.3),
            run_time=3,
            rate_func=linear
        )

        self.wait(3)
        
        # Mensaje final
        final_text = Text(
            "La singularidad es inevitable",
            font_size=36,
            color=RED
        )
        final_bg = BackgroundRectangle(final_text, color=BLACK, fill_opacity=0.9, buff=0.3)
        
        self.add_fixed_in_frame_mobjects(final_bg, final_text)
        self.play(
            FadeOut(cross_text), FadeOut(cross_bg),
            FadeIn(final_bg), FadeIn(final_text)
        )
        self.wait(3)