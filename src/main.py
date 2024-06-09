from src.car import get_random_car
from src.sensors import get_sensor_lines

from src.vectorlib.vector import Vector, angle
from src.vectorlib.line import Line, intersect_2D

import os
import pandas as pd


def main(
    min_x: int,
    max_x: int,
    min_y: int,
    max_y: int,
    v_min: int,
    v_max: int,
    num_sampeles: int,
    sensor_time: float,
    save_path: str,
    num_sensor_measurements: int = 3,
    negative_probability: int = 25,
    first_car_speed: int = 10,
    hit_box: int = 7,
    sensor_angle: int = 3,
):
    num_sensors = 90 // sensor_angle
    first_car = Line(Vector((0, 0)), Vector((0, first_car_speed)))

    for _ in range(num_sampeles):
        second_car = get_random_car(
            min_x, max_x, min_y, max_y, v_min, v_max, negative_probability
        )

        data = {}

        for t in [sensor_time * n for n in range(num_sensor_measurements)]:
            pos_angle = angle(Vector((1, 0)), second_car.getPoint(t))
            sensors = get_sensor_lines(
                sensor_angle, 90, *(first_car.getPoint(t).components)
            )

            start_sensor = int(pos_angle // sensor_angle)
            curr_sensor = start_sensor
            measurements = [float("inf")] * (num_sensors)

            while curr_sensor > 0:
                try:
                    sensor_t, car_t = intersect_2D(sensors[curr_sensor], second_car)

                except ZeroDivisionError:
                    curr_sensor -= 1
                    continue

                if abs(car_t * abs(second_car.v) - t * abs(second_car.v)) <= hit_box:
                    measurements[curr_sensor] = sensor_t

                else:
                    break

                curr_sensor -= 1

            curr_sensor = start_sensor + 1

            while curr_sensor < (num_sensors) - 1:
                try:
                    sensor_t, car_t = intersect_2D(sensors[curr_sensor], second_car)

                except ZeroDivisionError:
                    curr_sensor += 1
                    continue

                if abs(car_t * abs(second_car.v) - t * abs(second_car.v)) <= hit_box:
                    measurements[curr_sensor] = sensor_t

                else:
                    break

                curr_sensor += 1

            data.update(
                {
                    f"{t}x{i}": [round(measurement, 2)]
                    for i, measurement in enumerate(measurements)
                }
            )

        try:
            t_first, t_second = intersect_2D(first_car, second_car)
            t_half_first = hit_box / abs(first_car.v)
            t_half_second = hit_box / abs(second_car.v)
            collision = max(t_first - t_half_first, t_second - t_half_second) <= min(
                t_first + t_half_first, t_second + t_half_second
            )

        except ZeroDivisionError:
            collision = False

        data.update(
            {
                "collision": collision,
                "start_x": second_car.a.components[0],
                "start_y": second_car.a.components[1],
                "v_x": second_car.v.components[0],
                "v_y": second_car.v.components[1],
            }
        )

        df = pd.DataFrame(data)
        df.to_csv(
            save_path, mode="a", index=False, header=not os.path.exists(save_path)
        )
