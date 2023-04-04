from __future__ import annotations
import math
import random


class Point3D_numpy:
    def __init__(self, point) -> None:
        self.point = np.array(point)

    def dot(self, point: Point3D) -> float:
        return np.dot(self.point, point.point)

    def __sub__(self, point: Point3D) -> Point3D:
        return Point3D(self.point - point.point)

    def __add__(self, point: Point3D) -> Point3D:
        return Point3D(self.point + point.point)

    def __mul__(self, factor:  int | float | Point3D) -> Point3D:
        if isinstance(factor, float) or isinstance(factor, int):
            return Point3D(self.point * factor)
        elif isinstance(factor, Point3D):
            return Point3D(self.point * factor.point)

    def normalize(self) -> Point3D:
        factor = 1.0 / math.sqrt(self.dot(self))
        return Point3D(self.point * factor)

    def negate(self) -> Point3D:
        return Point3D(self.point * (-1))

    @staticmethod
    def sample_in_hemisphere():
        u1 = random.uniform(0.0, 1.0)
        u2 = random.uniform(0.0, 1.0)

        z = 1.0 - 2.0 * u1
        r = math.sqrt(max(0.0,  1.0 - z * z))
        phi = 2.0 * math.pi * u2
        x = r * math.cos(phi)
        y = r * math.sin(phi)

        return Point3D([x, y, z]).normalize()

    @staticmethod
    def reflect_vector(i, n):
        """
        Calculates the reflection vector of an incident vector off a surface with a given normal vector.

        Parameters:
            i (tuple or list): A 3-element sequence representing the incident vector.
            n (tuple or list): A 3-element sequence representing the normal vector of the surface.

        Returns:
            tuple: A 3-element sequence representing the reflection vector.
        """

        i_norm = (i[0] ** 2 + i[1] ** 2 + i[2] ** 2) ** 0.5
        i = (i[0] / i_norm, i[1] / i_norm, i[2] / i_norm)

        n_norm = (n[0] ** 2 + n[1] ** 2 + n[2] ** 2) ** 0.5
        n = (n[0] / n_norm, n[1] / n_norm, n[2] / n_norm)

        dot_product = i[0] * n[0] + i[1] * n[1] + i[2] * n[2]
        r = (i[0] - 2 * dot_product * n[0],
             i[1] - 2 * dot_product * n[1],
             i[2] - 2 * dot_product * n[2])

        return Point3D(r)

    def __repr__(self) -> str:
        return f"x: {self.point[0]}, y: {self.point[1]}, z: {self.point[2]}"


class Point3D:
    def __init__(self, point) -> None:
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def dot(self, point: Point3D) -> float:
        return self.x * point.x + self.y * point.y + self.z * point.z

    def __sub__(self, point: Point3D) -> Point3D:
        return Point3D([self.x - point.x, self.y - point.y, self.z - point.z])

    def __add__(self, point: Point3D) -> Point3D:
        return Point3D([self.x + point.x, self.y + point.y, self.z + point.z])

    def __mul__(self, factor:  int | float | Point3D) -> Point3D:
        if isinstance(factor, float) or isinstance(factor, int):
            return Point3D([self.x * factor, self.y * factor, self.z * factor])
        elif isinstance(factor, Point3D):
            return Point3D([self.x * factor.x, self.y * factor.y, self.z * factor.z])

    def normalize(self) -> Point3D:
        factor = 1.0 / math.sqrt(self.dot(self))
        return Point3D([self.x * factor, self.y * factor, self.z * factor])

    def negate(self) -> Point3D:
        return Point3D([self.x * (-1), self.y * (-1), self.z * (-1)])
        # return Point3D(self.x * -1, self.y * -1, self.z * -1)

    @staticmethod
    def sample_in_hemisphere():
        u1 = random.uniform(0.0, 1.0)
        u2 = random.uniform(0.0, 1.0)

        z = 1.0 - 2.0 * u1
        r = math.sqrt(max(0.0,  1.0 - z * z))
        phi = 2.0 * math.pi * u2
        x = r * math.cos(phi)
        y = r * math.sin(phi)

        return Point3D([x, y, z]).normalize()

    @staticmethod
    def reflect_vector(i: Point3D, n: Point3D):
        r = i - (n * (2 * i.dot(n)))
        return r

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}, z: {self.z}"
