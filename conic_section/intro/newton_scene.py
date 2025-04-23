from manim import *
import numpy as np

G = 1  # Gravitational constant (scaled)
M = 10  # Mass of the Sun (arbitrary but large)

# Time scaling: 1 second = 1 month
TIME_SCALE = 1 / 12

class NewtonOrbitScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Sun at origin
        sun = Sphere(radius=0.3, resolution=(24, 48), color=YELLOW).move_to(ORIGIN)
        self.add(sun)

        # Create a planet
        planet = Sphere(radius=0.1, resolution=(10, 20), color=BLUE)
        start_pos = np.array([4.0, 0.0, 0.0])  # Starting at perihelion
        planet.move_to(start_pos)

        # Initial velocity (perpendicular to radius, to make elliptical orbit)
        velocity = np.array([0.0, 1.5, 0.0])  # Tweak to get elliptical motion

        # Add orbit trail
        trail = TracedPath(planet.get_center, stroke_color=BLUE, stroke_width=1)
        self.add(trail)

        # Add force arrow (gravitational pull)
        force_arrow = always_redraw(lambda: Arrow3D(
            start=planet.get_center(),
            end=ORIGIN,
            color=RED,
            stroke_width=2,
            tip_length=0.2
        ))
        self.add(force_arrow)

        # Add and animate planet motion using basic physics integration
        def update_orbit(mob, dt):
            dt *= TIME_SCALE

            r_vec = -mob.get_center()
            r_mag = np.linalg.norm(r_vec)
            if r_mag == 0:
                return
            acc = G * M * r_vec / r_mag**3
            mob.velocity += acc * dt
            mob.move_to(mob.get_center() + mob.velocity * dt)

        planet.velocity = velocity
        planet.add_updater(update_orbit)

        self.add(planet)
      
