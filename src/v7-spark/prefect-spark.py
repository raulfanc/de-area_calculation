import json
from prefect import task, flow
from datetime import timedelta
from prefect.tasks import task_input_hash

# shape_management.py and json_val.py should be in the same directory
from .shape_management import ShapeFactory
from .json_val import validate_shape_json


@task(retries=3, log_stdout=True, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract():
    """Extract the different json from <sourcedata_url>"""


    json_shapes_data = [
        '{"type": "rectangle", "width": 5, "height": 10}',
        '{"type": "triangle", "base": 2, "height": 3}',
        '{"type": "circle", "radius": 4}',
        '{"type": "rectangle", "width": 5, "height": 5}',
        # ------------original data above this line----------

        '{"type": "rectangle", "width": "1", "height": -5, "base": 5}',  # validation check
        '{"type": "rectangle", "width": , "height": -5}',
    ]
    return json_shapes_data


@task(log_prints=True)
def validate(json_shapes):
    valid_shapes = []
    for shape_info in json_shapes:
        try:
            shape_dict = json.loads(shape_info)
        except json.JSONDecodeError:
            print(f"Invalid JSON: {shape_info}")
            continue

        # Only add valid shapes to the list
        if validate_shape_json(shape_dict):
            valid_shapes.append(shape_dict)

    return valid_shapes


@task
def calculate_area(valid_shapes):
    total_area = 0
    for shape_dict in valid_shapes:
        shape_object = ShapeFactory.create_shape(shape_dict)
        total_area += shape_object.area()

    return total_area


# Define Prefect Flow
@flow()
def flowrun():
    json_shapes = extract()
    valid_shapes = validate(json_shapes)
    total_area = calculate_area(valid_shapes)
    print(f"{total_area:.2f}")


# Run the flow
if __name__ == "__main__":
    flowrun()
