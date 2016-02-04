

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        output = str(self.x)
        output += " : "
        output += str(self.y)
        return output

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def length(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5

    def normal(self):
        return self / self.length()
