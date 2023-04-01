import sys
import math
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from pyray.point_3d import Point3D
from pyray.ray import Ray
from pyray.color import Color


class Renderer:
    def __init__(self, window, scene, camera) -> None:
        self.scene = scene
        self.window = window
        self.width = window.render_width
        self.height = window.render_height
        self.camera = camera
        self.max_depth = 3
        self.samples = 0
        self.buffer = [0.0] * (self.width * self.height * 3)

    def calculate(self):
        i = 0

        self.samples += 1
        for w in range(self.width):
            for h in range(self.height):
                color = self.compute_sample(w, h)
                self.buffer[i * 3 + 0] += color.r
                self.buffer[i * 3 + 1] += color.g
                self.buffer[i * 3 + 2] += color.b

                self.window.img.setPixel(w, h, QColor(self.buffer[i * 3 + 0] / self.samples, self.buffer[i * 3 + 1] / self.samples, self.buffer[i * 3 + 2] / self.samples, 1).rgb())
                i += 1

        self.window.update_screen()

    def compute_sample(self, x, y):
        fov = 160 * math.pi / 180
        aspect = self.height / self.width

        xdir = (x / self.width) * 2.0 - 1.0
        ydir = ((y / self.height) * 2.0 - 1.0) * aspect
        zdir = 1.0 / math.tan(fov)

        direction = Point3D(xdir, ydir, zdir).normalize()
        ray = Ray(self.camera, direction)

        return self.trace(ray, 1)

    def trace(self, ray, current_depth):
        hit_distance = 5000.0
        hit_object = None

        for sphere in self.scene.list:
            intersect = sphere.intersect(ray)
            if -1.0 < intersect < hit_distance:
                hit_distance = intersect
                hit_object = sphere

        if (hit_distance >= 5000.0):
            return Color(0, 0, 0)
        if hit_object.is_emitter:
            return hit_object.color
        if current_depth == self.max_depth:
            return Color(0, 0, 0)

        hit_point = ray.origin.add(ray.direction.mul(hit_distance * 0.998))
        normal = hit_object.normal(hit_point)

        #random_point = Point3D.sample_in_hemisphere()
        refl = normal.dot(ray.direction.normalize())
        # if random_point.dot(normal) < 0.0:
        #    random_point = random_point.negate()

        #reflection_ray = Ray(hit_point, random_point.normalize())
        reflection_ray = Ray(hit_point, ray.direction.sub(normal.mul(refl).mul(2)))
        return_color = self.trace(reflection_ray, current_depth + 1)

        r = 2 * hit_object.color.r * return_color.r / 255
        g = 2 * hit_object.color.g * return_color.g / 255
        b = 2 * hit_object.color.b * return_color.b / 255

        # tonemapping
        r = (r/(r+1))*100
        g = (g/(g+1))*100
        b = (b/(b+1))*100

        return Color(r, g, b)
