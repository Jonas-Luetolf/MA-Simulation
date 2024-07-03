from src.car import get_random_car
from src.sensors import get_sensor_lines

from src.vectorlib.vector import Vector, angle, vector_to_len
from src.vectorlib.line import Line, get_normal_2D, intersect_2D

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
    negative_probability: int = 10,
    first_car_speed: int = 10,
    hit_box_horizontal: int = 7,
    hit_box_vertical: int = 2,
    sensor_angle: int = 1,
):
    num_sensors = 90 // sensor_angle
    first_car = Line(Vector((0, 0)), Vector((0, first_car_speed)))
    for _ in range(num_sampeles):
        second_car = get_random_car(
            min_x, max_x, min_y, max_y, v_min, v_max, negative_probability
        )

        data = {}
        for t in [sensor_time * n for n in range(num_sensor_measurements)]:
            pos_angle = angle(
                Vector((1, 0)), second_car.getPoint(t) - first_car.getPoint(t)
            )

            # calculate front and back line
            sensors = get_sensor_lines(
                sensor_angle, 90, *first_car.getPoint(t).components
            )
            front_line = get_normal_2D(second_car)
            front_line.a = second_car.getPoint(t) + vector_to_len(
                second_car.v, hit_box_horizontal
            )

            back_line = get_normal_2D(second_car)
            back_line.a = second_car.getPoint(t) - vector_to_len(
                second_car.v, hit_box_horizontal
            )

            start_sensor = int(pos_angle // sensor_angle)
            measurements = [float("inf")] * (num_sensors)
            hits = [0, 0, 0]
            distances = [float("inf")] * 3
            hits_n = 0
            sensors_ordered = [start_sensor]
            i = 1
            while (start_sensor - i) >= 0 or start_sensor + i < num_sensors:
                if start_sensor - i >= 0:
                    sensors_ordered.append(start_sensor - i)

                if start_sensor + i < num_sensors:
                    sensors_ordered.append(start_sensor + i)
                i += 1

            not_detect_last = 0

            for sensor in sensors_ordered:
                try:
                    distances[0], front_t = intersect_2D(sensors[sensor], front_line)
                    distances[1], back_t = intersect_2D(sensors[sensor], back_line)
                    distances[2], second_car_t = intersect_2D(
                        sensors[sensor], second_car
                    )

                except ZeroDivisionError:
                    continue

                hits[0] = abs(front_t * abs(front_line.v)) <= hit_box_vertical
                hits[1] = abs(back_t * abs(back_line.v)) <= hit_box_vertical
                hits[2] = (
                    abs(second_car_t * abs(second_car.v) - t * abs(second_car.v))
                    <= hit_box_horizontal
                )

                hits_n += sum(hits)
                if sum(hits):
                    not_detect_last = 0
                    for i, h in enumerate(hits):
                        if h and distances[i] < measurements[sensor]:
                            measurements[sensor] = distances[i]
                            break
                else:
                    if not_detect_last > 3:
                        break

                    else:
                        not_detect_last += 1

            data.update(
                {
                    f"{t}x{i}": [round(measurement, 2)]
                    for i, measurement in enumerate(measurements)
                }
            )

        second_car_normal = get_normal_2D(second_car)

        # calculate top and bottom line of car
        border_line_vector = vector_to_len(second_car_normal.v, hit_box_vertical)

        top_second_car = second_car
        top_second_car.a = top_second_car.a + border_line_vector

        bottom_second_car = second_car
        bottom_second_car.a = bottom_second_car.a - border_line_vector

        first_car_normal = get_normal_2D(first_car)
        border_line_vector_first = vector_to_len(first_car_normal.v, hit_box_vertical)

        top_first_car = first_car
        top_first_car.a = top_first_car.a + border_line_vector_first

        bottom_first_car = first_car
        bottom_first_car.a = bottom_first_car.a - border_line_vector_first

        collision = False

        try:
            for second_line in [second_car, top_second_car, bottom_second_car]:
                for first_line in [first_car, top_first_car, bottom_first_car]:
                    t_first, t_second = intersect_2D(first_line, second_line)

                    t_half_first = hit_box_horizontal / abs(first_line.v)
                    t_half_second = hit_box_horizontal / abs(second_line.v)
                    collision = max(
                        t_first - t_half_first, t_second - t_half_second
                        ) <= min(t_first + t_half_first, t_second + t_half_second)

                    if collision:
                        break

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
