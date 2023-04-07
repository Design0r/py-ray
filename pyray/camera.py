import math


class Camera:
    def __init__(self, pos, rot, focal) -> None:
        self.pos = pos
        self.rot = rot
        self.fov = self.deg_to_rad(focal)

    def deg_to_rad(self, fov_deg) -> float:
        return fov_deg * math.pi / 180

    def rad_to_deg(self, fov_rad) -> float:
        return fov_rad * (180/math.pi)

    def focal_to_rad(self, focal_length) -> float:
        # 2 arctan (x / (2 f))
        rad = 2 * math.atan(36 / (2 * focal_length))
        return rad

    def rad_to_focal(self, fov_rad):
        # (sensor width/2) / tan(FOV/2)
        return (36 / 2) / math.tan(fov_rad / 2)
