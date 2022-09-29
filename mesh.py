from node import Node
from element import Element
from material import Material


class Mesh:
    x_ini: float
    x_final: float
    num_els: int
    length: float
    nodes: list[Node]
    elements: list[Element]

    def __init__(self, x_ini: float, x_final: float, num_els: int):
        """Constructor.

        :param x_ini: Initial position.
        :param x_final: Final position.
        :param num_els: Number of elements.
        """
        self.x_ini = x_ini
        self.x_final = x_final
        self.num_els = num_els

        self.nodes = []
        self.elements = []

    def __str__(self):
        lx = f"length={self.length()}"
        n_els = f"n_els={self.num_els}"
        n_nodes = f"n_nodes={len(self.nodes)}"

        return f"{self.__class__.__name__}({lx},{n_els}, {n_nodes})"

    def length(self) -> float:
        """Return the mesh length."""
        return self.x_final - self.x_ini

    def elements_length(self) -> float:
        """Return the length of elements. All elements have same length."""
        return self.length() / self.num_els

    def generate_mesh(self, material: Material):
        """Generate elements and nodes of the mesh.

        :param material: Material to apply in all elements.
        """

        x = 0

        self.nodes.append(Node(x))

        for i in range(self.num_els):
            n1 = self.nodes[i]
            n2 = Node(x=n1.x + self.elements_length())

            self.nodes.append(n2)

            el = Element(nodes=[n1, n2],
                         material=material)

            self.elements.append(el)

    def reset(self):
        """Reset elements properties. Use once in each step."""
        for el in self.elements:
            el.reset()
