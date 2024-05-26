from src.vectorlib.vector import Vector
from src.vectorlib.line import Line
from random import randrange


def get_random_car(
    min_x: int,
    max_x: int,
    min_y: int,
    max_y: int,
    v_min: int,
    v_max: int,
    negative_probability: int = 50,
):
    sign_x = (randrange(100) > negative_probability) * (-1)
    sign_y = (randrange(100) > negative_probability) * (-1)

    # Position
    x_pos = randrange(min_x, max_x, 1)
    y_pos = randrange(min_y, max_y, 1)
    start_vec = Vector((x_pos, y_pos))

    # Speed
    v_x = randrange(v_min, v_max, 1) * sign_x
    v_y = randrange(v_min, v_max, 1) * sign_y

    v_vec = Vector((v_x, v_y))

    return Line(start_vec, v_vec)
