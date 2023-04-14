from pyray.camera import Camera
from pyray.renderer import Renderer
from pyray.scene import Scene
from pyray.sphere import Sphere
from pyray.worker_thread import WorkerThread
from PySide6.QtGui import QImage, QColor
import glm


class RenderManager:
    def __init__(self, update_screen, update_progress_label) -> None:
        self.renderer = None
        self.stop_flag = False
        self.render_thread = None
        self.scene = None
        self.img = QImage(1, 1, QImage.Format.Format_ARGB32)
        self.img.setPixel(0, 0, QColor("black").rgb())

        # ===== Window functions =====
        self.update_screen = update_screen
        self.update_progress_label = update_progress_label

        # ===== Settings ======
        self.render_width = 128
        self.render_height = 128
        self.camera = Camera(glm.vec3(0.0, -2.0, 12.5), glm.vec3(0, 0, 0), 160)
        self.msaa = 2
        self.ray_depth = 3
        self.sky_color = glm.vec3(184, 211, 254)

    def init_renderer(self, restart=False):

        self.renderer = Renderer(self.update_screen, (self.render_width, self.render_height), self.msaa, self.ray_depth, self.scene, self.camera, self.sky_color)

        if restart and self.render_thread:
            self.stop_render_thread()
            self.start_render_thread()

    def start_render_thread(self):
        self.render_thread = WorkerThread(self.renderer)
        self.render_thread.progress_signal.connect(self.update_progress_label)
        self.render_thread.start()

    def stop_render_thread(self):
        self.render_thread.stop()
        self.render_thread.quit()
        self.render_thread.wait()

    def profiling(self):
        import cProfile
        import pstats

        with cProfile.Profile() as pr:
            for i in range(3):
                self.renderer.calculate()
        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()
        stats.dump_stats(filename="render_profiling.prof")

    def load_scene(self, number: int) -> None:
        red = glm.vec3(217, 59, 59)
        green = glm.vec3(39, 163, 60)
        white = glm.vec3(255, 255, 255)
        grey = glm.vec3(180, 180, 180)
        match number:
            case 1:
                sphere1 = Sphere(glm.vec3(0.0, -3.5, 3.0), 2, white, 0.0, True, intensity=1)
                sphere2 = Sphere(glm.vec3(8.0, 0.0, 3.0), 6, red, 1.0, False)
                sphere3 = Sphere(glm.vec3(-8.0, 0.0, 3.0), 6, green, 1.0, False)
                sphere4 = Sphere(glm.vec3(0.0, 8.0, 3.0), 6, grey, 1.0, False)
                sphere5 = Sphere(glm.vec3(0.0, -8.0, 3.0), 6, grey, 1.0, False)
                sphere6 = Sphere(glm.vec3(0.0, 1.5, 3.0), 0.75, green, 0.2, False)
                sphere7 = Sphere(glm.vec3(0.0, 0.48, 3.0), 0.33, white, 1.0, True)
                sphere8 = Sphere(glm.vec3(0.0, 0.0, -7.5), 6, grey, 0.2, False)
                self.scene = Scene(sphere1, sphere2, sphere3, sphere4, sphere5, sphere6, sphere7, sphere8)
            case 2:
                light_sphere = Sphere(glm.vec3(0.0, -6.3, 3.0), 2, white, 1.0, True, intensity=7)
                sphere2 = Sphere(glm.vec3(1.5, -0.3, 3.0), 0.415, red, 0.1, False)
                sphere3 = Sphere(glm.vec3(-5.339, -1.948, -16.014), 6, green, 0.2, False)
                ground_sphere = Sphere(glm.vec3(0.0, 50.0, 3.0), 50, grey, 0.5, False)
                sphere5 = Sphere(glm.vec3(0, -0.75, 3), 0.75, grey, 0.8, False)
                sphere6 = Sphere(glm.vec3(21, -2, 22), 11, green, 0.8, False)
                # sphere7 = Sphere(glm.vec3(-1.5, -1.95, 28.4), 6, white, True)
                sphere8 = Sphere(glm.vec3(-23.5, -2, 17.8), 8, grey, 0.6, False)
                self.scene = Scene(light_sphere, ground_sphere, sphere2, sphere3, sphere8, sphere5, sphere6)
            case 3:
                sphere1 = Sphere(glm.vec3(0.0, -3.5, 3.0), 2, glm.vec3(255, 255, 255), 1.0, True)
                self.scene = Scene(sphere1)

        self.init_renderer(restart=True)
