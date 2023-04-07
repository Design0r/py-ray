from __future__ import annotations


class Color:
    def __init__(self, r, g, b, a=1) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __mul__(self, factor):
        return Color(self.r * factor, self.g * factor, self.b * factor)

    def __add__(self, color: Color) -> Color:
        return Color(self.r + color.r, self.g + color.g, self.b + color.b)

    def __itruediv__(self, factor) -> Color:
        return Color(self.r / factor, self.g / factor, self.b / factor)

    def __repr__(self) -> str:
        return f"r: {self.r}, g: {self.g}, b: {self.b}, a: {self.a}"
