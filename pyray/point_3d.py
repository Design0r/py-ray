from __future__ import annotations
import math
import random
import numpy as np


class Point3D:
    def __init__(self, x, y=None, z=None) -> None:
        if (y == None and z == None):
            self.x = x.x
            self.y = x.y
            self.z = x.z
        else:
            self.x = x
            self.y = y
            self.z = z

    def dot(self, point: Point3D) -> float:
        return self.x * point.x + self.y * point.y + self.z * point.z

    def sub(self, point: Point3D) -> Point3D:
        return Point3D(self.x - point.x, self.y - point.y, self.z - point.z)

    def add(self, point: Point3D) -> Point3D:
        return Point3D(self.x + point.x, self.y + point.y, self.z + point.z)

    def mul(self, factor: float) -> Point3D:
        return Point3D(self.x * factor, self.y * factor, self.z * factor)

    def mul_vec(self, vector) -> Point3D:
        return Point3D(self.x * vector.x, self.y * vector.y, self.z * vector.z)

    def normalize(self) -> Point3D:
        factor = 1.0 / math.sqrt(self.dot(self))
        return Point3D(self.mul(factor))

    def negate(self) -> Point3D:
        return Point3D(self.x * -1, self.y * -1, self.z * -1)

    @staticmethod
    def sample_in_hemisphere():
        u1 = random.uniform(0.0, 1.0)
        u2 = random.uniform(0.0, 1.0)

        z = 1.0 - 2.0 * u1
        r = math.sqrt(max(0.0,  1.0 - z * z))
        phi = 2.0 * math.pi * u2
        x = r * math.cos(phi)
        y = r * math.sin(phi)

        return Point3D(x, y, z).normalize()

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}, z: {self.z}"
