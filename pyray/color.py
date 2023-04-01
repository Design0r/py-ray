class Color:
    def __init__(self, r, g, b, a=1) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __repr__(self) -> str:
        return f"r: {self.r}, g: {self.g}, b: {self.b}, a: {self.a}"
