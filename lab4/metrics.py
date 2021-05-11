from functools import reduce
from math import sqrt
from typing import Callable
from lab_types import Point

Function = Callable[[float], float]


def calc_deviation_measure(func: Function, points: list[Point]) -> float:
    result = 0
    for point in points:
        result += (func(point.x) - point.y) ** 2
    return result


def calc_standard_deviation(func: Function, points: list[Point]) -> float:
    measure = calc_deviation_measure(func, points)
    return sqrt(measure / len(points))


def calc_pearson_coefficient(points: list[Point]) -> float:
    number_of_points = len(points)
    x_average = reduce(lambda acc, point: acc + point.x, points, 0) / number_of_points
    y_average = reduce(lambda acc, point: acc + point.y, points, 0) / number_of_points

    sx2 = sy2 = sxy = 0

    for x, y in points:
        sxy += (x - x_average) * (y - y_average)
        sx2 += (x - x_average) ** 2
        sy2 += (y - y_average) ** 2

    return sxy / (sqrt(sx2 * sy2))

