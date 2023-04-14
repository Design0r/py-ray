from PySide6.QtGui import QImage, QColor
from pyray.camera import Camera
from pyray.ray import Ray
import glm
import random
import numpy as np


class Renderer:
    def __init__(self, update_screen, render_res, msaa, ray_depth, scene, camera, sky_color) -> None:
        self.width, self.height = render_res
        self.image = QImage(self.width, self.height, QImage.Format.Format_ARGB32)
        self.scene = scene
        self.update_screen = update_screen
        self.camera: Camera = camera
        self.msaa: int = msaa if msaa > 0 else 1
        self.max_depth: int = ray_depth
        self.samples: int = 0
        self.buffer = np.empty(self.width * self.height, dtype=glm.vec3)
        self.sky_color: glm.vec3 = sky_color

    def calculate(self):
        i = 0

        self.samples += 1
        for h in range(self.height):
            for w in range(self.width):
                color: glm.vec3 = self.compute_sample(w, h)

                if self.buffer[i]:
                    self.buffer[i] += color
                else:
                    self.buffer[i] = color

                color = glm.min(self.buffer[i] / self.samples, glm.vec3(255, 255, 255))
                self.image.setPixel(w, h, QColor(color.x, color.y, color.z).rgb())
                i += 1

        self.update_screen(self.image)

    def compute_sample(self, x: int, y: int):
        aspect = self.height / self.width
        zdir = 1.0 / glm.tan(self.camera.fov)

        color = glm.vec3(0, 0, 0)
        for i in range(self.msaa):
            sub_x = (i % 2) / 2.0
            sub_y = (i // 2) / 2.0
            sub_pixel_x = x + sub_x
            sub_pixel_y = y + sub_y

            sub_xdir = (sub_pixel_x / self.width) * 2.0 - 1.0
            sub_ydir = ((sub_pixel_y / self.height) * 2.0 - 1.0) * aspect
            sub_direction = glm.normalize(glm.vec3(sub_xdir, sub_ydir, zdir))
            sub_ray = Ray(self.camera.pos, sub_direction)
            color += self.trace(sub_ray, 0)

        color /= self.msaa
        return color

    def trace(self, ray, current_depth):
        hit_distance = 5000.0
        hit_object = None

        for sphere in self.scene.list:
            intersect = sphere.intersect(ray)
            if -1.0 < intersect < hit_distance:
                hit_distance = intersect
                hit_object = sphere

        if hit_distance >= 5000.0:
            return self.sky_color
        if hit_object.is_emitter:
            return hit_object.color * hit_object.intensity
        if current_depth >= self.max_depth:
            return glm.vec3(0.0, 0.0, 0.0)

        hit_point = ray.origin + (ray.direction * hit_distance * 0.998)
        normal = hit_object.normal(hit_point)

        reflection_ray = Ray(hit_point, self.reflect_vector(ray.direction, normal, hit_object.roughness))
        return_color = self.trace(reflection_ray, current_depth + 1)

        color = return_color * hit_object.color / 255.0
        return color

    @staticmethod
    def reflect_vector(i: glm.vec3, n: glm.vec3, roughness: float):
        # Calculate the reflection vector without roughness
        # i - (n * (2 * i.dot(n)))
        reflection_vector = glm.reflect(i, n)

        # Add random roughness
        roughness_vector = glm.sphericalRand(1)
        reflection_vector += roughness_vector * roughness
        return reflection_vector
