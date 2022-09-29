from math import sqrt


class Material:
    def __init__(self, density: float, young: float):
        """Constructor.

        :param density: Density.
        :param young: Young modulus.
        """
        self.rho = density
        self.young = young

    def __str__(self):
        return f"{self.__class__.__name__}(density={self.rho}, young={self.young})"

    def elastic_wave_speed(self) -> float:
        """Return the elastic wave speed in material."""
        return sqrt(self.young / self.rho)
