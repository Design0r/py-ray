from __future__ import annotations
import math
from pyray.object import Object
from pyray.point_3d import Point3D
from pyray.ray import Ray


class Sphere(Object):
    def __init__(self, center, radius, color, is_emitter) -> None:
        self.center = center
        self.radius = radius
        self.color = color
        self.is_emitter = is_emitter

    def intersect(self, ray: Ray):
        v = ray.origin.sub(self.center)
        a = ray.direction.dot(ray.direction)
        b = 2.0 * ray.direction.dot(v)
        c = v.dot(v) - self.radius * self.radius

        discriminant = (b*b) - (4.0 * a * c)
        if discriminant > 0:
            x1 = (-b - math.sqrt(discriminant)) / (2.0 * a)
            x2 = (-b + math.sqrt(discriminant)) / (2.0 * a)

            if x1 >= 0 and x2 >= 0:
                return x1
            elif x1 < 0 and x2 >= 0:
                return x2
        return -1.0

    def normal(self, point):
        return Point3D(point.sub(self.center).normalize())
