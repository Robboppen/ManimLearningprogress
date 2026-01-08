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


