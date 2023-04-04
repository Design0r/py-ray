from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from pyray.color import Color
from pyray.point_3d import Point3D
from pyray.renderer import Renderer
from pyray.scene import Scene
from pyray.sphere import Sphere
from functools import partial


class WorkerThread(QThread):
    # Define a signal to emit a message when the thread finishes
    finished_signal = Signal(str)
    progress_signal = Signal(int)

    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer
        self.stop_flag = False

    def run(self):
        samples = 0
        while not self.stop_flag:
            self.renderer.calculate()
            self.progress_signal.emit(samples)
            samples += 1
            self.msleep(5)
        message = "Thread finished"
        self.finished_signal.emit(message)

    def stop(self) -> None:
        self.stop_flag = True


class Window(QWidget):
    def __init__(self, window_dimensions, parent=None) -> None:
        super().__init__(parent)
        self.width, self.height = window_dimensions
        self.render_width, self.render_height = 128, 128
        self.viewport_width, self.viewport_height = 700, 700
        self.img = QImage(1, 1, QImage.Format.Format_ARGB32)
        self.img.setPixel(0, 0, QColor("black").rgb())
        self.viewport = None
        self.renderer = None
        self.scene = None
        self.camera = Point3D([0.0, -2.0, 12.5])
        self.ray_depth = 3
        self.render_thread = None

        self.init_ui()
        self.init_renderer()

    def init_ui(self):
        self.setWindowTitle("PyRay")
        self.setGeometry(100, 100, self.width, self.height)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.viewport = QLabel()
        self.viewport.setFixedSize(self.viewport_width, self.viewport_height)

        settings_widget = QWidget()
        settings_widget.setFixedSize(self.width - self.viewport_width, self.viewport_height)
        settings_layout = QVBoxLayout()

        # Render Resolution Fields
        resolution_widget = QWidget()
        resolution_layout = QHBoxLayout()
        resolution_widget.setLayout(resolution_layout)
        settings_layout.addWidget(QLabel("Render Resolution:"))
        settings_layout.addWidget(resolution_widget)

        resolution_layout.addWidget(QLabel("w:"))
        render_res_w = QLineEdit(f"{self.render_width}")
        render_res_w.returnPressed.connect(lambda: self.change_render_res(render_res_w.text(), axis="w"))
        resolution_layout.addWidget(render_res_w)

        resolution_layout.addWidget(QLabel("h:"))
        render_res_h = QLineEdit(f"{self.render_height}")
        render_res_h.returnPressed.connect(lambda: self.change_render_res(render_res_h.text(), axis="h"))
        resolution_layout.addWidget(render_res_h)

        # Ray Depth Widget
        ray_depth_widget = QWidget()
        ray_depth_layout = QHBoxLayout()
        ray_depth_widget.setLayout(ray_depth_layout)
        settings_layout.addWidget(QLabel("Ray Depth:"))
        settings_layout.addWidget(ray_depth_widget)

        ray_depth = QLineEdit(f"{self.ray_depth}")
        ray_depth_layout.addWidget(ray_depth)
        ray_depth.returnPressed.connect(lambda: self.change_ray_depth(ray_depth.text()))

        # Camera Transforms
        camera_transform_widget = QWidget()
        camera_transform_layout = QHBoxLayout()
        camera_transform_widget.setLayout(camera_transform_layout)
        settings_layout.addWidget(QLabel("Camera Transform"))
        settings_layout.addWidget(camera_transform_widget)

        camera_transform_layout.addWidget(QLabel("x:"))
        camera_t_x = QLineEdit(f"{self.camera.x}")
        camera_transform_layout.addWidget(camera_t_x)
        camera_transform_layout.addWidget(QLabel("y:"))
        camera_t_y = QLineEdit(f"{self.camera.y}")
        camera_transform_layout.addWidget(camera_t_y)
        camera_transform_layout.addWidget(QLabel("z:"))
        camera_t_z = QLineEdit(f"{self.camera.z}")
        camera_transform_layout.addWidget(camera_t_z)
        camera_t_x.returnPressed.connect(lambda: self.change_camera_transform(camera_t_x.text(), transform="translate", axis="x"))
        camera_t_y.returnPressed.connect(lambda: self.change_camera_transform(camera_t_y.text(), transform="translate", axis="y"))
        camera_t_z.returnPressed.connect(lambda: self.change_camera_transform(camera_t_z.text(), transform="translate", axis="z"))

        # load Scene Buttons
        load_scene_1_btn = QPushButton("Load Scene 1")
        load_scene_1_btn.clicked.connect(partial(self.load_scene, 1))
        settings_layout.addWidget(load_scene_1_btn)

        load_scene_2_btn = QPushButton("Load Scene 2")
        load_scene_2_btn.clicked.connect(partial(self.load_scene, 2))
        settings_layout.addWidget(load_scene_2_btn)

        load_scene_3_btn = QPushButton("Load Scene 3")
        load_scene_3_btn.clicked.connect(partial(self.load_scene, 3))
        settings_layout.addWidget(load_scene_3_btn)

        start_render = QPushButton(text="Render")
        start_render.clicked.connect(self.start_render_thread)
        settings_layout.addWidget(start_render)

        restart_render = QPushButton("Restart Render")
        restart_render.clicked.connect(self.init_renderer)
        settings_layout.addWidget(restart_render)

        stop_render = QPushButton("Stop Render")
        stop_render.clicked.connect(self.stop_render_thread)
        settings_layout.addWidget(stop_render)

        self.progress_label = QLabel("Progress:")
        settings_layout.addWidget(self.progress_label)

        settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        settings_widget.setLayout(settings_layout)

        main_layout.addWidget(self.viewport)
        main_layout.addWidget(settings_widget)

        self.setLayout(main_layout)

        self.show()
        self.update_screen()

    def change_render_res(self, resolution, axis="w"):
        if axis == "w":
            self.render_width = int(resolution)
        else:
            self.render_height = int(resolution)

        self.init_renderer(restart=True)

    def change_ray_depth(self, text):
        self.ray_depth = int(text)
        self.init_renderer(restart=True)

    def change_camera_transform(self, text, transform=None, axis=None):
        match transform, axis:
            case "translate", "x":
                self.camera.y = float(text)
            case "translate", "y":
                self.camera.y = float(text)
            case "translate", "z":
                self.camera.z = float(text)

        self.init_renderer(restart=True)

    def load_scene(self, number):
        red = Color(217, 59, 59)
        green = Color(39, 163, 60)
        white = Color(255, 255, 255)
        grey = Color(180, 180, 180)
        match number:
            case 1:
                sphere1 = Sphere(Point3D([0.0, -3.5, 3.0]), 2, white, True)
                sphere2 = Sphere(Point3D([8.0, 0.0, 3.0]), 6, red, False)
                sphere3 = Sphere(Point3D([-8.0, 0.0, 3.0]), 6, green, False)
                sphere4 = Sphere(Point3D([0.0, 8.0, 3.0]), 6, grey, False)
                sphere5 = Sphere(Point3D([0.0, -8.0, 3.0]), 6, grey, False)
                sphere6 = Sphere(Point3D([0.0, 1.5, 3.0]), 0.75, green, False)
                sphere7 = Sphere(Point3D([0.0, 0.48, 3.0]), 0.33, white, True)
                sphere8 = Sphere(Point3D([0.0, 0.0, -7.5]), 6, grey, False)
                self.scene = Scene(sphere1, sphere2, sphere3, sphere4, sphere5, sphere6, sphere7, sphere8)
            case 2:
                light_sphere = Sphere(Point3D([0.0, -6.3, 3.0]), 2, white, True)
                sphere2 = Sphere(Point3D([1.5, -0.3, 3.0]), 0.415, red, False)
                sphere3 = Sphere(Point3D([-5.339, -1.948, -16.014]), 6, green, False)
                ground_sphere = Sphere(Point3D([0.0, 50.0, 3.0]), 50, grey, False)
                sphere5 = Sphere(Point3D([0, -0.75, 3]), 0.75, grey, False)
                sphere6 = Sphere(Point3D([21, -2, 22]), 11, green, False)
                #sphere7 = Sphere(Point3D([-1.5, -1.95, 28.4]), 6, white, True)
                sphere8 = Sphere(Point3D([-23.5, -2, 17.8]), 8, grey, False)
                self.scene = Scene(light_sphere, ground_sphere, sphere2, sphere3, sphere8, sphere5, sphere6)
            case 3:
                sphere1 = Sphere(Point3D([0.0, -3.5, 3.0]), 2, Color(255, 255, 255), True)
                self.scene = Scene(sphere1)

        self.init_renderer(restart=True)

    def init_renderer(self, restart=False):
        self.img = QImage(self.render_width, self.render_height, QImage.Format.Format_ARGB32)
        self.renderer = Renderer(self.update_screen, self.img, (self.render_width, self.render_height), self.ray_depth, self.scene, self.camera)

        if restart and self.render_thread:
            self.stop_render_thread()
            self.start_render_thread()

    def start_render_thread(self):
        self.render_thread = WorkerThread(self.renderer)
        self.render_thread.progress_signal.connect(self.update_progress_label)
        self.render_thread.start()
        # with cProfile.Profile() as pr:
        #    self.renderer.calculate()
        #stats = pstats.Stats(pr)
        # stats.sort_stats(pstats.SortKey.TIME)
        # stats.print_stats()
        # stats.dump_stats(filename="render_profiling.prof")

    def stop_render_thread(self):
        self.render_thread.stop()
        self.render_thread.quit()
        self.render_thread.wait()

    def update_progress_label(self, progress):
        self.progress_label.setText(f"Progress: {progress} Samples")

    def update_screen(self):
        self.viewport.setPixmap(QPixmap.fromImage(self.img.scaled(self.viewport_width, self.viewport_height)))
