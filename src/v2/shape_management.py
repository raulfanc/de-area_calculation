"""
similar to v1, but separate the shape management and area calculation
"""

import math


class Shape:
    """Abstract base class for different shapes."""

    def area(self):
        """Calculate and return the area of the shape."""
        pass


class Rectangle(Shape):
    """Rectangle shape."""

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        """Calculate and return the area of the rectangle."""
        return self.width * self.height


class Triangle(Shape):
    """Triangle shape."""

    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        """Calculate and return the area of the triangle."""
        return 0.5 * self.base * self.height


class Circle(Shape):
    """Circle shape."""

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        """Calculate and return the area of the circle."""
        return math.pi * self.radius ** 2


class ShapeFactory:
    """Factory class for creating shape objects."""

    SHAPE_CLASS_MAP = {
        'rectangle': Rectangle,
        'triangle': Triangle,
        'circle': Circle
        # add more shape classes here for future extensive support
        # 'new-shape': NewShape
    }

    @staticmethod
    def create_shape(shape_info):
        """Create a shape object from the given shape dictionary."""
        shape_type = shape_info.pop('type')
        shape_class = ShapeFactory.SHAPE_CLASS_MAP.get(shape_type)

        if shape_class:
            return shape_class(**shape_info)
        else:
            print(f'Unsupported shape type: "{shape_type}"')
            return None
