from unittest import TestCase
from src.vectorlib.vector import Vector, angle


class TestVector(TestCase):
    def test_init(self):
        self.assertEqual(
            [1, 2, 3],
            Vector([1, 2, 3]).components,
            "Vector initialization with list failed",
        )
        self.assertEqual(
            [1, 2, 3],
            Vector((1, 2, 3)).components,
            "Vector initialization with tuple failed",
        )

    def test_abs(self):
        self.assertEqual(
            7, abs(Vector([2, 3, 6])), "Callculation of absolut value failed"
        )

    def test_add_sub(self):
        self.assertEqual(
            [3, 6, 9],
            (Vector((1, 2, 3)) + Vector((2, 4, 6))).components,
            "addition of Vectors failed",
        )
        self.assertEqual(
            [1, 2, 3],
            (Vector((3, 6, 9)) - Vector((2, 4, 6))).components,
            "subtraction of Vectors failed",
        )
        self.assertRaises(
            TypeError,
            lambda: Vector((1, 2, 3)) + 2,
            "TypeError not raised: addition between Vector and number",
        )
        self.assertRaises(
            TypeError,
            lambda: Vector((1, 2, 3)) - 2,
            "TypeError not raised: subtraction between Vector and number",
        )

    def test_mul_div(self):
        self.assertEqual(
            [2, 4, 6],
            (Vector((1, 2, 3)) * 2).components,
            "multiplication of Vector and number failed",
        )
        self.assertEqual(
            [1, 2, 3],
            (Vector((2, 4, 6)) / 2).components,
            "division of Vector and number failed",
        )

        self.assertRaises(
            TypeError,
            lambda: Vector((1, 2, 3)) * Vector((1, 2, 3)),
            "TypeError not raised: multiplication between Vector and number",
        )

        self.assertRaises(
            TypeError,
            lambda: Vector((1, 2, 3)) / Vector((1, 2, 3)),
            "TypeError not raised: division between Vector and number",
        )

    def test_angle(self):
        self.assertEqual(
            90.0,
            angle(Vector((1, 0)), Vector((0, 1))),
        )
        self.assertEqual(45.0, angle(Vector((0, 1)), Vector((1, 1))))
