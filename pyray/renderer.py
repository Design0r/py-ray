import math
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from pyray.point_3d import Point3D
from pyray.ray import Ray
from pyray.color import Color
import array


class Renderer:
    def __init__(self, update_screen, image, render_res, ray_depth, scene, camera) -> None:
        self.scene = scene
        self.update_screen = update_screen
        self.width, self.height = render_res
        self.camera = camera
        self.max_depth = ray_depth
        self.samples = 0
        self.buffer = array.array("f", [0.0] * (self.width * self.height * 3))
        self.image = image

    def calculate(self):
        i = 0

        self.samples += 1
        for w in range(self.width):
            for h in range(self.height):
                color = self.compute_sample(w, h)
                self.buffer[i * 3 + 0] += color.r
                self.buffer[i * 3 + 1] += color.g
                self.buffer[i * 3 + 2] += color.b

                r = self.buffer[i * 3 + 0] / self.samples
                g = self.buffer[i * 3 + 1] / self.samples
                b = self.buffer[i * 3 + 2] / self.samples

                #r, g, b = self.reinhard_tonemapping((r, g, b))

                self.image.setPixel(w, h, QColor(r, g, b).rgb())
                i += 1

        self.update_screen()

    def compute_sample(self, x, y):
        fov = 160 * math.pi / 180
        aspect = self.height / self.width

        xdir = (x / self.width) * 2.0 - 1.0
        ydir = ((y / self.height) * 2.0 - 1.0) * aspect
        zdir = 1.0 / math.tan(fov)

        direction = Point3D([xdir, ydir, zdir]).normalize()
        ray = Ray(self.camera, direction)

        return self.trace(ray, 0)

    def trace(self, ray, current_depth):
        hit_distance = 5000.0
        hit_object = None

        for sphere in self.scene.list:
            intersect = sphere.intersect(ray)
            if -1.0 < intersect < hit_distance:
                hit_distance = intersect
                hit_object = sphere

        if (hit_distance >= 5000.0):
            return Color(163, 198, 255)
        if hit_object.is_emitter:
            return hit_object.color
        if current_depth >= self.max_depth:
            return Color(0, 0, 0)

        hit_point = ray.origin + ray.direction * (hit_distance * 0.998)
        normal = hit_object.normal(hit_point)

        random_point = Point3D.sample_in_hemisphere()
        if random_point.dot(normal) < 0.0:
            random_point = random_point.negate()
        reflection_ray = Ray(hit_point, random_point.normalize())

        #reflection_ray = Ray(hit_point, Point3D.reflect_vector(ray.direction, normal))
        return_color = self.trace(reflection_ray, current_depth + 1)

        r = hit_object.color.r * return_color.r / 255
        g = hit_object.color.g * return_color.g / 255
        b = hit_object.color.b * return_color.b / 255

        return Color(r, g, b)
