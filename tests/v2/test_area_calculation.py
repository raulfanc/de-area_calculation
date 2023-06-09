import unittest
from src.v2.area_calculation import calculate_total_area


class TestCalculateArea(unittest.TestCase):

    def test_calculate_total_area(self):
        json_shapes_data = [
            '{"type": "rectangle", "width": 5, "height": 10}',
            '{"type": "triangle", "base": 2, "height": 3}',
            '{"type": "circle", "radius": 4}',
            '{"type": "rectangle", "width": 5, "height": 5}',
        ]
        total_area = calculate_total_area(json_shapes_data)
        self.assertAlmostEqual(total_area, 128.27, places=2)


if __name__ == '__main__':
    unittest.main()
