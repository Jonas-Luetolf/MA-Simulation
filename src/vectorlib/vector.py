from math import acos, degrees, sqrt


class Vector:
    def __init__(self, components):
        if not isinstance(components, (tuple, list)):
            raise TypeError("Vector only takes list or tupel")

        if not all(isinstance(i, (int, float)) for i in components):
            raise TypeError(
                f"""Vector only takes float or integers as components got:
                 {','.join(set([type(i) for i in components]))}"""
            )

        self.components = list(components)

    def __getitem__(self, n):
        if abs(n) >= len(self.components):
            raise IndexError(
                f"""Vector has only {len(self.components)}
                components tried to access  number {n + 1}"""
            )

        return self.components[n]

    def __setitem__(self, n, value):
        if abs(n) >= len(self.components):
            raise IndexError(
                f"""Vector has only {len(self.components)}
                components tried to access number {n + 1}"""
            )

        self.components[n] = value

    def __abs__(self):
        return sqrt(sum([x**2 for x in self.components]))

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("additon only supported between Vector and Vector")

        if not len(self.components) == len(other.components):
            raise TypeError("additon only supported between Vectors with same size")

        return Vector([x + y for x, y in zip(self.components, other.components)])

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("subtraction only supported between Vector and Vector")

        if not len(self.components) == len(other.components):
            raise TypeError("subtraction only supported between Vector with same size")

        return self.__add__(other * (-1))

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("multiplication only supported between Vectors and number")

        return Vector([x * other for x in self.components])

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("division only supported between Vector and number")

        return self.__mul__(1 / other)


def angel(x: Vector, y: Vector, deg: bool = True) -> float:
    if not isinstance(x, Vector) or not isinstance(y, Vector):
        raise TypeError("angel only supported between Vector and Vector")

    if not len(x.components) == len(y.components):
        raise ValueError(
            "angel only supported between two Vectors with same number of components"
        )

    angel = acos(
        sum([a * b for a, b in zip(x.components, y.components)]) / (abs(x) * abs(y))
    )

    if deg:
        angel = degrees(angel)

    return round(angel, 4)
