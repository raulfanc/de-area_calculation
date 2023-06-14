"""
after some research, found this jsonschema package
https://python-jsonschema.readthedocs.io/en/stable/
instead of manually define schema and validation function, this lib automatically handles them
schema seems a bit more, but with better readability for others
"""

import jsonschema

SHAPE_SCHEMAS = {
    "rectangle": {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "width": {"type": "number", "minimum": 0},
            "height": {"type": "number", "minimum": 0}
        },
        "required": ["type", "width", "height"],
        "additionalProperties": False
    },
    "triangle": {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "base": {"type": "number", "minimum": 0},
            "height": {"type": "number", "minimum": 0}
        },
        "required": ["type", "base", "height"],
        "additionalProperties": False
    },
    "circle": {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "radius": {"type": "number", "minimum": 0}
        },
        "required": ["type", "radius"],
        "additionalProperties": False
    },
    # Add more shape schemas here for future extensive support
}


# def validate_shape_json(shape_info):
#     """stop at the first error, good practice"""
#     shape_type = shape_info.get('type')
#     schema = SHAPE_SCHEMAS.get(shape_type)
#
#     if schema:
#         try:
#             jsonschema.validate(shape_info, schema)
#             return True
#         except jsonschema.exceptions.ValidationError as e:
#             print(f'Validation error for shape: {e.message}')
#             return False
#     else:
#         print(f'Unsupported shape type: "{shape_type}"')
#         return False

def validate_shape_json(shape_info):
    """capture all errors"""
    shape_type = shape_info.get('type')
    schema = SHAPE_SCHEMAS.get(shape_type)

    if schema:
        validator = jsonschema.Draft7Validator(schema)                                               # different versions can be used, V7 is the latest 2023
        """https://python-jsonschema.readthedocs.io/en/latest/validate/#the-validator-protocol"""
        errors = sorted(validator.iter_errors(shape_info), key=lambda e: e.path)                     # great API to handle errors
        if errors:
            for error in errors:
                print(f'Validation error for shape: {error.message}')
            return False
        return True
    else:
        print(f'Unsupported shape type: "{shape_type}"')
        return False

