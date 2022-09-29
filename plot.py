from model import Model
import matplotlib.pyplot as plt
import numpy as np


class Plot:
    def __init__(self, model: Model):
        self.model = model

    def plot_initial_structure(self):
        px = [p.x for p in self.model.particles]
        nx = [n.x for n in self.model.mesh.nodes]
        nx_fix = [n.x for n in self.model.mesh.nodes if n.is_fixed]

        fig = plt.figure()
        ax = fig.subplots()
        # ax.plot(nx, len(nx)*[0], color='gray')
        ax.scatter(px, len(px) * [0], color='orange', label='Particle')
        ax.scatter(nx, len(nx) * [0], color='black', label='Free node')
        ax.scatter(nx_fix, len(nx_fix) * [0], color='red', label='Fixed node')

        plt.legend()
        plt.show()

    def list_of_particle_in_time_step(self, i: int):
        return self.model.result[i]

    def time_steps(self) -> list[float]:
        n = self.model.number_of_steps()
        t = n * [0.0]
        for i in range(1, n):
            t[i] = t[i - 1] + self.model.dt

        return t

    def particles_velocities_in_center_of_mass(self) -> list[float]:
        total_mass = sum([p.mass for p in self.model.particles])
        n = self.model.number_of_steps()
        v = []
        for i in range(n):
            v.append(sum([p.velocity * p.mass / total_mass for p in self.list_of_particle_in_time_step(i)]))

        return v

    def particles_positions_in_center_of_mass(self):
        total_mass = sum([p.mass for p in self.model.particles])
        n = self.model.number_of_steps()
        x = []
        for i in range(n):
            x.append(sum([p.x * p.mass / total_mass for p in self.list_of_particle_in_time_step(i)]))

        return x

    def plot_velocity_result_in_center_of_mass(self, va: list[float] | None = None):
        v = self.particles_velocities_in_center_of_mass()
        t = self.time_steps()

        fig, ax = plt.subplots()

        if v is not None:
            ax.plot(t, va, label='Analytical', color='black')

        ax.scatter(t, v, s=10, label='MPM', color='orange')
        ax.set_ylabel('Velocity')
        ax.set_xlabel('Time (s)')
        ax.set_title('Velocity x Time')

        plt.legend()
        plt.show()

    def plot_position_result_in_center_of_mass(self, xa: list[float] | None = None):
        x = self.particles_positions_in_center_of_mass()
        t = self.time_steps()

        fig, ax = plt.subplots()

        if xa is not None:
            ax.plot(t, xa, label='Analytical', color='black')

        ax.scatter(t, x, s=10, label='MPM', color='orange')
        ax.set_ylabel('Position')
        ax.set_xlabel('Time (s)')
        ax.set_title('Position x Time')

        plt.show()

    def positions_particles_in_time_step(self, i: int) -> np.ndarray:
        """Return a vector of all particles in time step i"""
        return np.array([p.x for p in self.list_of_particle_in_time_step(i)])

    def max_displacement_animation(self, scale=60):
        xmax = -np.Inf
        x0 = self.positions_particles_in_time_step(0)
        for i in range(self.model.number_of_steps()):
            x = x0 + scale * (self.positions_particles_in_time_step(i) - x0)
            xmax = max(xmax, max(x))

        return xmax

    def animate_solution(self, scale=60):
        plt.ion()
        fig, ax = plt.subplots()
        x, y = [], []
        sc = ax.scatter(x, y)
        plt.xlim(self.model.mesh.x_ini, self.max_displacement_animation(scale))

        x0 = self.positions_particles_in_time_step(0)

        plt.draw()
        for i in range(self.model.number_of_steps()):
            x = x0 + scale * (self.positions_particles_in_time_step(i) - x0)
            y = np.zeros(len(x))

            sc.set_offsets(np.c_[x, y])
            fig.canvas.draw_idle()
            plt.pause(0.00001)

        plt.waitforbuttonpress()
