from material import Material
from plot import Plot
from model import Model
from mesh import Mesh
from math import pi, sin, cos

E = 100  # Young modulus.
rho = 1  # Material density.
v0 = 0.1  # Velocity amplitude.
L = 25  # Mesh length.
Le = 1  # Element length.
n = 1  # Vibration mode.


def v_ini(x):
    return v0 * sin(beta_n * x)


# Create material
material = Material(rho, E)

# Mode constants
beta_n = (pi / L) * (2 * n - 1) / 2
omega_n = beta_n * material.elastic_wave_speed()

# Create mesh.
mesh = Mesh(x_ini=0,
            x_final=25,
            num_els=25)

# Generate mesh with only one material.
mesh.generate_mesh(material)

# Create model
model = Model(mesh=mesh,
              num_particles_per_el=2,
              total_time=140)

# Initial conditions.
for p in model.particles:
    p.velocity = v_ini(p.x)

mesh.nodes[0].is_fixed = True

# Create Plot object.
plot = Plot(model)

# plot.plot_initial_structure()

# Analytical solution.
tv = model.discrete_time_steps()
va = []
for i in range(model.number_of_steps()):
    va.append(v0 * cos(omega_n * tv[i]) / (beta_n * L))

# Solve model.
model.solve()

# Plot results.
# plot.plot_velocity_result_in_center_of_mass(va)
plot.plot_velocity_error(va)
# plot.plot_position_result_in_center_of_mass()
# plot.animate_solution()
