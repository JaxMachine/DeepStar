import math


class Vector:
    def __init__(self, x=None, y=None, tuple_input=None):
        self.x = x if tuple_input is None else tuple_input[0]
        self.y = y if tuple_input is None else tuple_input[1]

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

    def mult(self, scalarx, scalary):
        return Vector(self.x * scalarx, self.y * scalary)

    def dot(self, other):
        return ((self.x * other.x) + (self.y * other.y))

    def __div__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def to_tuple(self):
        return self.x, self.y

    def length(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5

    def normal(self):
        return self / self.length()


class Circle:

    def __init__(self, x, y, radius):
        self.center = Vector(x, y)
        self.radius = radius

    def intersects_line(self, start_vector, end_vector):
        V = end_vector - start_vector
        a = V.dot(V)
        b = 2 * V.dot(start_vector - self.center)
        c = start_vector.dot(start_vector) + self.center.dot(self.center) - 2 * start_vector.dot(self.center) - self.radius ** 2

        disc = b**2 - 4 * a * c
        if disc < 0:
            return False

        sqrt_disc = math.sqrt(disc)
        t1 = (-b + sqrt_disc) / (2 * a)
        t2 = (-b - sqrt_disc) / (2 * a)

        if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
            return False

        return True

    def intersects_rect(self, rect):
        return (rect.collidepoint(self.center.x, self.center.y) or
                self.intersects_line(Vector(tuple_input=rect.topleft), Vector(tuple_input=rect.bottomleft)) or
                self.intersects_line(Vector(tuple_input=rect.bottomleft), Vector(tuple_input=rect.bottomright)) or
                self.intersects_line(Vector(tuple_input=rect.bottomright), Vector(tuple_input=rect.topright)) or
                self.intersects_line(Vector(tuple_input=rect.topright), Vector(tuple_input=rect.topleft)))
