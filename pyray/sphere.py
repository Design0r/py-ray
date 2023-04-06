from __future__ import annotations
import math
from pyray.color import Color
from pyray.object import Object
from pyray.ray import Ray
import pyray.point_3d as p3d


class Sphere(Object):
    def __init__(self, center: tuple, radius: float, color: Color, roughness: float, is_emitter: bool, intensity=1) -> None:
        self.center = center
        self.radius = radius
        self.color = color
        self.roughness = roughness
        self.is_emitter = is_emitter
        self.intensity = intensity

    def intersect(self, ray: Ray) -> float:
        v = p3d.sub(ray.origin, self.center)
        a: float = p3d.dot(ray.direction, ray.direction)
        b: float = 2 * p3d.dot(ray.direction, v)
        c: float = p3d.dot(v, v) - self.radius * self.radius

        discriminant: float = (b*b) - (4.0 * a * c)
        if discriminant > 0:
            x1: float = (-b - math.sqrt(discriminant)) / (2.0 * a)
            x2: float = (-b + math.sqrt(discriminant)) / (2.0 * a)

            if x1 >= 0 and x2 >= 0:
                return x1
            elif x1 < 0 and x2 >= 0:
                return x2
        return -1.0

    def normal(self, point: tuple):
        return p3d.normalize(p3d.sub(point, self.center))
