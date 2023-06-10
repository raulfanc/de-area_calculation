import json
from .shape_management import ShapeFactory
from .json_val import validate_shape_json


def calculate_total_area(json_shapes):
    """Calculate the total area of all shapes in the given JSON data."""

    """data might corrupted during transmission, try-except to catch the invalid JSON
    and keep running to catch other errors"""
    total_area = 0
    for shape_info in json_shapes:
        try:
            shape_dict = json.loads(shape_info)
        except json.JSONDecodeError:
            print(f"Invalid JSON: {shape_info}")
            continue

        # Only calculate area for valid shapes
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
        # ------------original data above this line----------

        '{"type": "rectangle", "width": "1", "height": -5, "base": 5}',  # validation check
        '{"type": "rectangle", "width": , "height": -5}',
    ]

    # print the total area of all shapes with the format of 2 decimal places
    print(f"{calculate_total_area(json_shapes_data):.2f}")
