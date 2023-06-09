import json
from shape_management import ShapeFactory


def calculate_total_area(json_shapes):
    """Calculate the total area of all shapes in the given JSON data."""

    total_area = 0
    for shape_info in json_shapes:
        shape_dict = json.loads(shape_info)
        shape_object = ShapeFactory.create_shape(shape_dict)

        if shape_object is not None:
            total_area += shape_object.area()

    return total_area


if __name__ == '__main__':
    json_shapes_data = [
        '{"type": "rectangle", "width": 5, "height": 10}',
        '{"type": "triangle", "base": 2, "height": 3}',
        '{"type": "circle", "radius": 4}',
        '{"type": "rectangle", "width": 5, "height": 5}',
        '{"type": "very round", "width": 5, "height": 5}',    # unsupported shape, not calculated in total area
    ]

    print(calculate_total_area(json_shapes_data))
