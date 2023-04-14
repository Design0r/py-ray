import glm


class Ray:
    def __init__(self, origin: glm.vec3, direction: glm.vec3) -> None:
        self.origin: glm.vec3 = origin
        self.direction: glm.vec3 = direction

    def __repr__(self) -> str:
        return f"Origin: {self.origin}, Direction: {self.direction}"
