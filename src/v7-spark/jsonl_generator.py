"""
for testing, include more invlid data, to test the robustness of the datapipeline
"""

import json
import random

shape_data = []

for _ in range(1000):
    # Randomly select a shape
    shape_type = random.choice(["rectangle", "triangle", "circle", "polygon", "ellipse"])

    if shape_type == "rectangle":
        if random.random() < 0.1:
            shape_data.append({"type": "rectangle", "width": "a", "height": -1, "extra": random.randint(1, 10)})
        else:
            shape_data.append({"type": "rectngle", "width": random.randint(1, 10), "height": random.randint(1, 10)})

    elif shape_type == "triangle":
        if random.random() < 0.1:
            shape_data.append({"typ": "triangle", "base": -1, "height": "b"})
        else:
            shape_data.append({"type": "triangle", "base": random.randint(1, 10), "height": random.randint(1, 10),
                               "extra": random.randint(1, 10)})

    elif shape_type == "circle":
        if random.random() < 0.1:
            shape_data.append({"type": "circle", "radius": "c"})
        else:
            shape_data.append(
                {"type": "circle", "radius": random.randint(1, 10), "color": random.choice(["red", "green", "blue"])})


    elif shape_type == "polygon":
        if random.random() < 0.1:
            shape_data.append({"type": "polygon", "sides": "x", "length": -1})
        else:
            shape_data.append({"type": "polygon", "sides": random.randint(3, 10), "length": random.randint(1, 10)})

    elif shape_type == "ellipse":
        if random.random() < 0.1:
            shape_data.append({"type": "ellipse", "major_axis": "y", "minor_axis": "z"})
        else:
            shape_data.append(
                {"type": "ellipse", "major_axis": random.randint(1, 10), "minor_axis": random.randint(1, 10)})

# Write data to .jsonl file
with open('dummy_data.jsonl', 'w') as f:
    for shape in shape_data:
        json.dump(shape, f)
        f.write('\n')
