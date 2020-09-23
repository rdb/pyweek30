import random

from panda3d import core
from direct.interval.LerpInterval import *

from .planet import PlanetObject
from .procgen import asteroid


MIN_B = 0.03
MAX_B = 0.3


class Asteroid(PlanetObject):
    def __init__(self, planet):
        super().__init__(planet)
        bounds = core.Vec3(*(random.uniform(MIN_B, MAX_B) for _ in range(3)))
        color1 = core.Vec3(random.uniform(0.05, 0.25))
        color2 = color1 * random.uniform(0.3, 0.9)
        node = asteroid.generate(bounds, color1, color2, random.uniform(5.2, 9.5))
        baserot = self.root.attach_new_node('Base Rotation')
        baserot.set_hpr(random.randrange(360), random.randrange(-90, 90), 0)
        self.rotation = baserot.attach_new_node('Rotation')
        self.rotation.set_pos(0, 0, -1)
        self.asteroid = self.rotation.attach_new_node(node)
        self.asteroid.set_pos(
            planet.size * random.uniform(2.0, 5.0),
            planet.size * random.uniform(2.0, 5.0),
            0
        )
        mat = core.Material()
        mat.set_roughness(1)
        self.asteroid.set_material(mat)

        self._orbit_ival = LerpHprInterval(self.rotation, 10.0, (360, 0, 0))
        self._spin_ival = LerpHprInterval(self.asteroid, 3.0, (360, 360, 0))

        self._orbit_ival.loop()
        self._spin_ival.loop()

        collide = core.CollisionNode('asteroid')
        collide.add_solid(core.CollisionSphere(center=(0, 0, 0), radius=0.3))
        collide.set_into_collide_mask(0b0100)
        collide.set_from_collide_mask(0b0000)
        collide = self.asteroid.attach_new_node(collide)
        collide.set_python_tag('asteroid', self)

    def destroy(self):
        self.asteroid.remove_node()
        super().destroy()

    def stop(self):
        self._orbit_ival.pause()
        self._spin_ival.pause()
