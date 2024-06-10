from src.vectorlib.vector import Vector


class Line:
    def __init__(self, a: Vector, v: Vector) -> None:
        assert isinstance(a, Vector)
        assert isinstance(v, Vector)
        assert len(a.components) == len(v.components)
        self.a = a
        self.v = v

    def getPoint(self, t) -> Vector:
        assert isinstance(t, (float, int))
        return self.v * t + self.a


def get_normal_2D(g: Line):
    assert isinstance(g, Line)
    assert len(g.v.components) == 2
    v = list(reversed(g.v.components))
    v[0] = v[0] * -1
    return Line(g.a, Vector(v))


def intersect_2D(g: Line, h: Line):
    assert isinstance(g, Line)
    assert isinstance(h, Line)
    assert len(g.a.components) == len(h.a.components) == 2

    det_A = g.v[0] * (-h.v[1]) - g.v[1] * (-h.v[0])
    det_A1 = (h.a[0] - g.a[0]) * (-h.v[1]) - (h.a[1] - g.a[1]) * (-h.v[0])
    det_A2 = g.v[0] * (h.a[1] - g.a[1]) - g.v[1] * (h.a[0] - g.a[0])

    t = det_A1 / det_A
    s = det_A2 / det_A

    return t, s
