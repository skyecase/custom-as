from manim import *
import numpy as np

TIME_SCALE = 1 / 12

class KeplerOrbitScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        sun = Sphere(radius=0.3, resolution=(24, 48), color=YELLOW).move_to(ORIGIN)
        self.add(sun)

        planets = [
            {"name": "Earth", "a": 4, "e": 0.0167, "color": BLUE, "period": 12},     # 1 year
            {"name": "Mars", "a": 6, "e": 0.0934, "color": RED, "period": 22.7},    # 1.88 years
            {"name": "Jupiter", "a": 9, "e": 0.0489, "color": ORANGE, "period": 142} # 11.86 years
        ]

        for planet in planets:
            self.add_orbit(planet)

    def add_orbit(self, planet):
        a = planet["a"]
        e = planet["e"]
        b = a * np.sqrt(1 - e ** 2)
        f = a * e  # focal distance
        period = planet["period"]
        color = planet["color"]

        # Create the parametric orbit
        orbit = ParametricFunction(
            lambda t: np.array([
                a * np.cos(t) - f,  # Sun is at focus
                b * np.sin(t),
                0
            ]),
            t_range=[0, TAU],
            color=color,
            stroke_opacity=0.4
        )
        self.add(orbit)

        # Create the planet
        body = Sphere(radius=0.1, resolution=(10, 20), color=color)
        body.move_to(orbit.points[0])
        self.add(body)

        trail = TracedPath(body.get_center, stroke_color=color, stroke_width=1)
        self.add(trail)

        # Animate the orbit
        def update_pos(mob, dt):
            mob.time += dt * TIME_SCALE
            angle = (mob.time / period) * TAU
            mob.move_to(np.array([
                a * np.cos(angle) - f,
                b * np.sin(angle),
                0
            ]))
        
        body.time = 0
        body.add_updater(update_pos)

        self.add(body)

