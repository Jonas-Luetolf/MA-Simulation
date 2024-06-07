from src.car import get_random_car
from src.sensors import get_sensor_lines

from src.vectorlib.vector import Vector, angel
from src.vectorlib.line import Line, intersect_2D


def main(
    min_x: int,
    max_x: int,
    min_y: int,
    max_y: int,
    v_max: int,
    num_sampeles: int,
    sensor_time: float,
    save_path: str,
    num_sensor_measurements: int = 3,
    negative_probability: int = 25,
    first_car_speed: int = 10,
    hit_box: int = 5,
):
    sensors = get_sensor_lines(3, 90, 0, 0)

    for _ in range(num_sampeles):
        first_car = Line(Vector((0, 0)), Vector((0, first_car_speed)))

        second_car = get_random_car(
            min_x, max_x, min_y, max_y, v_max, v_max, negative_probability
        )

        for t in [sensor_time * n for n in range(num_sensor_measurements)]:
            pos_angel = angel(Vector((1, 0)), second_car.getPoint(t))

            start_sensor = int(pos_angel // 3)
            curr_sensor = start_sensor
            measurements = [float("inf")] * (90 // 3)
            while curr_sensor > 0:
                sensor_t, car_t = intersect_2D(sensors[curr_sensor], second_car)

                if abs(car_t * abs(second_car.v) - t * abs(second_car.v)) <= hit_box:
                    measurements[curr_sensor] = sensor_t
                else:
                    break

            while curr_sensor < (90 // 3) - 1:
                sensor_t, car_t = intersect_2D(sensors[curr_sensor], second_car)

                if abs(car_t * abs(second_car.v) - t * abs(second_car.v)) <= hit_box:
                    measurements[curr_sensor] = sensor_t
                else:
                    break

            # TODO: save measurements

        t_first, t_second = intersect_2D(first_car, second_car)
        t_half_first = hit_box / abs(first_car.v)
        t_half_second = hit_box / abs(second_car.v)
        collision = max(t_first - t_half_first, t_second - t_half_second) <= min(
            t_first + t_half_first, t_second + t_half_second
        )

        # TODO: save all measurements and collision
