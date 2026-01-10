from manim import *
import numpy as np
# Deformación espacio tiempo para un agujero negro, con labels corregidos

class SpacetimeDeformation_bh(ThreeDScene):
    def construct(self):
        # Configurar la cámara en perspectiva inclinada
        self.set_camera_orientation(phi=80 * DEGREES, theta=-60 * DEGREES, distance=9)
        
        # Parámetros
        r_V = 2.5  # Radio de Schwarzschild (rojo)
        r_T = 4.5  # Radio exterior (amarillo)
        grid_size = 20

        # GROSOR MUY DELGADO desde el inicio
        GRID_STROKE_WIDTH = 2.9
        CIRCLE_STROKE_WIDTH = 6
        
        # Color azul más brillante e intenso para la grilla
        GRID_COLOR = "#00FFFF"  # Cyan puro, más brillante
        
        # FUNCIÓN DE DEFORMACIÓN MODIFICADA para permitir deformación hasta r_T
        def deformation_function(r, depth_factor, deformation_radius=r_V):
            """
            Deformación tipo agujero negro que crece desde el centro
            depth_factor controla la intensidad (0 = plano, 1 = máxima deformación)
            deformation_radius controla hasta dónde llega la deformación
            """
            if r >= deformation_radius:
                return 0
            elif r < 0.15:
                return -depth_factor * 7.0
            else:
                normalized = r / deformation_radius
                z = -depth_factor * 6.0 * (1 - normalized**2)**1.5 / (normalized**0.7 + 0.15)
                return z
        
        # CREAR GRILLA DEFORMADA con parámetro de profundidad y radio de deformación
        def create_deformed_grid(depth_factor=0.0, deformation_radius=r_V):
            lines = VGroup()
            for i in np.linspace(-grid_size, grid_size, 60):
                points1 = []
                points2 = []
                
                dist_from_center_i = abs(i) / grid_size
                opacity_i = 1.0 - (dist_from_center_i ** 1.5) * 0.7
                
                for j in np.linspace(-grid_size, grid_size, 120):
                    # Líneas en dirección x
                    r = np.sqrt(i**2 + j**2)
                    z = deformation_function(r, depth_factor, deformation_radius)
                    points1.append([i, j, z])
                    
                    # Líneas en dirección y
                    r = np.sqrt(j**2 + i**2)
                    z = deformation_function(r, depth_factor, deformation_radius)
                    points2.append([j, i, z])
                
                line1 = VMobject(color=GRID_COLOR, stroke_width=GRID_STROKE_WIDTH)
                line1.set_points_as_corners(points1)
                line1.set_stroke(opacity=opacity_i)
                
                line2 = VMobject(color=GRID_COLOR, stroke_width=GRID_STROKE_WIDTH)
                line2.set_points_as_corners(points2)
                line2.set_stroke(opacity=opacity_i)
                
                lines.add(line1, line2)
            return lines
        
        # CREAR SOMBRA con radio de deformación ajustable
        def create_grid_shadow(depth_factor=0.0, deformation_radius=r_V):
            """Crea una superficie que da efecto de sombra a la grilla"""
            if depth_factor < 0.01:
                return VGroup()
            
            surfaces = VGroup()
            resolution = 30
            
            for i in range(resolution):
                for j in range(resolution):
                    u1 = (i / resolution) * 2 - 1
                    v1 = (j / resolution) * 2 - 1
                    u2 = ((i + 1) / resolution) * 2 - 1
                    v2 = ((j + 1) / resolution) * 2 - 1
                    
                    x1, y1 = u1 * deformation_radius * 1.1, v1 * deformation_radius * 1.1
                    x2, y2 = u2 * deformation_radius * 1.1, v1 * deformation_radius * 1.1
                    x3, y3 = u2 * deformation_radius * 1.1, v2 * deformation_radius * 1.1
                    x4, y4 = u1 * deformation_radius * 1.1, v2 * deformation_radius * 1.1
                    
                    r1 = np.sqrt(x1**2 + y1**2)
                    r2 = np.sqrt(x2**2 + y2**2)
                    r3 = np.sqrt(x3**2 + y3**2)
                    r4 = np.sqrt(x4**2 + y4**2)
                    
                    if r1 < deformation_radius and r2 < deformation_radius and r3 < deformation_radius and r4 < deformation_radius:
                        z1 = deformation_function(r1, depth_factor, deformation_radius)
                        z2 = deformation_function(r2, depth_factor, deformation_radius)
                        z3 = deformation_function(r3, depth_factor, deformation_radius)
                        z4 = deformation_function(r4, depth_factor, deformation_radius)
                        
                        avg_depth = abs((z1 + z2 + z3 + z4) / 4)
                        shadow_opacity = min(0.25, avg_depth * 0.05)
                        
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
        
        def create_deformed_circle(radius, color, depth_factor=0.0, deformation_radius=r_V):
            points = []
            num_points = 120
            for i in range(num_points + 1):
                angle = i * TAU / num_points
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                r = radius
                
                z = deformation_function(r, depth_factor, deformation_radius)
                points.append([x, y, z])
            
            circle = VMobject(color=color, stroke_width=CIRCLE_STROKE_WIDTH)
            circle.set_points_as_corners(points)
            circle.set_stroke(opacity=1.0)
            return circle
        
        # Crear grilla inicial (plana, depth_factor=0)
        grid = create_deformed_grid(depth_factor=0.0)
        shadow = create_grid_shadow(depth_factor=0.0)
        circle_rV = create_deformed_circle(r_V, RED, depth_factor=0.0)
        circle_rT = create_deformed_circle(r_T, YELLOW, depth_factor=0.0)
        
        # Tracker para la profundidad actual (para calcular posición z de labels)
        current_depth = ValueTracker(0.0)
        
        # Punto central (esfera verde)
        center_dot = Dot3D(point=[0, 0, 0], color=BLACK, radius=0.5)
        center_dot.set(glow_factor=0.001)

        accretion_ring = Circle(radius=0.8, color=ORANGE, stroke_width=2)
        accretion_ring.set_stroke(opacity=0.8)
        
        # FASE 1: Mostrar estado inicial
        self.play(Create(grid), run_time=2.5)
        self.add(shadow)
        
        # Crear labels en espacio 3D con mayor énfasis visual
        label_rV = MathTex("r_V", color=RED, font_size=60).set_stroke(BLACK, width=3, background=True)
        label_rT = MathTex("r_T", color=YELLOW, font_size=60).set_stroke(BLACK, width=3, background=True)
        
        # Función para actualizar labels mirando a la cámara
        def update_label_rV(mob):
            z_pos = deformation_function(r_V, current_depth.get_value(), r_T)
            point_3d = np.array([r_V + 0.7, 0.5, z_pos + 0.5])
            point_2d = self.camera.project_point(point_3d)
            mob.move_to(point_2d)
        
        def update_label_rT(mob):
            z_pos = deformation_function(r_T, current_depth.get_value(), r_T)
            point_3d = np.array([r_T + 0.7, 0.8, z_pos + 0.5])
            point_2d = self.camera.project_point(point_3d)
            mob.move_to(point_2d)
        
        # Fijar labels al frame y agregar updaters
        self.add_fixed_in_frame_mobjects(label_rV, label_rT)
        label_rV.add_updater(update_label_rV)
        label_rT.add_updater(update_label_rT)
        
        self.play(
            Create(circle_rT),
            Create(circle_rV),
            Write(label_rT),
            Write(label_rV),
            run_time=2
        )
        self.play(
            FadeIn(center_dot, scale=0.3),
            Create(accretion_ring),
            run_time=1
        )
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
        
        # Crear línea geodésica que seguirá la curvatura del espacio-tiempo
        def create_geodesic_line(depth_factor=0.0, deformation_radius=r_V):
            """Crea una línea que sigue la curvatura del espacio-tiempo"""
            points = []
            num_points = 50
            for i in range(num_points + 1):
                t = i / num_points
                x = (r_V + t * (r_T - r_V)) * np.cos(angle_ref)
                y = (r_V + t * (r_T - r_V)) * np.sin(angle_ref)
                r = np.sqrt(x**2 + y**2)
                z = deformation_function(r, depth_factor, deformation_radius)
                points.append([x, y, z])
            
            line = VMobject(color=WHITE, stroke_width=4)
            line.set_points_as_corners(points)
            return line
        
        geodesic_line = create_geodesic_line(depth_factor=0.0, deformation_radius=r_V)
        
        # Label de distancia en espacio 3D (arriba de la línea geodésica)
        distance_label = MathTex("d", color=WHITE, font_size=65).set_stroke(BLACK, width=3, background=True)
        
        def update_distance_label(mob):
            # Posición 3D en el punto medio de la geodésica
            mid_r = (r_V + r_T) / 2
            z_pos = deformation_function(mid_r, 0.0, r_V)
            point_3d = np.array([mid_r * np.cos(angle_ref), mid_r * np.sin(angle_ref), z_pos + 0.8])
            point_2d = self.camera.project_point(point_3d)
            mob.move_to(point_2d)
        
        self.add_fixed_in_frame_mobjects(distance_label)
        distance_label.add_updater(update_distance_label)
        
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
        
        # FASE 4A: DEFORMACIÓN LEVE hasta r_T (circunferencia amarilla)
        depth_tracker_1 = ValueTracker(0.0)
        
        # Recrear la línea geodésica para la animación
        geodesic_line = create_geodesic_line(depth_factor=0.0, deformation_radius=r_T)
        self.add(geodesic_line)
        
        # Updaters para deformación hasta r_T
        def update_grid_phase1(mob):
            new_grid = create_deformed_grid(depth_factor=depth_tracker_1.get_value(), deformation_radius=r_T)
            mob.become(new_grid)
        
        def update_shadow_phase1(mob):
            new_shadow = create_grid_shadow(depth_factor=depth_tracker_1.get_value(), deformation_radius=r_T)
            mob.become(new_shadow)
        
        def update_circle_rV_phase1(mob):
            new_circle = create_deformed_circle(r_V, RED, depth_factor=depth_tracker_1.get_value(), deformation_radius=r_T)
            mob.become(new_circle)
        
        def update_circle_rT_phase1(mob):
            new_circle = create_deformed_circle(r_T, YELLOW, depth_factor=depth_tracker_1.get_value(), deformation_radius=r_T)
            mob.become(new_circle)
        
        def update_geodesic_phase1(mob):
            new_line = create_geodesic_line(depth_factor=depth_tracker_1.get_value(), deformation_radius=r_T)
            mob.become(new_line)
        
        def update_dot_rV_phase1(mob):
            z = deformation_function(r_V, depth_tracker_1.get_value(), deformation_radius=r_T)
            mob.move_to([r_V * np.cos(angle_ref), r_V * np.sin(angle_ref), z])
        
        def update_current_depth(mob):
            current_depth.set_value(depth_tracker_1.get_value())
        
        # Agregar updaters (incluyendo actualizar current_depth)
        grid.add_updater(update_grid_phase1)
        shadow.add_updater(update_shadow_phase1)
        circle_rV.add_updater(update_circle_rV_phase1)
        circle_rT.add_updater(update_circle_rT_phase1)
        geodesic_line.add_updater(update_geodesic_phase1)
        dot_rV.add_updater(update_dot_rV_phase1)
        
        # Crear objeto dummy para actualizar current_depth
        dummy = VMobject()
        dummy.add_updater(update_current_depth)
        self.add(dummy)
        
        # Deformación leve (30% de intensidad) hasta r_T
        self.play(
            depth_tracker_1.animate.set_value(0.3),
            run_time=2.5,
            rate_func=linear
        )
        
        # Remover updaters
        grid.clear_updaters()
        shadow.clear_updaters()
        circle_rV.clear_updaters()
        circle_rT.clear_updaters()
        geodesic_line.clear_updaters()
        dot_rV.clear_updaters()
        dummy.clear_updaters()
        self.remove(dummy)
        
        self.wait(1)
        
        # Mostrar label de distancia después de primera deformación
        distance_label_1 = MathTex("d_1", color=WHITE, font_size=65).set_stroke(BLACK, width=3, background=True)
        
        def update_distance_label_1(mob):
            mid_r = (r_V + r_T) / 2
            z_pos = deformation_function(mid_r, current_depth.get_value(), r_T)
            point_3d = np.array([mid_r * np.cos(angle_ref), mid_r * np.sin(angle_ref), z_pos + 0.8])
            point_2d = self.camera.project_point(point_3d)
            mob.move_to(point_2d)
        
        self.add_fixed_in_frame_mobjects(distance_label_1)
        distance_label_1.add_updater(update_distance_label_1)
        
        self.play(Write(distance_label_1), run_time=0.8)
        self.wait(1.5)
        
        # Ocultar label
        self.play(FadeOut(distance_label_1), run_time=0.5)
        distance_label_1.clear_updaters()
        self.wait(0.3)
        
        # Mostrar label de distancia después de segunda deformación
        distance_label_2 = MathTex("d_2", color=WHITE, font_size=65).set_stroke(BLACK, width=3, background=True)
        
        def update_distance_label_2(mob):
            mid_r = (r_V + r_T) / 2
            z_pos = deformation_function(mid_r, current_depth.get_value(), r_T)
            point_3d = np.array([mid_r * np.cos(angle_ref), mid_r * np.sin(angle_ref), z_pos + 0.8])
            point_2d = self.camera.project_point(point_3d)
            mob.move_to(point_2d)
        
        self.add_fixed_in_frame_mobjects(distance_label_2)
        distance_label_2.add_updater(update_distance_label_2)
        
        self.play(Write(distance_label_2), run_time=0.8)
        self.wait(1.5)
        
        # Ocultar label
        self.play(FadeOut(distance_label_2), run_time=0.5)
        distance_label_2.clear_updaters()
        
        # Fade out de los puntos y la línea geodésica
        self.play(
            FadeOut(dot_rV),
            FadeOut(dot_rT),
            FadeOut(geodesic_line),
            run_time=0.5
        )
        
        # Movimiento de cámara cinematográfico
        # 1. Acercarse mientras da una vuelta completa
        self.move_camera(
            phi=80 * DEGREES,
            theta=-60 * DEGREES + 360 * DEGREES,
            distance=6,
            run_time=4,
            rate_func=smooth
        )
        
        # 2. Pasar por el cenit (vista desde arriba)
        self.move_camera(
            phi=10 * DEGREES,
            theta=-60 * DEGREES + 360 * DEGREES + 180 * DEGREES,
            distance=6,
            run_time=3,
            rate_func=smooth
        )
        
        # 3. Volver a la posición original
        self.move_camera(
            phi=80 * DEGREES,
            theta=-60 * DEGREES,
            distance=9,
            run_time=3,
            rate_func=smooth
        )
        
        self.wait(2)