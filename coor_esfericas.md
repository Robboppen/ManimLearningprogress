# Coordenadas Esféricas en Manim

## Código Completo
```python
from manim import *


class Coor_esfericas(ThreeDScene):
    def construct(self):

        # ========================
        # Titulo
        # ========================

        title= Text(
            "Coordenadas esféricas.",
            font_size=48
        )

        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(3)
        self.play(FadeOut(title))


        #===========================
        #Parametros Físicos.
        # =======================
    

        sph_rad = 2.5 #radio de la esfera
        sph = Sphere(radius = sph_rad) #esfera 
        ax = ThreeDAxes() #ejes 
        base_plane = NumberPlane().shift(sph_rad * IN) 
        xyplane = VMobject(fill_color = BLUE, stroke_width = 1 / 4, fill_opacity = 7 / 8)
        xyplane.set_points_as_corners([5 * UL, 5 * UR, 5 * DR, 5 * DL, 5 * UL])
        self.add(ax)
        self.wait(2)

        self.play(Write(sph))
        self.wait(1)
        self.move_camera(phi = 60 * DEGREES, theta = 30 * DEGREES)
        self.wait(1)

        #self.play(sph.animate.set_style(fill_opacity = 1 / 8))

        pdot = Dot3D(sph_rad * OUT)
        pline = Line(ORIGIN, pdot.get_center())
        self.play(Write(pdot), Write(pline))
        self.wait()

        polar_grid = VGroup()
        circle_mesh = VGroup()
        nums = 4
        for k in range(1, nums + 1):
            rd = k * sph_rad / nums
            a = k * 90 * DEGREES / nums
            circle_mesh.add(
                Arc(radius = rd, stroke_width = 1 / 2),
                Line(ORIGIN, sph_rad * RIGHT, stroke_width = 1 / 2).rotate_about_origin(a)
            )
        #circle_mesh.set_color(GREY)
        polar_grid.add(circle_mesh.copy())
        polar_grid.add(circle_mesh.copy().rotate(90 * DEGREES, about_point = ORIGIN, axis = RIGHT))
        polar_grid.add(circle_mesh.copy().rotate(-90 * DEGREES, about_point = ORIGIN, axis = UP))
        #carc = Sector(outer_radius = sph_rad, fill_color = GREEN, fill_opacity = 1 / 2, stroke_width = 2)
        carc = VMobject(fill_color = BLUE, fill_opacity = 1 / 4, stroke_color = WHITE)
        cpts = [ORIGIN]
        for k in range(100 + 1):
            cpts += [sph_rad * np.cos(k * PI / 2 / 100) * RIGHT + sph_rad * np.sin(k * PI / 2 / 100) * UP]
        cpts += [ORIGIN]
        carc.set_points_as_corners(cpts)
        polar_grid.add(carc.copy())
        polar_grid.add(carc.copy().rotate(90 * DEGREES, about_point = ORIGIN, axis = RIGHT))
        polar_grid.add(carc.copy().rotate(-90 * DEGREES, about_point = ORIGIN, axis = UP))

        self.play(
            sph.animate.fade(7 / 8),
            FadeIn(polar_grid)
        )
        #self.move_camera(theta = 90 * DEGREES)
        self.wait()

        ta, pa = ValueTracker(0), ValueTracker(0)
        #pdot.add_updater(lambda m: m.restore().rotate().rotate())
        pdot.add_updater(lambda m: m.move_to(sph_rad * (np.cos(ta.get_value()) * OUT + np.sin(ta.get_value()) * np.cos(pa.get_value()) * RIGHT + np.sin(ta.get_value()) * np.sin(pa.get_value()) * UP)))
        pline.add_updater(lambda m: m.become(Line(ORIGIN, pdot.get_center())))
        self.add(pdot, pline)

        self.play(ta.animate.set_value(45 * DEGREES), run_time = 2)
        self.play(pa.animate.set_value(45 * DEGREES), run_time = 2)
        self.wait()

        xydot, xdot = Dot(sph_rad * np.sin(ta.get_value()) * (np.cos(pa.get_value()) * RIGHT + np.sin(pa.get_value()) * UP)), Dot(sph_rad * np.sin(ta.get_value() * np.cos(pa.get_value()) * RIGHT), fill_opacity = 0)
        zline = Line(pdot.get_center(), xydot.get_center(), color = GREY)
        yline = Line(xydot.get_center(), xdot.get_center(), color = GRAY)
        xyline = Line(ORIGIN, xydot.get_center(), color = GREY)
        
        self.play(Write(zline), Write(yline), Write(xyline), Write(xydot), Write(xdot))
        self.wait()

        xydot.add_updater(lambda m: m.move_to(sph_rad * np.sin(ta.get_value()) * (np.cos(pa.get_value()) * RIGHT + np.sin(pa.get_value()) * UP)))
        xdot.add_updater(lambda m: m.move_to(sph_rad * np.sin(ta.get_value() * np.cos(pa.get_value()) * RIGHT)))
        zline.add_updater(lambda m: m.become(Line(pdot.get_center(), xydot.get_center(), color = GREY)))
        yline.add_updater(lambda m: m.become(Line(xydot.get_center(), xdot.get_center(), color = GREY)))
        xyline.add_updater(lambda m: m.become(Line(ORIGIN, xydot.get_center(), color = GREY)))
        self.add(xydot, xdot, zline, yline, xyline)

        '''thet_ang, phi_ang = Anglet(pdot.get_center(), ORIGIN, OUT, color = GREEN), Anglet(xydot.get_center(), ORIGIN, xdot.get_center(), color = RED)
        self.play(Write(thet_ang), Write(phi_ang))
        thet_ang.add_updater(lambda m: m.become(Anglet(pdot.get_center(), ORIGIN, OUT, color = GREEN)))
        phi_ang.add_updater(lambda m: m.become(Anglet(xydot.get_center(), ORIGIN, xdot.get_center(), color = RED)))
        self.add(thet_ang, phi_ang)'''

        thet_circle = Circle(color = GREEN, radius = sph_rad).rotate_about_origin(PI / 2, axis = RIGHT).rotate_about_origin(pa.get_value())
        phi_circle = Circle(color = RED, radius = sph_rad * np.sin(ta.get_value())).shift(sph_rad * np.cos(ta.get_value()) * OUT)

        angle_defs = VGroup(
            MathTex("\\text{polar angle, }\\theta"),
            MathTex("\\text{azimuthal angle, }\\phi"),
        )
        angle_defs.arrange(DOWN)
        angle_defs[0][0][-1].set_color(GREEN)
        angle_defs[1][0][-1].set_color(RED)
        angle_defs.to_corner(UR)

        self.add_fixed_in_frame_mobjects(angle_defs[0])
        self.play(Write(thet_circle))
        self.wait()

        thet_circle.add_updater(lambda m: m.become(Circle(color = GREEN, radius = sph_rad).rotate_about_origin(PI / 2, axis = RIGHT).rotate_about_origin(pa.get_value())))
        self.add(thet_circle)

        self.move_camera(theta = -45 * DEGREES, phi = 90 * DEGREES)
        self.play(
            ta.animate.set_value(179 * DEGREES),
            run_time = 5, rate_func = there_and_back,
        )
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        self.wait()

        self.add_fixed_in_frame_mobjects(angle_defs[1])
        self.play(Write(phi_circle))
        phi_circle.add_updater(lambda m: m.become(Circle(color = RED, radius = sph_rad * np.sin(ta.get_value())).shift(sph_rad * np.cos(ta.get_value()) * OUT)))
        self.add(phi_circle)
        self.wait()

        self.move_camera(phi = 0 * DEGREES)
        self.play(pa.animate.increment_value(180 * DEGREES), run_time = 5, rate_func = there_and_back)
        self.move_camera(phi = 45 * DEGREES)
        self.wait()

        z_arclen = VGroup(
            MathTex("z = 1 + \\cos \\theta"),
            MathTex("ds^2 = d\\theta^2 + \\sin^2\\theta d\\phi^2")
        )
        z_arclen.arrange(DOWN)
        z_arclen[0][0][0].set_color(ORANGE)
        z_arclen[0][0][-1].set_color(GREEN)
        z_arclen[1][0][1].set_color(GOLD)
        z_arclen[1][0][5].set_color(GREEN)
        z_arclen[1][0][12].set_color(GREEN)
        z_arclen[1][0][14].set_color(RED)
        z_arclen.add_background_rectangle()

        z_arclen.to_corner(DR)

        linegp = VGroup(
            Line(sph_rad * DOWN, sph_rad * np.cos(ta.get_value()) * UP, color = ORANGE),
        )
        linegp.add(Brace(linegp[-1], LEFT))
        linegp.add(MathTex("1+\\cos\\theta").rotate_about_origin(90 * DEGREES).next_to(linegp[-1], LEFT))
        linegp[-1][0][-1].set_color(GREEN)
        linegp.add(Line(3 * LEFT + sph_rad * DOWN, 3 * RIGHT + sph_rad * DOWN))
        linegp.rotate_about_origin(90 * DEGREES, axis = RIGHT)
        linegp.rotate_about_origin(pa.get_value())
        linegp.add(Line(pdot.get_center(), linegp[0].get_end(), color = GREY))

        self.move_camera(theta = -PI / 2 + pa.get_value(), phi = 90 * DEGREES, run_time = 2)
        self.play(Write(linegp))
        self.add_fixed_in_frame_mobjects(z_arclen)
        self.wait()

        self.move_camera(theta = 15 * DEGREES, phi = 60 * DEGREES, run_time = 2)

        self.begin_ambient_camera_rotation(rate = 0.1)

        xydot.clear_updaters()
        xdot.clear_updaters()
        pdot.clear_updaters()
        pline.clear_updaters()
        zline.clear_updaters()
        yline.clear_updaters()
        xyline.clear_updaters()
        #thet_ang.clear_updaters()
        #phi_ang.clear_updaters()
        thet_circle.clear_updaters()
        phi_circle.clear_updaters()
        self.wait(10)
```
<p align="center"><img src ="vidios_gifs/vidios_gifs/Coor_esfericas_ManimCE_v0.19.1.gif" /></p>
---

