from node import Node
from material import Material


class Element:
    nodes: list[Node]
    length: float
    mass: float
    volume: float
    material: Material

    def __init__(self, nodes: list[Node], volume: float = 1, material: Material = None):
        """Constructor.

        :param nodes: List of nodes.
        :param volume: Initial volume.
        :param material: Material object.
        """
        self.nodes = nodes
        self.volume = volume
        self.material = material

        self.mass = self.material.rho * self.volume

    def x_ini(self) -> float:
        """Return the initial coordinate of the element."""
        return self.nodes[0].x

    def x_final(self) -> float:
        """Return the final coordinate of the element."""
        return self.nodes[1].x

    def length(self) -> float:
        return self.x_final() - self.x_ini()

    def reset(self):
        """Reset the values of element nodes."""
        for n in self.nodes:
            n.reset()
