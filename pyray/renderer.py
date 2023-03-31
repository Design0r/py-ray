import sys
import math
from PySide6.QtWidgets import *
from pyray.point_3d import Point3D
from pyray.ray import Ray
from pyray.color import Color
from pyray.window import Window


class Renderer:
    def __init__(self, scene, width, height, camera, zoom) -> None:
        self.scene = scene
        self.width = width
        self.height = height
        self.camera = camera
        self.max_depth = 4
        self.samples = 0
        self.buffer = [0] * (self.width * self.height * 3 + 1)

        self.app = QApplication(sys.argv)
        self.zoom = zoom
        self.window = Window(zoom=zoom)
        self.window.set_width(self.width * zoom)
        self.window.set_height(self.height * zoom)

    def calculate(self):
        i = 0

        for w in range(self.width):
            for h in range(self.height):
                color = self.compute_sample(w, h)
                self.buffer[i * 3 + 0] += color.r
                self.buffer[i * 3 + 1] += color.g
                self.buffer[i * 3 + 2] += color.b
                i += 1

        self.samples += 1

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

        if (hit_distance == 5000.0):
            return Color(0, 0, 0)
        if hit_object.is_emitter:
            return hit_object.color
        if current_depth == self.max_depth:
            return Color(0, 0, 0)

        hit_point = ray.origin.add(ray.direction.mul(hit_distance * 0.998))
        normal = hit_object.normal(hit_point)

        random_point = Point3D.sample_in_hemisphere()
        if random_point.dot(normal) < 0.0:
            random_point = random_point.negate()
        reflection_ray = Ray(hit_point, random_point.normalize())

        return_color = self.trace(reflection_ray, current_depth + 1)

        r = hit_object.color.r * return_color.r
        g = hit_object.color.g * return_color.g
        b = hit_object.color.b * return_color.b

        r /= 255.0
        g /= 255.0
        b /= 255.0

        return Color(r, g, b)

    def update_screen(self):
        i = 0
        for w in range(self.width):
            for h in range(self.height):
                r = self.buffer[i * 3 + 0] / self.samples
                g = self.buffer[i * 3 + 1] / self.samples
                b = self.buffer[i * 3 + 2] / self.samples
                self.window.set_pixel(w, h, Color(r, g, b))
                i += 1
        self.window.update_screen(self.samples)
