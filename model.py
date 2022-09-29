from mesh import Mesh
from particle import Particle
from element import Element
from math import sqrt, floor, ceil
from copy import deepcopy
import numpy as np


class Model:
    mesh: Mesh
    num_particles_per_el: int
    total_time: float
    dt: float
    particles: list[Particle]
    result: list[list[Particle]]

    def __init__(self, mesh: Mesh, num_particles_per_el: int, total_time: float):
        """Constructor.

        :param mesh: Mesh of domain.
        :param num_particles_per_el: Number of particles per element in the initial step.
        :param total_time: Total time of simulation
        """
        self.mesh = mesh
        self.num_particles_per_el = num_particles_per_el
        self.total_time = total_time

        self.dt = 0
        self.define_dt()

        self.particles = []

        self.result = []

        self.generate_particles()

    def generate_particles(self):
        """Generate particles inside every element."""
        for el in self.mesh.elements:
            dx = el.length() / (self.num_particles_per_el + 1)

            for i in range(self.num_particles_per_el):
                p = Particle(x=el.x_ini() + (i + 1) * dx,
                             mass=el.mass / self.num_particles_per_el,
                             volume=el.volume / self.num_particles_per_el,
                             material=el.material)

                self.particles.append(p)

    def element_that_contains_particle(self, particle: Particle) -> Element:
        """Return the element object that contains the reference particle.

        :param particle: Reference particle.
        """
        n = floor((particle.x - self.mesh.x_ini) / self.mesh.elements_length())
        return self.mesh.elements[n]

    def max_elastic_wave_speed(self) -> float:
        """Return the maximum elastic wave speed."""
        return max([el.material.elastic_wave_speed() for el in self.mesh.elements])

    def define_dt(self):
        """Compute the dt value."""
        self.dt = 0.1 * self.mesh.elements_length() / self.max_elastic_wave_speed()
        n = ceil(self.total_time / self.dt)
        self.dt = self.total_time / n

    def number_of_steps(self) -> int:
        """Return the number of time steps of solution."""
        return round(self.total_time / self.dt)

    def step_solve(self):
        """Solve with USL for one time step."""
        self.reset()
        # Shape functions and derivatives
        for p in self.particles:
            el = self.element_that_contains_particle(p)
            for n in el.nodes:
                n.map_mass_from_particle(p, el.length())
                n.map_momentum_from_particle(p, el.length())
                n.map_force_from_particle(p, el.length())

        # Update nodal momenta
        for n in self.mesh.nodes:
            n.update_momentum(self.dt)

        # Update particle velocity and position
        for p in self.particles:
            el = self.element_that_contains_particle(p)

            for n in el.nodes:
                p.update_velocity_from_node(node_shape=n.shape(p.x, el.length()),
                                            node_force=n.force,
                                            node_mass=n.mass,
                                            dt=self.dt)

                p.update_position_from_node(node_shape=n.shape(p.x, el.length()),
                                            node_momentum=n.momentum,
                                            node_mass=n.mass,
                                            dt=self.dt)

        # Stress update
        for p in self.particles:
            el = self.element_that_contains_particle(p)

            for n in el.nodes:
                # n.update_velocity_from_particle(p, el.length())
                p.update_velocity_gradient(n.diff_shape(p.x, el.length()), n.velocity())

            p.update_deformation_gradient(self.dt)
            p.update_volume()
            p.update_strain_increment(self.dt)
            p.update_stress()

    def solve(self):
        """Solve the problem for each time step"""
        n_steps = round(self.total_time / self.dt)

        for t in self.discrete_time_steps():
            self.step_solve()

            self.result.append(deepcopy(self.particles))

            print(f't:{t:.4f}s\tprogress:{100 * t / self.total_time:.2f}%')

    def reset(self):
        """Reset some properties of all elements. Use once for time step."""
        self.mesh.reset()

        for p in self.particles:
            p.reset()

    def discrete_time_steps(self) -> np.ndarray:
        """Return a vector with all time steps."""
        return np.linspace(0, self.total_time, self.number_of_steps())
