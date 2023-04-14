from __future__ import annotations
from pyray.object import Object
from pyray.ray import Ray
import glm


class Sphere(Object):
    def __init__(self, center: glm.vec3, radius: float, color: glm.vec3, roughness: float, is_emitter: bool, intensity=1) -> None:
        self.center: glm.vec3 = center
        self.radius: float = radius
        self.color: glm.vec3 = color
        self.roughness: float = roughness
        self.is_emitter: bool = is_emitter
        self.intensity: float = intensity

    def intersect(self, ray: Ray) -> float:
        v: glm.vec3 = ray.origin - self.center
        a: float = glm.dot(ray.direction, ray.direction)
        b: float = 2 * glm.dot(ray.direction, v)
        c: float = glm.dot(v, v) - self.radius * self.radius

        discriminant: float = (b*b) - (4.0 * a * c)
        if discriminant > 0:
            x1: float = (-b - glm.sqrt(discriminant)) / (2.0 * a)
            x2: float = (-b + glm.sqrt(discriminant)) / (2.0 * a)

            if x1 >= 0 and x2 >= 0:
                return x1
            elif x1 < 0 and x2 >= 0:
                return x2
        return -1.0

    def normal(self, point: glm.vec3):
        return glm.normalize(point - self.center)
