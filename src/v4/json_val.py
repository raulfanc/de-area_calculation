"""
renamed shape_management.py to json_val.py
- manages shapes and validation together in one script
- more considerations about the input data
- error handling not to interrupt because I want to validate all the data
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

    @staticmethod
    def validate_shape_json(shape_info):
        """Validate the necessary keys and their values for each shape type."""
        """this validation can handle multiple error in one single jsonline"""

        shape_type = shape_info.get('type')

        # Define necessary keys for each shape
        shape_keys = {
            'rectangle': [('width', float, int), ('height', float, int)],
            'triangle': [('base', float, int), ('height', float, int)],
            'circle': [('radius', float, int)],
        }

        errors = []

        # Check if the shape type is supported
        if shape_type not in shape_keys:
            errors.append(f'Unsupported shape type: "{shape_type}".')

        # Check if all necessary keys are present for the shape type and their values are correct
        for key, *value_types in shape_keys.get(shape_type, []):
            # missing key and value check
            value = shape_info.get(key)
            if value is None:
                errors.append(f'Missing required key "{key}" for shape type "{shape_type}".')
            # int,float value check
            elif not isinstance(value, tuple(value_types)):
                errors.append(
                    f'Invalid value type for key "{key}" in shape type "{shape_type}". Expected one of {value_types}, got {type(value).__name__}.')
            # positive value check
            elif value <= 0:
                errors.append(
                    f'Invalid value for key "{key}" in shape type "{shape_type}". It should be a positive number.')

        # extra key check
        extra_keys = set(shape_info.keys()) - {key for key, *_ in shape_keys.get(shape_type, [])}
        extra_keys.discard('type')  # remove 'type' from the set of extra keys
        if extra_keys:
            errors.append(f'Extra keys {extra_keys} found in shape type "{shape_type}". These are not required.')

        # If any errors were found, return them as a single string
        if errors:
            return "; ".join(errors)

        # If it passes all checks, return True
        return True

