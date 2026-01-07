# Visualización de Deformación del Espacio-Tiempo con Manim

## Código Completo

```python
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
        
        # ESTRELLA CENTRAL CON CORONA/LLAMAS
        # Núcleo de la estrella
        star_core = Sphere(
            radius=0.3,
            resolution=(30, 30)
        )
        star_core.set_color_by_gradient(WHITE, YELLOW, ORANGE)
        star_core.set_sheen(1.0, direction=UP)
        star_core.move_to([0, 0, 0])
        
        # Capas de resplandor (múltiples para efecto de profundidad)
        glow_layers = VGroup()
        glow_colors = [YELLOW, ORANGE, RED_E]
        glow_radii = [0.45, 0.6, 0.75]
        glow_opacities = [0.6, 0.4, 0.2]
        
        for i, (color, radius, opacity) in enumerate(zip(glow_colors, glow_radii, glow_opacities)):
            glow = Sphere(radius=radius, resolution=(20, 20))
            glow.set_color(color)
            glow.set_opacity(opacity)
            glow.move_to([0, 0, 0])
            glow_layers.add(glow)
        
        # Corona solar (anillo externo con "llamas")
        corona_particles = VGroup()
        num_flames = 16
        
        for i in range(num_flames):
            angle = i * TAU / num_flames
            # Variación aleatoria para hacer las llamas más naturales
            base_radius = 0.4
            height = 0.15 + np.random.random() * 0.15
            
            # Crear "llama" como un triángulo alargado
            flame = Polygon(
                [base_radius * np.cos(angle - 0.1), base_radius * np.sin(angle - 0.1), 0],
                [base_radius * np.cos(angle + 0.1), base_radius * np.sin(angle + 0.1), 0],
                [(base_radius + height) * np.cos(angle), (base_radius + height) * np.sin(angle), 0],
                color=ORANGE,
                fill_opacity=0.7,
                stroke_width=0
            )
            flame.set_color_by_gradient(YELLOW, ORANGE, RED)
            corona_particles.add(flame)
        
        # Agrupar toda la estrella
        star_system = VGroup(star_core, glow_layers, corona_particles)
        star_system.move_to([0, 0, 0])
        
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
        self.play(
            FadeIn(star_core, scale=0.3),
            FadeIn(glow_layers, scale=0.5),
            run_time=0.5
        )
        # Animar la aparición de las llamas
        self.play(
            LaggedStart(*[FadeIn(flame, scale=0.5) for flame in corona_particles], lag_ratio=0.05),
            run_time=0.8
        )
        self.wait(1)
        
        # FASE 2: Mostrar puntos en las circunferencias y LÍNEA GEODÉSICA
        angle_ref = 180 * DEGREES
        
        # Agregar updaters de animación continua a las llamas
        time_tracker = ValueTracker(0)
        
        def update_flames(mob, dt):
            time_tracker.increment_value(dt)
            t = time_tracker.get_value()
            for i, flame in enumerate(mob):
                # Cada llama pulsa con un offset de fase
                phase = i * TAU / len(mob)
                scale_factor = 1 + 0.15 * np.sin(3 * t + phase)
                opacity_factor = 0.6 + 0.2 * np.sin(3 * t + phase)
                
                # Mantener posición base pero variar escala
                angle = i * TAU / len(mob)
                base_radius = 0.4
                height = (0.15 + 0.08 * np.sin(2 * t + phase)) * scale_factor
                
                new_flame = Polygon(
                    [base_radius * np.cos(angle - 0.1), base_radius * np.sin(angle - 0.1), 0],
                    [base_radius * np.cos(angle + 0.1), base_radius * np.sin(angle + 0.1), 0],
                    [(base_radius + height) * np.cos(angle), (base_radius + height) * np.sin(angle), 0],
                    color=ORANGE,
                    fill_opacity=opacity_factor,
                    stroke_width=0
                )
                new_flame.set_color_by_gradient(YELLOW, ORANGE, RED)
                flame.become(new_flame)
        
        corona_particles.add_updater(update_flames)
        
        # Rotación del núcleo estelar
        star_core.add_updater(lambda m, dt: m.rotate(0.3 * dt, axis=UP))
        
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
        
        # Detener animaciones de la estrella al final
        corona_particles.clear_updaters()
        star_core.clear_updaters()
```

## Demo

https://github.com/user-attachments/assets/f480ce53-9b55-4725-9176-7928b5601a72





## Explicación del código

Este código crea una **visualización 3D de la deformación del espacio-tiempo** similar a lo que ocurre cerca de un agujero negro, utilizando la biblioteca Manim para animaciones matemáticas.

### Conceptos principales

**Función de deformación**: Simula cómo la gravedad curva el espacio-tiempo. El espacio permanece plano fuera del radio amarillo (r_T), se deforma sutilmente entre los radios amarillo y rojo (r_V), y tiene máxima curvatura en el centro (singularidad).

**Grilla deformable**: Una malla de líneas cyan que se curva según la función de deformación, permitiendo visualizar la curvatura del espacio.

**Estrella central**: Un objeto estelar compuesto por un núcleo esférico con capas de resplandor y llamas animadas que simulan una corona solar.

**Geodésica**: Una línea blanca que conecta dos puntos y se curva junto con el espacio, mostrando cómo la geometría afecta las distancias.

### Fases de la animación

1. **Inicialización**: Se crea la grilla plana con dos círculos (rojo y amarillo) y aparece la estrella central con su corona animada
2. **Geodésica inicial**: Se muestran dos puntos conectados por una línea geodésica recta (distancia "d")
3. **Rotación de cámara**: La cámara rota para ofrecer otra perspectiva de la escena
4. **Deformación del espacio-tiempo**: El espacio-tiempo se deforma gradualmente, curvando la grilla, los círculos y la geodésica
5. **Distancia curvada**: La distancia cambia de "d" a "d_curved" para mostrar cómo la gravedad afecta las mediciones
6. **Movimientos cinematográficos**: Varios movimientos de cámara para apreciar la deformación 3D desde diferentes ángulos

### Efectos visuales destacados

- **Sombras dinámicas**: Se generan superficies semitransparentes que crean sombras en las zonas más profundas de la deformación
- **Llamas pulsantes**: Las llamas de la corona solar tienen animaciones continuas que las hacen pulsar y variar en altura
- **Núcleo rotatorio**: El núcleo de la estrella rota continuamente para añadir dinamismo
- **Transiciones suaves**: Todas las deformaciones usan funciones de interpolación suaves para crear transiciones realistas
- **Opacidad variable**: Las líneas de la grilla más alejadas del centro tienen menor opacidad, creando sensación de profundidad