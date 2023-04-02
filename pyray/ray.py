class Ray:
    def __init__(self, origin, direction) -> None:
        self.origin = origin
        self.direction = direction

    def __repr__(self) -> str:
        return f"Origin: {self.origin}, Direction: {self.direction}"
