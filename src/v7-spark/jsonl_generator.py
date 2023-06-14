import json
import random

shape_data = []

for _ in range(1000):
    # Randomly select a shape type, including typo versions and additional shapes
    shape_type = random.choice(["rectangle", "triangle", "circle", "polygon", "ellipse",
                                "regtngle", "tringle", "circel", "poligon", "elipse"])

    if shape_type in ["rectangle", "regtngle"]:
        if random.random() < 0.1:
            # 10% chance to generate invalid data
            shape_data.append({"type": shape_type, "width": "a", "height": -1, "extra": random.randint(1, 10)})
        else:
            # 90% chance to generate valid data
            shape_data.append({"type": shape_type, "width": random.randint(1, 10), "height": random.randint(1, 10)})

    elif shape_type in ["triangle", "tringle"]:
        if random.random() < 0.1:
            # 10% chance to generate invalid data
            shape_data.append({"type": shape_type, "base": -1, "height": "b"})
        else:
            # 90% chance to generate valid data
            shape_data.append({"type": shape_type, "base": random.randint(1, 10), "height": random.randint(1, 10)})

    elif shape_type in ["circle", "circel"]:
        if random.random() < 0.1:
            # 10% chance to generate invalid data
            shape_data.append({"type": shape_type, "radius": "c"})
        else:
            # 90% chance to generate valid data
            shape_data.append({"type": shape_type, "radius": random.randint(1, 10)})

    elif shape_type in ["polygon", "poligon"]:
        if random.random() < 0.1:
            # 10% chance to generate invalid data
            shape_data.append({"type": shape_type, "sides": "x", "length": -1})
        else:
            # 90% chance to generate valid data
            shape_data.append({"type": shape_type, "sides": random.randint(3, 10), "length": random.randint(1, 10)})

    elif shape_type in ["ellipse", "elipse"]:
        if random.random() < 0.1:
            # 10% chance to generate invalid data
            shape_data.append({"type": shape_type, "major_axis": "y", "minor_axis": "z"})
        else:
            # 90% chance to generate valid data
            shape_data.append({"type": shape_type, "major_axis": random.randint(1, 10), "minor_axis": random.randint(1, 10)})

# Write data to .jsonl file
with open('dummy_data.json', 'w') as f:
    for shape in shape_data:
        json.dump(shape, f)
        f.write(',\n')
