from material import Material


class Particle:
    x: float
    velocity: float
    mass: float
    initial_volume: float
    current_volume: float
    material: Material
    stress: float
    force: float
    velocity_gradient: float
    deformation_gradient: float
    strain: float

    def __init__(self, x: float, velocity: float = 0, mass: float = 0, volume: float = 0, material: Material = None):
        """Constructor.

        :param x: Position.
        :param velocity: Velocity.
        :param mass: Mass.
        :param volume: Initial volume.
        :param material: Material.
        """
        self.x = x
        self.velocity = velocity
        self.mass = mass
        self.initial_volume = volume
        self.current_volume = volume
        self.material = material

        self.stress = 0
        self.force = 0
        self.velocity_gradient = 0
        self.deformation_gradient = 1
        self.strain = 0
        self.strain_increment = 0

    def __str__(self):
        x = f"x={self.x}"
        v = f"velocity={self.velocity}"
        m = f"mass={self.mass}"
        vol = f"volume={self.current_volume}"
        mat = f"material={self.material}"
        stress = f"stress={self.stress}"
        force = f"force={self.force}"
        name = f"{self.__class__.__name__}"

        return f"{name}({x}, {v}, {m}, {vol}, {mat}, {stress}, {force})"

    def momentum(self) -> float:
        """Return the momentum."""
        return self.mass * self.velocity

    def update_deformation_gradient(self, dt: float):
        """Update the deformation gradient based on velocity gradient."""
        self.deformation_gradient *= 1 + self.velocity_gradient * dt

    def update_velocity_gradient(self, node_diff_shape: float, node_velocity: float):
        """Increase the velocity gradient contribution from a node."""
        self.velocity_gradient += node_diff_shape * node_velocity

    def update_volume(self):
        """Update current volume based on deformation gradient."""
        self.current_volume = self.deformation_gradient * self.initial_volume

    def update_stress(self):
        """Increase stress value based on strain increment."""
        self.stress += self.material.young * self.strain_increment

    def update_strain_increment(self, dt: float):
        """Update strain increment based on velocity gradient."""
        self.strain_increment = self.velocity_gradient * dt

    def update_velocity_from_node(self, node_shape: float, node_force: float, node_mass: float, dt: float):
        """Update velocity based on node quantities."""
        self.velocity += dt * node_shape * node_force / node_mass

    def update_position_from_node(self, node_shape: float, node_momentum: float, node_mass: float, dt: float):
        """Update position based on node quantities."""
        self.x += dt * node_shape * node_momentum / node_mass

    def reset(self):
        """Reset values for a step. Apply at each time step."""
        self.velocity_gradient = 0
