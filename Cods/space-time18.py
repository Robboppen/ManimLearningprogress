from manim import *
import numpy as np

class SpacetimeDeformation(ThreeDScene):
    def construct(self):
        # Configurar la cámara en perspectiva inclinada
        self.set_camera_orientation(phi=80 * DEGREES, theta=-60 * DEGREES, distance=9)
        
        # Parámetros
        r_V = 2.5  # Radio de Schwarzschild (rojo)
        r_T = 4.5  # Radio exterior (amarillo)
        grid_size = 15
        
        GRID_STROKE_WIDTH = 0.6
        CIRCLE_STROKE_WIDTH = 6
        GRID_COLOR = "#00FFFF"
        
        # FUNCIÓN DE DEFORMACIÓN MEJORADA - MÁS SUTIL Y GRADUAL
        def deformation_function(r, depth_factor):
            """
            Deformación tipo agujero negro SUTIL:
            - Fuera de r_T (amarillo): z=0 (SIN deformación)
            - Entre r_T y r_V: deformación muy sutil
            - Dentro de r_V (rojo): deformación gradual desde el borde hacia el centro
            - La máxima deformación está solo en el centro (singularidad)
            """
            if r >= r_T:
                # Fuera de la circunferencia amarilla: plano
                return 0
            elif r >= r_V:
                # Entre r_T (amarillo) y r_V (rojo): transición muy sutil
                t = (r_T - r) / (r_T - r_V)
                intensity = t**2.5  # Muy suave
                z_at_rV = -depth_factor * 0.3  # Muy sutil en el borde rojo
                return z_at_rV * intensity
            else:
                # Dentro de r_V (rojo): deformación gradual hacia el centro
                if r < 0.05:
                    # Singularidad central - máxima deformación
                    return -depth_factor * 3.5
                else:
                    # Deformación que crece gradualmente desde r_V hacia el centro
                    # Normalizar: 1 en el borde de r_V, 0 en el centro
                    normalized = r / r_V
                    
                    # En el borde de r_V: deformación muy sutil
                    z_at_rV = -depth_factor * 0.3
                    
                    # En el centro: deformación máxima
                    z_center = -depth_factor * 3.5
                    
                    # Interpolación suave: usa función exponencial para transición gradual
                    # Cuando normalized = 1 (borde r_V): intensity = 0
                    # Cuando normalized = 0 (centro): intensity = 1
                    intensity = 1 - normalized**0.6
                    
                    z = z_at_rV + (z_center - z_at_rV) * intensity
                    
                    return z
        
        # CREAR GRILLA DEFORMADA
        def create_deformed_grid(depth_factor=0.0):
            lines = VGroup()
            for i in np.linspace(-grid_size, grid_size, 60):
                points1 = []
                points2 = []
                
                dist_from_center_i = abs(i) / grid_size
                opacity_i = 1.0 - (dist_from_center_i ** 1.5) * 0.7
                
                for j in np.linspace(-grid_size, grid_size, 120):
                    r = np.sqrt(i**2 + j**2)
                    z = deformation_function(r, depth_factor)
                    points1.append([i, j, z])
                    
                    r = np.sqrt(j**2 + i**2)
                    z = deformation_function(r, depth_factor)
                    points2.append([j, i, z])
                
                line1 = VMobject(color=GRID_COLOR, stroke_width=GRID_STROKE_WIDTH)
                line1.set_points_as_corners(points1)
                line1.set_stroke(opacity=opacity_i)
                
                line2 = VMobject(color=GRID_COLOR, stroke_width=GRID_STROKE_WIDTH)
                line2.set_points_as_corners(points2)
                line2.set_stroke(opacity=opacity_i)
                
                lines.add(line1, line2)
            return lines
        
        # CREAR SOMBRA
        def create_grid_shadow(depth_factor=0.0):
            if depth_factor < 0.01:
                return VGroup()
            
            surfaces = VGroup()
            resolution = 35
            
            for i in range(resolution):
                for j in range(resolution):
                    u1 = (i / resolution) * 2 - 1
                    v1 = (j / resolution) * 2 - 1
                    u2 = ((i + 1) / resolution) * 2 - 1
                    v2 = ((j + 1) / resolution) * 2 - 1
                    
                    x1, y1 = u1 * r_T * 1.2, v1 * r_T * 1.2
                    x2, y2 = u2 * r_T * 1.2, v1 * r_T * 1.2
                    x3, y3 = u2 * r_T * 1.2, v2 * r_T * 1.2
                    x4, y4 = u1 * r_T * 1.2, v2 * r_T * 1.2
                    
                    r1 = np.sqrt(x1**2 + y1**2)
                    r2 = np.sqrt(x2**2 + y2**2)
                    r3 = np.sqrt(x3**2 + y3**2)
                    r4 = np.sqrt(x4**2 + y4**2)
                    
                    z1 = deformation_function(r1, depth_factor)
                    z2 = deformation_function(r2, depth_factor)
                    z3 = deformation_function(r3, depth_factor)
                    z4 = deformation_function(r4, depth_factor)
                    
                    avg_depth = abs((z1 + z2 + z3 + z4) / 4)
                    shadow_opacity = min(0.45, avg_depth * 0.15)
                    
                    quad = Polygon(
                        [x1, y1, z1],
                        [x2, y2, z2],
                        [x3, y3, z3],
                        [x4, y4, z4],
                        color=BLUE_E,
                        fill_opacity=shadow_opacity,
                        stroke_width=0
                    )
                    surfaces.add(quad)
            
            return surfaces
        
        def create_deformed_circle(radius, color, depth_factor=0.0):
            points = []
            num_points = 120
            for i in range(num_points + 1):
                angle = i * TAU / num_points
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                
                z = deformation_function(radius, depth_factor)
                points.append([x, y, z])
            
            circle = VMobject(color=color, stroke_width=CIRCLE_STROKE_WIDTH)
            circle.set_points_as_corners(points)
            circle.set_stroke(opacity=1.0)
            return circle
        
        # Crear elementos iniciales
        grid = create_deformed_grid(depth_factor=0.0)
        shadow = create_grid_shadow(depth_factor=0.0)
        circle_rV = create_deformed_circle(r_V, RED, depth_factor=0.0)
        circle_rT = create_deformed_circle(r_T, YELLOW, depth_factor=0.0)
        
        # Labels
        label_rV = MathTex("r_V", color=RED, font_size=48).move_to([r_V + 0.7, 0.5, 0])
        label_rT = MathTex("r_T", color=YELLOW, font_size=48).move_to([r_T + 0.7, 0.8, 0])
        
        # Singularidad central
        center_dot = Dot3D(point=[0, 0, 0], color=GREEN, radius=0.25)
        center_dot.set(glow_factor=1.5)
        
        # FASE 1: Mostrar estado inicial
        self.play(Create(grid), run_time=2.5)
        self.add(shadow)
        self.play(
            Create(circle_rT),
            Create(circle_rV),
            Write(label_rT),
            Write(label_rV),
            run_time=2
        )
        self.play(FadeIn(center_dot, scale=0.3), run_time=0.5)
        self.wait(1)
        
        # FASE 2: Mostrar puntos en las circunferencias y LÍNEA GEODÉSICA
        angle_ref = 180 * DEGREES
        
        dot_rV = Dot3D(
            point=[r_V * np.cos(angle_ref), r_V * np.sin(angle_ref), 0],
            color=RED,
            radius=0.18
        )
        dot_rV.set(glow_factor=1.2)
        
        dot_rT = Dot3D(
            point=[r_T * np.cos(angle_ref), r_T * np.sin(angle_ref), 0],
            color=YELLOW,
            radius=0.18
        )
        dot_rT.set(glow_factor=1.2)
        
        def create_geodesic_line(depth_factor=0.0):
            points = []
            num_points = 50
            for i in range(num_points + 1):
                t = i / num_points
                x = (r_V + t * (r_T - r_V)) * np.cos(angle_ref)
                y = (r_V + t * (r_T - r_V)) * np.sin(angle_ref)
                r = np.sqrt(x**2 + y**2)
                z = deformation_function(r, depth_factor)
                points.append([x, y, z])
            
            line = VMobject(color=WHITE, stroke_width=4)
            line.set_points_as_corners(points)
            return line
        
        geodesic_line = create_geodesic_line(depth_factor=0.0)
        distance_label = MathTex("d", color=WHITE, font_size=50).move_to([-4.0, 0.3, 0])
        
        self.play(
            FadeIn(dot_rV, scale=0.3),
            FadeIn(dot_rT, scale=0.3),
            Create(geodesic_line),
            Write(distance_label),
            run_time=1.5
        )
        self.wait(1)
        
        # FASE 3: Rotación
        self.move_camera(theta=-410 * DEGREES, run_time=3, rate_func=smooth)
        self.wait(0.5)
        
        self.play(
            FadeOut(geodesic_line),
            FadeOut(distance_label),
            run_time=0.5
        )
        self.wait(0.3)
        
        # FASE 4: DEFORMACIÓN GRADUAL
        depth_tracker = ValueTracker(0.0)
        geodesic_line = create_geodesic_line(depth_factor=0.0)
        self.add(geodesic_line)
        
        # Updaters
        def update_grid(mob):
            new_grid = create_deformed_grid(depth_factor=depth_tracker.get_value())
            mob.become(new_grid)
        
        def update_shadow(mob):
            new_shadow = create_grid_shadow(depth_factor=depth_tracker.get_value())
            mob.become(new_shadow)
        
        def update_circle_rV(mob):
            new_circle = create_deformed_circle(r_V, RED, depth_factor=depth_tracker.get_value())
            mob.become(new_circle)
        
        def update_circle_rT(mob):
            new_circle = create_deformed_circle(r_T, YELLOW, depth_factor=depth_tracker.get_value())
            mob.become(new_circle)
        
        def update_geodesic(mob):
            new_line = create_geodesic_line(depth_factor=depth_tracker.get_value())
            mob.become(new_line)
        
        def update_dot_rV(mob):
            z = deformation_function(r_V, depth_tracker.get_value())
            mob.move_to([r_V * np.cos(angle_ref), r_V * np.sin(angle_ref), z])
        
        # NO agregar updater al centro - permanece fijo en z=0
        
        # Agregar updaters
        grid.add_updater(update_grid)
        shadow.add_updater(update_shadow)
        circle_rV.add_updater(update_circle_rV)
        circle_rT.add_updater(update_circle_rT)
        geodesic_line.add_updater(update_geodesic)
        dot_rV.add_updater(update_dot_rV)
        
        # Deformación
        self.play(
            depth_tracker.animate.set_value(1.0),
            run_time=4.5,
            rate_func=linear
        )
        
        # Remover updaters (centro no tiene updater, se mantiene fijo)
        grid.clear_updaters()
        shadow.clear_updaters()
        circle_rV.clear_updaters()
        circle_rT.clear_updaters()
        geodesic_line.clear_updaters()
        dot_rV.clear_updaters()
        
        self.wait(1)
        
        # Label final
        distance_label_final = MathTex("d_{curved}", color=WHITE, font_size=50).move_to([-4.0, 0.3, 0])
        self.play(Write(distance_label_final), run_time=0.8)
        self.wait(1.5)
        
        self.play(FadeOut(distance_label_final), run_time=0.5)
        
        # Fade out
        self.play(
            FadeOut(dot_rV),
            FadeOut(dot_rT),
            FadeOut(geodesic_line),
            run_time=0.5
        )
        
        # Movimiento de cámara cinematográfico
        self.move_camera(
            phi=80 * DEGREES,
            theta=-60 * DEGREES + 360 * DEGREES,
            distance=6,
            run_time=4,
            rate_func=smooth
        )
        
        self.move_camera(
            phi=10 * DEGREES,
            theta=-60 * DEGREES + 360 * DEGREES + 180 * DEGREES,
            distance=6,
            run_time=3,
            rate_func=smooth
        )
        
        self.move_camera(
            phi=80 * DEGREES,
            theta=-60 * DEGREES,
            distance=9,
            run_time=3,
            rate_func=smooth
        )
        
        self.wait(2)