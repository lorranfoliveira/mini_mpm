from material import Material
from plot import Plot
from model import Model
from mesh import Mesh
from math import pi, sqrt, cos

E = 4 * pi ** 2  # Young modulus.
rho = 1  # Material density.
v0 = 0.1  # Amplitude of velocity.
L = 1  # Model length.

# Create material.
material = Material(density=rho,
                    young=E)

omega = sqrt(material.young / material.rho) / L

# Create mesh.
mesh = Mesh(x_ini=0,
            x_final=1,
            num_els=1)

# Generate the mesh with only one material for all elements.
mesh.generate_mesh(material=material)

# Create model.
model = Model(mesh=mesh,
              num_particles_per_el=1,
              total_time=10)

# Initial conditions.
model.particles[0].velocity = 0.1
mesh.nodes[0].is_fixed = True

# Model plot.
plot = Plot(model)
# plot.plot_initial_structure()

# Solve model.
model.solve()

# Analytical solution.
tv = model.discrete_time_steps()
va = []
for i in range(model.number_of_steps()):
    va.append(v0 * cos(omega * tv[i]))

# Plot results.
plot.plot_velocity_result_in_center_of_mass(va)
# plot.plot_position_result_in_center_of_mass()
# plot.animate_solution()
