from typing import Tuple
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QPushButton
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
from pyray.render_manager import RenderManager


class Window(QWidget):
    def __init__(self, window_dimensions: Tuple[int, int], parent=None) -> None:
        super().__init__(parent)
        self.window_width, self.window_height = window_dimensions
        self.viewport_width, self.viewport_height = 700, 700

        self.viewport = None
        self.render_manager = RenderManager(self.update_screen, self.update_progress_label)

        self.init_ui()
        self.init_renderer()

    def init_ui(self):
        self.setWindowTitle("PyRay")
        self.setGeometry(100, 100, self.window_width, self.window_height)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.viewport = QLabel()
        self.viewport.setFixedSize(self.viewport_width, self.viewport_height)

        settings_widget = QWidget()
        settings_widget.setFixedSize(self.window_width - self.viewport_width, self.viewport_height)
        settings_layout = QVBoxLayout()

        # Render Resolution Fields
        resolution_widget = QWidget()
        resolution_layout = QHBoxLayout()
        resolution_widget.setLayout(resolution_layout)
        settings_layout.addWidget(QLabel("Render Resolution:"))
        settings_layout.addWidget(resolution_widget)

        resolution_layout.addWidget(QLabel("w:"))
        render_res_w = QLineEdit(f"{self.render_manager.render_width}")
        render_res_w.returnPressed.connect(lambda: self.change_render_res(render_res_w.text(), axis="w"))
        resolution_layout.addWidget(render_res_w)

        resolution_layout.addWidget(QLabel("h:"))
        render_res_h = QLineEdit(f"{self.render_manager.render_height}")
        render_res_h.returnPressed.connect(lambda: self.change_render_res(render_res_h.text(), axis="h"))
        resolution_layout.addWidget(render_res_h)

        # MSAA Widget
        msaa_widget = QWidget()
        msaa_layout = QHBoxLayout()
        msaa_widget.setLayout(msaa_layout)
        settings_layout.addWidget(QLabel("Render Settings:"))
        settings_layout.addWidget(msaa_widget)

        msaa_layout.addWidget(QLabel("MSAA:"))
        msaa = QLineEdit(f"{self.render_manager.msaa}")
        msaa_layout.addWidget(msaa)
        msaa.returnPressed.connect(lambda: self.change_msaa(msaa.text()))
        msaa_layout.addWidget(QLabel("Bounces:"))
        ray_depth = QLineEdit(f"{self.render_manager.ray_depth}")
        msaa_layout.addWidget(ray_depth)
        ray_depth.returnPressed.connect(lambda: self.change_ray_depth(ray_depth.text()))

        # Camera Transforms
        camera_widget = QWidget()
        camera_layout = QGridLayout()
        camera_widget.setLayout(camera_layout)
        settings_layout.addWidget(QLabel("Camera"))
        settings_layout.addWidget(camera_widget)

        camera_layout.addWidget(QLabel("x:"), 1, 0)
        camera_t_x = QLineEdit(f"{self.render_manager.camera.pos[0]}")
        camera_layout.addWidget(camera_t_x, 1, 1)
        camera_layout.addWidget(QLabel("y:"), 1, 2)
        camera_t_y = QLineEdit(f"{self.render_manager.camera.pos[1]*-1}")
        camera_layout.addWidget(camera_t_y, 1, 3)
        camera_layout.addWidget(QLabel("z:"), 1, 4)
        camera_t_z = QLineEdit(f"{self.render_manager.camera.pos[2]}")
        camera_layout.addWidget(camera_t_z, 1, 5)

        camera_layout.addWidget(QLabel("x"), 2, 0)
        camera_layout.addWidget(QLineEdit("0"), 2, 1)
        camera_layout.addWidget(QLabel("y"), 2, 2)
        camera_layout.addWidget(QLineEdit("0"), 2, 3)
        camera_layout.addWidget(QLabel("z"), 2, 4)
        camera_layout.addWidget(QLineEdit("0"), 2, 5)

        camera_t_x.returnPressed.connect(lambda: self.change_camera(camera_t_x.text(), attribute="translate", axis="x"))
        camera_t_y.returnPressed.connect(lambda: self.change_camera(camera_t_y.text(), attribute="translate", axis="y"))
        camera_t_z.returnPressed.connect(lambda: self.change_camera(camera_t_z.text(), attribute="translate", axis="z"))

        # Sky Color
        sky_color_widget = QWidget()
        sky_color_layout = QHBoxLayout()
        sky_color_widget.setLayout(sky_color_layout)
        settings_layout.addWidget(QLabel("Skydome Color:"))
        settings_layout.addWidget(sky_color_widget)

        sky_color_layout.addWidget(QLabel("r:"))
        sky_color_r = QLineEdit(f"{self.render_manager.sky_color.r}")
        sky_color_layout.addWidget(sky_color_r)
        sky_color_layout.addWidget(QLabel("g:"))
        sky_color_g = QLineEdit(f"{self.render_manager.sky_color.g}")
        sky_color_layout.addWidget(sky_color_g)
        sky_color_layout.addWidget(QLabel("b:"))
        sky_color_b = QLineEdit(f"{self.render_manager.sky_color.b}")
        sky_color_layout.addWidget(sky_color_b)
        sky_color_r.returnPressed.connect(lambda: self.change_sky_color(sky_color_r.text(), axis="r"))
        sky_color_g.returnPressed.connect(lambda: self.change_sky_color(sky_color_g.text(), axis="g"))
        sky_color_b.returnPressed.connect(lambda: self.change_sky_color(sky_color_b.text(), axis="b"))

        # load Scene Buttons
        load_scene_1_btn = QPushButton("Load Scene 1")
        load_scene_1_btn.clicked.connect(lambda: self.render_manager.load_scene(1))
        settings_layout.addWidget(load_scene_1_btn)

        load_scene_2_btn = QPushButton("Load Scene 2")
        load_scene_2_btn.clicked.connect(lambda: self.render_manager.load_scene(2))
        settings_layout.addWidget(load_scene_2_btn)

        load_scene_3_btn = QPushButton("Start Profiling")
        load_scene_3_btn.clicked.connect(lambda: self.render_manager.profiling())
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

        self.progress_label = QLabel("")
        settings_layout.addWidget(self.progress_label)

        settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        settings_widget.setLayout(settings_layout)

        main_layout.addWidget(self.viewport)
        main_layout.addWidget(settings_widget)

        self.setLayout(main_layout)

        self.show()

    def change_render_res(self, resolution, axis="w"):
        if axis == "w":
            self.render_manager.render_width = int(resolution)
        else:
            self.render_manager.render_height = int(resolution)

        self.render_manager.init_renderer(restart=True)

    def change_msaa(self, num):
        self.render_manager.msaa = int(num)
        self.render_manager.init_renderer(restart=True)

    def change_ray_depth(self, text):
        self.render_manager.ray_depth = int(text)
        self.render_manager.init_renderer(restart=True)

    def change_camera(self, text, attribute=None, axis=None):
        match attribute, axis:
            case "translate", "x":
                self.render_manager.camera.pos = (float(text), self.render_manager.camera.pos[1], self.render_manager.camera.pos[2])
            case "translate", "y":
                self.render_manager.camera.pos = (self.render_manager.camera.pos[0], float(text)*-1, self.render_manager.camera.pos[2])
            case "translate", "z":
                self.render_manager.camera.pos = (self.render_manager.camera.pos[0], self.render_manager.camera.pos[1], float(text))
        self.render_manager.init_renderer(restart=True)

    def change_sky_color(self, text, axis=None):
        match axis:
            case "r":
                self.render_manager.sky_color.r = int(text)
            case "g":
                self.render_manager.sky_color.g = int(text)
            case "b":
                self.render_manager.sky_color.b = int(text)

        self.init_renderer(restart=True)

    def load_scene(self, number: int):
        self.render_manager.load_scene(number)

    def init_renderer(self, restart=False):
        self.render_manager.init_renderer()

    def start_render_thread(self):
        self.render_manager.start_render_thread()

    def stop_render_thread(self):
        self.render_manager.stop_render_thread()

    def update_progress_label(self, update):
        samples, sample_time, overall_time = update
        self.progress_label.setText(f"\nProgress:\n\nSamples: {samples} \nTime per Frame: {sample_time:.3f}s\nOverall Time: {overall_time:.0f}s")

    def update_screen(self, image: QImage):
        self.viewport.setPixmap(QPixmap.fromImage(image.scaled(self.viewport_width, self.viewport_height)))