## Explicación del Código

### Estructura General

Este código crea una animación educativa en 3D que visualiza el sistema de coordenadas esféricas usando la librería Manim. La clase `Coor_esfericas` hereda de `ThreeDScene`, lo que permite crear y manipular objetos en un espacio tridimensional.

### Secciones del Código

#### 1. Título (líneas 8-16)

Se crea y muestra un título que dice "Coordenadas esféricas". El título se fija al marco de la cámara para que permanezca visible independientemente de la rotación 3D, se escribe, permanece visible por 3 segundos y luego desaparece.

#### 2. Configuración Inicial de Objetos 3D (líneas 18-33)

Se definen los elementos básicos de la escena:
- `sph_rad = 2.5`: radio de la esfera principal
- `sph`: una esfera con el radio especificado
- `ax`: ejes tridimensionales cartesianos
- `base_plane` y `xyplane`: planos de referencia

La escena muestra primero los ejes, luego dibuja la esfera y finalmente mueve la cámara a una posición angular (phi=60°, theta=30°) para obtener una vista tridimensional clara.

#### 3. Punto y Línea Radial (líneas 35-39)

Se crea un punto (`pdot`) en la posición `(0, 0, sph_rad)` y una línea (`pline`) que va desde el origen hasta este punto. Estos elementos representan el vector de posición en coordenadas esféricas.

