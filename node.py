from math import fabs
from particle import Particle


class Node:
    x: float
    is_fixed: bool
    mass: float
    force: float
    momentum: float

    def __init__(self, x: float, is_fixed: bool = False):
        """Constructor.

        :param x: Position.
        :param is_fixed: True if the node is constrained.
        """
        self.x = x
        self.is_fixed = is_fixed

        self.mass = 0
        self.force = 0
        self.momentum = 0

    def __str__(self):
        name = f"{self.__class__.__name__}"
        x = f"x={self.x}"
        v = f"velocity={self.velocity()}"
        m = f"mass={self.mass}"
        force = f"f={self.force}"
        momentum = f"momentum={self.momentum}"
        is_fixed = f"is_fixed={self.is_fixed}"

        return f"{name}({x}, {v}, {m}, {force}, {momentum}, {is_fixed})"

    def velocity(self) -> float:
        return self.momentum / self.mass

    @property
    def force(self) -> float:
        return self._force

    @force.setter
    def force(self, value):
        self._force = 0 if self.is_fixed else value

    @property
    def momentum(self) -> float:
        return self._momentum

    @momentum.setter
    def momentum(self, value):
        self._momentum = 0 if self.is_fixed else value

    def shape(self, xp: float, lx: float) -> float:
        if (self.x - lx) <= xp < (self.x + lx):
            return 1 - fabs(xp - self.x) / lx
        else:
            return 0

    def diff_shape(self, xp: float, lx: float) -> float:
        if (self.x - lx) <= xp < self.x:
            return 1 / lx
        elif self.x <= xp <= (self.x + lx):
            return -1 / lx
        else:
            return 0

    def map_mass_from_particle(self, particle: Particle, lx: float):
        """Increments the node mass with the contribution of the reference particle.

        :param particle: Reference particle.
        :param lx: Length of the reference element.
        """
        self.mass += self.shape(particle.x, lx) * particle.mass

    def map_momentum_from_particle(self, particle: Particle, lx: float):
        """Increments the node momentum with the contribution of the reference particle.

        :param particle: Reference particle
        :param lx: Length of the reference element.
        """
        self.momentum += self.shape(particle.x, lx) * particle.momentum()

    def map_force_from_particle(self, particle: Particle, lx: float):
        """Increments the node force with the contribution of the reference particle.

        :param particle: Reference particle
        :param lx: Length of the reference element.
        """
        self.force += -particle.stress * particle.current_volume * self.diff_shape(particle.x, lx)

    def update_momentum(self, dt: float):
        """Update the node momentum with explicit time integration."""
        self.momentum += self.force * dt

    def reset(self):
        """Reset values of momentum, mass, and force. Use once in each time step."""
        self.momentum = 0
        self.mass = 0
        self.force = 0
