from __future__ import annotations
from pyray.object import Object
from pyray.ray import Ray
import glm


class Sphere(Object):
    def __init__(
        self,
        center: glm.vec3,
        radius: float,
        color: glm.vec3,
        roughness: float,
        is_emitter: bool,
        intensity=1,
    ) -> None:
        self.center = center
        self.radius_sq = radius * radius  # Precompute squared radius
        self.color = color
        self.roughness = roughness
        self.is_emitter = is_emitter
        self.intensity = intensity

    def intersect(self, ray: Ray) -> float:
        cam_to_sphere_vec = ray.origin - self.center
        a = glm.dot(ray.direction, ray.direction)
        b = 2.0 * glm.dot(ray.direction, cam_to_sphere_vec)
        c = glm.dot(cam_to_sphere_vec, cam_to_sphere_vec) - self.radius_sq

        discriminant = b * b - 4.0 * a * c
        if discriminant > 0:
            sqrt_discriminant = glm.sqrt(discriminant)
            x1 = (-b - sqrt_discriminant) / (2.0 * a)
            x2 = (-b + sqrt_discriminant) / (2.0 * a)

            if x1 >= 0 and x2 >= 0:
                return min(x1, x2)  # Return the smallest positive root

        return -1.0

    def normal(self, point: glm.vec3):
        return glm.normalize(point - self.center)
