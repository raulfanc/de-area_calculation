import json
import random

shape_data = []
data_size = 1000

for _ in range(data_size):
    # Randomly select a shape
    shape_type = random.choice(["rectangle", "triangle", "circle"])

    if shape_type == "rectangle":
        # Occasionally generate invalid data
        if random.random() < 0.1:
            shape_data.append({"type": "rectangle", "width": "a", "height": -1})
        else:
            shape_data.append({"type": "rectangle", "width": random.randint(1, 10), "height": random.randint(1, 10)})

    elif shape_type == "triangle":
        if random.random() < 0.1:
            shape_data.append({"type": "triangle", "base": -1, "height": "b"})
        else:
            shape_data.append({"type": "triangle", "base": random.randint(1, 10), "height": random.randint(1, 10)})

    elif shape_type == "circle":
        if random.random() < 0.1:
            shape_data.append({"type": "circle", "radius": "c"})
        else:
            shape_data.append({"type": "circle", "radius": random.randint(1, 10)})

# Write data to .jsonl file
with open('dummy_data.jsonl', 'w') as f:
    for shape in shape_data:
        json.dump(shape, f)
        f.write('\n')
