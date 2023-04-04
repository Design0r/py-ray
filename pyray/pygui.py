from pyray.color import Color
from pyray.point_3d import Point3D
from pyray.renderer import Renderer
from pyray.scene import Scene
from pyray.sphere import Sphere
from functools import partial


class RenderUI:
    def __init__(self, window_dimensions, render_resolution) -> None:
        self.stop_flag = True

        self.window_width, self.window_height = window_dimensions
        self.viewport_width, self.viewport_height = render_resolution
        self.render_width, self.render_height = render_resolution
        self.downscaling = 4

        self.renderer = None
        self.scene = None
        self.img_buffer = np.array([0] * (self.render_width * self.render_height * 4))

        self.load_scene(1)
        self.run_ui()

    def run_ui(self):
        dpg.create_context()
        dpg.create_viewport(title='PyRay', width=self.window_width, height=self.window_height)
        dpg.setup_dearpygui()
        dpg.configure_app(docking=True, docking_space=True, init_file="dpg.ini")

        self.ui_elements()

        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            self.render()
            dpg.render_dearpygui_frame()
        dpg.destroy_context()

    def ui_elements(self):
        dpg.add_texture_registry(tag="texture_container")
        dpg.add_raw_texture(self.render_width, self.render_height, default_value=self.img_buffer,
                            format=dpg.mvFormat_Float_rgba, parent="texture_container", tag="image_texture")

        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)

        with dpg.item_handler_registry(tag="viewport_handler"):
            dpg.add_item_resize_handler(callback=self.on_resize)

        with dpg.window(label="Viewport", tag="Viewport", no_scrollbar=True, on_close=self._on_demo_close):
            dpg.draw_image("image_texture", (0, 0), (self.viewport_width, self.viewport_height), tag="draw_image")

        with dpg.window(label="Settings", tag="Settings"):
            dpg.add_button(label="Load Scene: 1", callback=partial(self.load_scene, 1))
            dpg.add_button(label="Load Scene: 2", callback=partial(self.load_scene, 2))
            dpg.add_button(label="Load Scene: 3", callback=partial(self.load_scene, 3))
            dpg.add_button(label="Render", callback=self.start_render)
            dpg.add_button(label="Stop Render", callback=self.stop_render)
            dpg.add_button(label="Save UI", callback=self.save_ui)

        dpg.bind_item_theme("Viewport", global_theme)
        dpg.bind_item_handler_registry("Viewport", "viewport_handler")

    def save_ui(self):
        dpg.save_init_file("dpg.ini")

    def stop_render(self):
        self.stop_flag = True

    def start_render(self):
        self.on_resize()
        self.stop_flag = False

    def on_resize(self):
        self.stop_render()

        size = dpg.get_item_rect_size("Viewport")
        self.viewport_width, self.viewport_height = size

        dpg.configure_item("image_texture", width=self.render_width, height=self.render_height, format=dpg.mvFormat_Float_rgba, parent="texture_container", tag="image_texture")

        smaller = min([self.viewport_height, self.viewport_width])
        dpg.configure_item("draw_image", pmin=(0, 0), pmax=(smaller, smaller))
        self.load_scene(1)

    def render(self):
        if not self.stop_flag:
            dpg.set_value("image_texture", self.renderer.calculate())

    def _on_demo_close(self, sender, app_data, user_data):
        dpg.delete_item(sender)
        dpg.delete_item("image_container")
        dpg.delete_item("image_texture")

    def load_scene(self, number):
        match number:
            case 1:
                sphere1 = Sphere(Point3D(0.0, -3.5, 3.0), 2, Color(1.0, 1.0, 1.0), True)
                sphere2 = Sphere(Point3D(8.0, 0.0, 3.0), 6, Color(1.0, 1.0, 1.0), False)
                sphere3 = Sphere(Point3D(-8.0, 0.0, 3.0), 6, Color(1.0, 1.0, 1.0), False)
                sphere4 = Sphere(Point3D(0.0, 8.0, 3.0), 6, Color(1.0, 1.0, 1.0), False)
                sphere5 = Sphere(Point3D(0.0, -8.0, 3.0), 6, Color(1.0, 1.0, 1.0), False)
                sphere6 = Sphere(Point3D(0.0, 1.5, 3.0), 0.75, Color(0.0, 1.0, 0.0), False)
                sphere7 = Sphere(Point3D(0.0, 0.48, 3.0), 0.33, Color(1.0, 1.0, 1.0), True)
                sphere8 = Sphere(Point3D(0.0, 0.0, -7.5), 6, Color(1.0, 1.0, 1.0), False)
                self.scene = Scene(sphere1, sphere2, sphere3, sphere4, sphere5, sphere6, sphere7, sphere8)
            case 2:
                sphere1 = Sphere(Point3D(0.0, -3.5, 3.0), 2, Color(1.0, 1.0, 1.0), True)
                sphere2 = Sphere(Point3D(8.0, 0.0, 3.0), 6, Color(1.0, 1.0, 1.0), False)
                self.scene = Scene(sphere1, sphere2)
            case 3:
                sphere1 = Sphere(Point3D(0.0, -3.5, 3.0), 2, Color(1.0, 1.0, 1.0), True)
                self.scene = Scene(sphere1)

        self.renderer = Renderer(self.render_width, self.render_height, self.scene, Point3D(0, 0, 10))


RenderUI((1000, 700), (128, 128))
