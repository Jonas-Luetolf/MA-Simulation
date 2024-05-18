from unittest import TestCase
from src.vectorlib.line import Line, intersect_2D
from src.vectorlib.vector import Vector


class TestLine(TestCase):
    def test_get_Point(self):
        self.assertEqual(
            [3, 6, 9],
            (Line(Vector((1, 2, 3)), Vector((1, 2, 3))).getPoint(2)).components,
            "get wrong Point",
        )

    def test_intersect_2D(self):
        g = Line(Vector((2, 4)), Vector((1, 4)))
        h = Line(Vector((5, 10)), Vector((-2, -5)))
        self.assertEqual((-1, 2), intersect_2D(g, h))
        self.assertEqual(g.getPoint(-1).components, h.getPoint(2).components)