#### 4. Construcción de la Malla Polar (líneas 41-69)

Esta sección construye una cuadrícula polar compleja que ayuda a visualizar la geometría esférica:
- Se crean arcos concéntricos y líneas radiales
- Se generan sectores circulares con transparencia
- Todo se replica y rota en tres orientaciones diferentes para crear una red esférica completa
- La esfera original se vuelve semi-transparente para no obstruir la vista de la malla

#### 5. Sistema de Rastreadores y Actualización Dinámica (líneas 71-80)

Se introducen dos `ValueTracker`:
- `ta`: rastrea el ángulo polar θ (ángulo desde el eje z)
- `pa`: rastrea el ángulo azimutal φ (ángulo en el plano xy)

Se añaden actualizadores (updaters) al punto y la línea para que se muevan automáticamente según las fórmulas de conversión de coordenadas esféricas a cartesianas:
- x = r·sin(θ)·cos(φ)
- y = r·sin(θ)·sin(φ)
- z = r·cos(θ)

Luego se animan ambos ángulos hasta 45°.

#### 6. Proyecciones y Líneas Auxiliares (líneas 82-100)

Se crean varios elementos para mostrar las proyecciones del punto sobre diferentes planos:
- `xydot`: proyección del punto sobre el plano xy
- `xdot`: proyección sobre el eje x
- `zline`, `yline`, `xyline`: líneas que conectan estas proyecciones

Todos estos elementos también reciben actualizadores para moverse dinámicamente con los cambios en θ y φ.

#### 7. Visualización de Ángulos con Círculos (líneas 102-125)

Se crean dos círculos coloreados que representan los ángulos:
- **Círculo verde** (`thet_circle`): muestra el recorrido del ángulo polar θ
- **Círculo rojo** (`phi_circle`): muestra el recorrido del ángulo azimutal φ

Se añaden etiquetas de texto que identifican cada ángulo y se colorean coherentemente (verde para θ, rojo para φ).

La animación muestra cómo θ varía desde 0° hasta 179° y vuelve, con movimientos de cámara que permiten apreciar mejor cada ángulo.

#### 8. Animación del Ángulo Azimutal (líneas 127-134)

Similar a la sección anterior, pero enfocada en el ángulo φ. La cámara se mueve a una vista cenital (phi=0°) y se anima φ recorriendo 180° ida y vuelta.

#### 9. Fórmulas Matemáticas (líneas 136-163)

Se muestran dos ecuaciones importantes:
1. `z = 1 + cos θ`: una función de altura
2. `ds² = dθ² + sin²θ dφ²`: el elemento de línea (métrica) en coordenadas esféricas

Se crea también una representación visual de la altura `1 + cos θ` usando líneas, un bracket (corchete) y una etiqueta, todo rotado y posicionado adecuadamente en el espacio 3D.

#### 10. Finalización (líneas 165-180)

La animación concluye con:
- Un cambio de perspectiva de cámara
- Inicio de rotación ambiental continua (`begin_ambient_camera_rotation`) que hace girar la cámara lentamente alrededor de la escena
- Limpieza de todos los actualizadores para evitar cambios no deseados durante la rotación final
- Espera de 10 segundos mostrando la escena completa con la rotación

### Conceptos Clave de Coordenadas Esféricas

El código ilustra efectivamente que en coordenadas esféricas (r, θ, φ):
- **r**: es la distancia desde el origen (constante = 2.5 en este caso)
- **θ**: es el ángulo polar, medido desde el eje z positivo (0° a 180°)
- **φ**: es el ángulo azimutal, medido en el plano xy desde el eje x (0° a 360°)

La animación muestra cómo estos dos ángulos permiten ubicar cualquier punto sobre la superficie de una esfera y cómo se relacionan con las coordenadas cartesianas.