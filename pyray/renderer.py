import sys
import math
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from pyray.point_3d import Point3D
from pyray.ray import Ray
from pyray.color import Color
import numpy as np


class Renderer:
    def __init__(self, window, scene, camera) -> None:
        self.scene = scene
        self.window = window
        self.width = window.render_width
        self.height = window.render_height
        self.camera = camera
        self.max_depth = 10
        self.samples = 0
        self.buffer = np.zeros((self.width * self.height * 3))

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

                self.window.img.setPixel(w, h, QColor(r, g, b).rgb())
                i += 1

        self.window.update_screen()

    def compute_sample(self, x, y):
        fov = 160 * math.pi / 180
        aspect = self.height / self.width

        xdir = (x / self.width) * 2.0 - 1.0
        ydir = ((y / self.height) * 2.0 - 1.0) * aspect
        zdir = 1.0 / math.tan(fov)

        direction = Point3D([xdir, ydir, zdir]).normalize()
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
            return Color(163, 198, 255)
        if hit_object.is_emitter:
            return hit_object.color
        if current_depth == self.max_depth:
            return Color(0, 0, 0)

        hit_point = ray.origin + ray.direction * (hit_distance * 0.998)
        normal = hit_object.normal(hit_point)

        #random_point = Point3D.sample_in_hemisphere()
        # if random_point.dot(normal) < 0.0:
        #    random_point = random_point.negate()
        #reflection_ray = Ray(hit_point, random_point.normalize())

        reflection_ray = Ray(hit_point, Point3D.reflect_vector((ray.direction.x, ray.direction.y, ray.direction.z), (normal.x, normal.y, normal.z)))
        return_color = self.trace(reflection_ray, current_depth + 1)

        r = hit_object.color.r * return_color.r / 255
        g = hit_object.color.g * return_color.g / 255
        b = hit_object.color.b * return_color.b / 255

        return Color(r, g, b)

    def reinhard_tonemapping(self, rgb, a=0.18):
        """
        Maps an RGB color to the range 0 to 1 using the Reinhard tonemapping operator.

        Parameters:
            rgb (tuple): A tuple containing the RGB values of the color as integers between 0 and 255.
            a (float): A parameter that controls the amount of compression as a float.

        Returns:
            tuple: A tuple containing the tonemapped RGB values of the color as integers between 0 and 255.
        """

        # Convert RGB values to linear luminance
        r_lin = rgb[0] / 255.0
        g_lin = rgb[1] / 255.0
        b_lin = rgb[2] / 255.0
        lum_lin = 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin

        # Calculate the key value (average luminance)
        L_w = (lum_lin ** a).mean() ** (1.0 / a)

        # Check for a zero key value
        if L_w == 0:
            L_w = 1.0

        # Calculate the tonemapped luminance
        if lum_lin == 0:
            Ld_lin = 0.0
        else:
            Ld_lin = (a / L_w) * lum_lin
        Ld_lin_clipped = Ld_lin / (1.0 + Ld_lin)

        # Convert tonemapped luminance to tonemapped RGB
        if lum_lin == 0:
            r_tonemapped = 0.0
            g_tonemapped = 0.0
            b_tonemapped = 0.0
        else:
            r_tonemapped = 255.0 * ((r_lin / lum_lin) * Ld_lin_clipped)
            g_tonemapped = 255.0 * ((g_lin / lum_lin) * Ld_lin_clipped)
            b_tonemapped = 255.0 * ((b_lin / lum_lin) * Ld_lin_clipped)

        # Clip the output to the range 0 to 255
        r_tonemapped = max(min(int(r_tonemapped), 255), 0)
        g_tonemapped = max(min(int(g_tonemapped), 255), 0)
        b_tonemapped = max(min(int(b_tonemapped), 255), 0)

        return (r_tonemapped, g_tonemapped, b_tonemapped)
