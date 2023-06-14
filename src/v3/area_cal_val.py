"""
on top of v2, added validation check for `keys`.
"""

import json
from .shape_management import ShapeFactory


def validate_shape_json(shape_info):
    """Validate the necessary keys for each shape type."""
    """added in v3"""

    shape_type = shape_info.get('type')

    # Define necessary keys for each shape
    shape_keys = {
        'rectangle': ['width', 'height'],
        'triangle': ['base', 'height'],
        'circle': ['radius'],
    }

    # Check if the shape type is supported
    if shape_type not in shape_keys:
        print(f'Unsupported shape type: "{shape_type}"')
        return False

    # Check if all necessary keys are present for the shape type
    for key in shape_keys[shape_type]:
        if key not in shape_info:
            print(f'Missing key "{key}" for shape type "{shape_type}"')
            return False

    # If it passes all checks, return True
    return True


def calculate_total_area(json_shapes):
    """Calculate the total area of all shapes in the given JSON data."""

    total_area = 0
    for shape_info in json_shapes:
        shape_dict = json.loads(shape_info)

        # Only calculate area for valid shapes, added in v3
        if validate_shape_json(shape_dict):
            shape_object = ShapeFactory.create_shape(shape_dict)
            total_area += shape_object.area()

    return total_area


if __name__ == '__main__':
    json_shapes_data = [
        '{"type": "rectangle", "width": 5, "height": 10}',
        '{"type": "triangle", "base": 2, "height": 3}',
        '{"type": "circle", "radius": 4}',
        '{"type": "rectangle", "width": 5, "height": 5}',
        '{"type": "very round", "width": 5, "height": 5}',  # unsupported shape, not calculated in total area
        '{"type": "rectangle", "base": 5, "height": 5}',    # upsupported key, not calculated in total area
    ]

    # print the total area of all shapes with the format of 2 decimal places
    print(f"{calculate_total_area(json_shapes_data):.2f}")
