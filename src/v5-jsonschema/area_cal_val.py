"""
core function remains the same
"""
import json
from shape_management import ShapeFactory
from json_val import validate_shape_json, SHAPE_SCHEMAS


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


def calculate_total_area(json_shapes):
    """Calculate the total area of all shapes in the given JSON data."""
    total_area = 0
    for shape_info in json_shapes:
        # Only calculate area for valid shapes
        if validate_shape_json(shape_info):
            shape_object = ShapeFactory.create_shape(shape_info)
            total_area += shape_object.area()

    return total_area


if __name__ == '__main__':
    # Load JSONL data from a file
    json_shapes_data = []
    with open('dummy_data.jsonl', 'r') as f:
        for line in f:
            try:
                shape_info = json.loads(line)
                json_shapes_data.append(shape_info)
            except json.JSONDecodeError:
                print(f"Invalid JSON: {line.strip()}")

    # print the total area of all shapes with the format of 2 decimal places
    print(f"{calculate_total_area(json_shapes_data):.2f}")
