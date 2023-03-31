import sys
import time
from pyray.color import Color
from pyray.point_3d import Point3D
from pyray.renderer import Renderer
from pyray.scene import Scene
from pyray.sphere import Sphere

sphere1 = Sphere(Point3D(0.0, -3.5, 3.0), 2, Color(255, 255, 255), True)
sphere2 = Sphere(Point3D(8.0, 0.0, 3.0), 6, Color(255, 255, 255), False)
sphere3 = Sphere(Point3D(-8.0, 0.0, 3.0), 6, Color(255, 255, 255), False)
sphere4 = Sphere(Point3D(0.0, 8.0, 3.0), 6, Color(255, 255, 255), False)
sphere5 = Sphere(Point3D(0.0, -8.0, 3.0), 6, Color(255, 255, 255), False)
sphere6 = Sphere(Point3D(0.0, 1.5, 3.0), 0.75, Color(0, 255, 0), False)
sphere7 = Sphere(Point3D(0.0, 0.48, 3.0), 0.33, Color(255, 255, 255), True)
sphere8 = Sphere(Point3D(0.0, 0.0, -7.5), 6, Color(255, 255, 255), False)

scene = Scene(sphere1, sphere2, sphere3, sphere4, sphere5, sphere6, sphere7, sphere8)
renderer = Renderer(scene, 128, 128, Point3D(0, 0, 10), 4)

start_time = time.time()

for _ in range(100):
    renderer.calculate()
    renderer.update_screen()
    renderer.app.processEvents()

print(f"Finished Rendering in {time.time() - start_time}s")

sys.exit(renderer.app.exec())
