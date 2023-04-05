from __future__ import annotations
import math
from pyray.color import Color
from pyray.object import Object
from pyray.ray import Ray
from pyray.point_3d import Point3D


class Sphere(Object):
    def __init__(self, center: Point3D, radius: float, color: Color, roughness: float, is_emitter: bool, intensity=1) -> None:
        self.center = center
        self.radius = radius
        self.color = color
        self.roughness = roughness
        self.is_emitter = is_emitter
        self.intensity = intensity

    def intersect(self, ray: Ray) -> float:
        v: Point3D = ray.origin - self.center
        a: float = ray.direction.dot(ray.direction)
        b: float = 2.0 * ray.direction.dot(v)
        c: float = v.dot(v) - self.radius * self.radius

        discriminant: float = (b*b) - (4.0 * a * c)
        if discriminant > 0:
            x1: float = (-b - math.sqrt(discriminant)) / (2.0 * a)
            x2: float = (-b + math.sqrt(discriminant)) / (2.0 * a)

            if x1 >= 0 and x2 >= 0:
                return x1
            elif x1 < 0 and x2 >= 0:
                return x2
        return -1.0

    def normal(self, point: Point3D):
        return (point - self.center).normalize()
