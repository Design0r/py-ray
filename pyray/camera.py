import glm


class Camera:
    def __init__(self, pos: glm.vec3, rot, focal: float) -> None:
        self.pos: glm.vec3 = pos
        self.rot = rot
        self.fov: float = self.deg_to_rad(focal)

    def deg_to_rad(self, fov_deg) -> float:
        return fov_deg * glm.pi() / 180

    def rad_to_deg(self, fov_rad) -> float:
        return fov_rad * (180/glm.pi())

    def focal_to_rad(self, focal_length) -> float:
        # 2 arctan (x / (2 f))
        rad = 2 * glm.atan(36 / (2 * focal_length))
        return rad

    def rad_to_focal(self, fov_rad):
        # (sensor width/2) / tan(FOV/2)
        return (36 / 2) / glm.tan(fov_rad / 2)
