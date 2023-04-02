class Color:
    def __init__(self, r, g, b, a=1) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def to_rgbf(self):
        self.r /= 255
        self.g /= 255
        self.b /= 255

        return self

    def to_rgbi(self):
        self.r *= 255
        self.g *= 255
        self.b *= 255

    def __repr__(self) -> str:
        return f"r: {self.r}, g: {self.g}, b: {self.b}, a: {self.a}"
