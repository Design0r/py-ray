import math
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import pyray.point_3d as p3d
from pyray.ray import Ray
from pyray.color import Color
import array
from multiprocessing import Pool


class Renderer:
    def __init__(self, update_screen, image, render_res, msaa, ray_depth, scene, camera, sky_color) -> None:
        self.scene = scene
        self.update_screen = update_screen
        self.width, self.height = render_res
        self.camera = camera
        self.msaa = msaa if msaa > 0 else 1
        self.max_depth = ray_depth
        self.samples = 0
        self.buffer = array.array("f", [0.0] * (self.width * self.height * 3))
        self.image = image
        self.sky_color = sky_color

    def calculate(self):
        i = 0

        self.samples += 1
        for h in range(self.height):
            for w in range(self.width):
                color = self.compute_sample(w, h, self.msaa)
                self.buffer[i * 3 + 0] += color.r
                self.buffer[i * 3 + 1] += color.g
                self.buffer[i * 3 + 2] += color.b

                r: float = min(self.buffer[i * 3 + 0] / self.samples, 255)
                g: float = min(self.buffer[i * 3 + 1] / self.samples, 255)
                b: float = min(self.buffer[i * 3 + 2] / self.samples, 255)

                self.image.setPixel(w, h, QColor(r, g, b).rgb())
                i += 1

        self.update_screen()

    def compute_sample(self, x: int, y: int, samples: int):
        aspect = self.height / self.width
        zdir = 1.0 / math.tan(self.camera.fov)

        color = Color(0, 0, 0)
        for i in range(samples):
            sub_x = (i % 2) / 2.0
            sub_y = (i // 2) / 2.0
            sub_pixel_x = x + sub_x
            sub_pixel_y = y + sub_y

            sub_xdir = (sub_pixel_x / self.width) * 2.0 - 1.0
            sub_ydir = ((sub_pixel_y / self.height) * 2.0 - 1.0) * aspect
            sub_direction = p3d.normalize((sub_xdir, sub_ydir, zdir))
            sub_ray = Ray(self.camera.pos, sub_direction)
            color += self.trace(sub_ray, 0)

        color /= samples
        return color

    def trace(self, ray, current_depth):
        hit_distance = 5000.0
        hit_object = None

        for sphere in self.scene.list:
            intersect = sphere.intersect(ray)
            if -1.0 < intersect < hit_distance:
                hit_distance = intersect
                hit_object = sphere

        if (hit_distance >= 5000.0):
            return self.sky_color
        if hit_object.is_emitter:
            return hit_object.color * hit_object.intensity
        if current_depth >= self.max_depth:
            return Color(0, 0, 0)

        hit_point = p3d.add(ray.origin, p3d.mul(ray.direction, hit_distance * 0.998))
        normal = hit_object.normal(hit_point)

        reflection_ray = Ray(hit_point, p3d.reflect_vector(ray.direction, normal, hit_object.roughness))
        return_color = self.trace(reflection_ray, current_depth + 1)

        r = hit_object.color.r * return_color.r / 255
        g = hit_object.color.g * return_color.g / 255
        b = hit_object.color.b * return_color.b / 255

        return Color(r, g, b)
