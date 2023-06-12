import unittest
from src.v3.shape_management import ShapeFactory, Rectangle, Circle, Triangle


class TestShapes(unittest.TestCase):

    def test_create_rectangle(self):
        shape_info = {'type': 'rectangle', 'width': 5, 'height': 10}
        rectangle = ShapeFactory.create_shape(shape_info)
        self.assertIsInstance(rectangle, Rectangle)
        self.assertEqual(rectangle.area(), 50)

    def test_create_circle(self):
        shape_info = {'type': 'circle', 'radius': 4}
        circle = ShapeFactory.create_shape(shape_info)
        self.assertIsInstance(circle, Circle)
        self.assertAlmostEqual(circle.area(), 50.26548245743669)

    def test_create_triangle(self):
        shape_info = {'type': 'triangle', 'base': 2, 'height': 3}
        triangle = ShapeFactory.create_shape(shape_info)
        self.assertIsInstance(triangle, Triangle)
        self.assertEqual(triangle.area(), 3)

    # def test_create_unknown_shape(self):
    #     shape_info = {'type': 'unknown', 'side': 5}
    #     unknown_shape = ShapeFactory.create_shape(shape_info)
    #     self.assertIsNone(unknown_shape)


if __name__ == '__main__':
    unittest.main()
