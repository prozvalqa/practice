class Shape:
    pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def calculate_area(self):
        return 3.14 * self.radius ** 2

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def calculate_area(self):
        return self.side ** 2

shapes = [Circle(4), Square(3)]

for shape in shapes:
    print(shape.calculate_area())
