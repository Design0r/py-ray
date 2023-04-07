from __future__ import annotations
import math
import random


def dot(vec1: tuple, vec2: tuple) -> float:
    return (vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2])


def add(vec1, vec2) -> tuple:
    return (vec1[0] + vec2[0], vec1[1] + vec2[1], vec1[2] + vec2[2])


def sub(vec1, vec2) -> tuple:
    return (vec1[0] - vec2[0], vec1[1] - vec2[1], vec1[2] - vec2[2])


def mul(vec1, vec2) -> tuple:
    if isinstance(vec2, tuple):
        return (vec1[0] * vec2[0], vec1[1] * vec2[1], vec1[2] * vec2[2])

    return (vec1[0] * vec2, vec1[1] * vec2, vec1[2] * vec2)


def normalize(vec):
    factor = 1 / math.sqrt(dot(vec, vec))
    return (vec[0] * factor, vec[1] * factor, vec[2] * factor)


def negate(vec):
    return (vec[0] * -1, vec[1] * -1, vec[2] * -1)


def reflect_vector(i: tuple, n: tuple, roughness: float):
    # Calculate the reflection vector without roughness
    # i - (n * (2 * i.dot(n)))
    reflection_vector = sub(i, mul(n, dot(i, n) * 2))
    # Add random roughness
    roughness_vector = (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
    roughness_vector = normalize(roughness_vector)
    reflection_vector = add(reflection_vector, mul(roughness_vector, roughness))
    return reflection_vector


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
    def reflect_vector(i: Point3D, n: Point3D, roughness: float):
        # Calculate the reflection vector without roughness
        reflection_vector = i - (n * (2 * i.dot(n)))

        # Add random roughness
        roughness_vector = Point3D([random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)])
        roughness_vector.normalize()
        reflection_vector += roughness_vector * roughness

        return reflection_vector

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}, z: {self.z}"
