"""
object-oriented programming
- `Shape` abstract base class, serving as the blueprint for all shapes.
- defines a method area() that will be overridden in the subclasses to calculate the area of a particular shape.
- inherited classes: Rectangle, Triangle, Circle and more shapes, calculate area
- create more shapes without specifying the exact class of object that will be created
- handles unsupported shapes
"""

import math
import json


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


## create a new shape class below for future extensive support
# class NewShape(Shape):
#     """New shape."""


class ShapeFactory:
    """Factory class for creating shape objects."""

    SHAPE_MAP = {
        'rectangle': Rectangle,
        'triangle': Triangle,
        'circle': Circle
        # add more shape classes below for future extensive support
        # 'new-shape': NewShape
    }

    @staticmethod
    def create_shape(shape_dict):
        """Create a shape object from the given shape dictionary."""
        shape_type = shape_dict.pop('type')                     # filter out the value of 'type' key
        shape_class = ShapeFactory.SHAPE_MAP.get(shape_type)    # get the class of the shape type

        if shape_class:
            return shape_class(**shape_dict)                    # create a shape object from the shape class
        else:
            print(f"Unsupported shape type: {shape_type}")      # print out the unsupported shape type
            return None


def calculate_total_area(json_data):
    """Calculate the total area of all shapes in the given JSON data."""

    total_area = 0
    for line in json_data:
        shape_dict = json.loads(line)                        # contain shape type and their dimensions
        shape = ShapeFactory.create_shape(shape_dict)        # returns shape objects

        if shape is not None:                                # check with ShapeFactory if the shape is supported
            total_area += shape.area()                       # call the area() method to add total areas

    return total_area


json_data = [
    '{"type": "rectangle", "width": 5, "height": 10}',
    '{"type": "triangle", "base": 2, "height": 3}',
    '{"type": "circle", "radius": 4}',
    '{"type": "rectangle", "width": 5, "height": 5}',
    '{"type": "very round", "width": 5, "height": 5}',  # unsupported shape, not calculated in total area
]




print(calculate_total_area(json_data))
