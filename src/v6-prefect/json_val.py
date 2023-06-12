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
        validator = jsonschema.Draft7Validator(schema)
        errors = sorted(validator.iter_errors(shape_info), key=lambda e: e.path)
        if errors:
            for error in errors:
                print(f'Validation error for shape: {error.message}')
            return False
        return True
    else:
        print(f'Unsupported shape type: "{shape_type}"')
        return False


# # function to log the validation errors into a text file in this directory:
# def log_validation_errors(shape_info):
#     shape_type = shape_info.get('type')
#     schema = SHAPE_SCHEMAS.get(shape_type)
#
#     if schema:
#         validator = jsonschema.Draft7Validator(schema)
#         errors = sorted(validator.iter_errors(shape_info), key=lambda e: e.path)
#         if errors:
#             with open('validation_errors.txt', 'a') as f:
#                 for error in errors:
#                     f.write(f'Validation error for shape: {error.message}\n')
#             return False
#         return True
#     else:
#         print(f'Unsupported shape type: "{shape_type}"')
#         return False


