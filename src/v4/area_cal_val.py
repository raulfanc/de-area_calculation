import json
from .json_val import ShapeFactory


def calculate_total_area(json_shapes):
    """Calculate the total area of all shapes in the given JSON data."""

    total_area = 0
    for shape_info in json_shapes:
        shape_dict = json.loads(shape_info)

        # Validate the shape data
        validation_result = ShapeFactory.validate_shape_json(shape_dict)

        # Only calculate area for valid shapes
        if validation_result is True:
            shape_object = ShapeFactory.create_shape(shape_dict)
            total_area += shape_object.area()
        else:
            print(f'Validation error: {validation_result}')

    return total_area



if __name__ == '__main__':
    json_shapes_data = [
        '{"type": "rectangle", "width": 5, "height": 10}',
        '{"type": "triangle", "base": 2, "height": 3}',
        '{"type": "circle", "radius": 4}',
        '{"type": "rectangle", "width": 5, "height": 5}',
        # ------------original data above this line----------

        '{"type": "rectangle", "width": "1", "height": -5, "base": 5}',    # validation check
    ]

    # print the total area of all shapes with the format of 2 decimal places
    print(f"{calculate_total_area(json_shapes_data):.2f}")
