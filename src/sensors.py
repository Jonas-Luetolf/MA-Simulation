from src.vectorlib.vector import Vector
from src.vectorlib.line import Line

from math import cos, sin, radians


def get_sensor_lines(angel: int, view_angel: int = 180, pos_x: int = 0, pos_y: int = 0):
    sensors = []
    num_sensors = view_angel // angel

    for i in range(num_sensors):
        dir_x = cos(radians(angel * i))
        dir_y = sin(radians(angel * i))

        dir_vec = Vector((dir_x, dir_y))

        sensors.append(Line(Vector((pos_x, pos_y)), dir_vec))

    return sensors
