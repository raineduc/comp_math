from typing import Optional
from math import exp, log
from lab_types import Point, ApproximationResult
from metrics import calc_deviation_measure, calc_standard_deviation


def calc_exponential_least_squares(points: list[Point]) -> Optional[ApproximationResult]:
    sx = sxx = sy = sxy = 0
    number_of_points = len(points)

    for point in points:
        sx += point.x
        sxx += point.x ** 2
        if point.y <= 0:
            return None
        sy += log(point.y)
        sxy += point.x * log(point.y)

    determinant = sxx * number_of_points - sx * sx
    if determinant == 0:
        return None

    b = (sxy * number_of_points - sx * sy) / determinant
    a = (sxx * sy - sx * sxy) / determinant

    a1 = exp(a)  # a = ln(a1)
    b1 = b

    def func(x):
        return a1 * exp(b1 * x)

    func_text = '{:.3f} * e^({:.3f} * x)'.format(a1, b1)

    measure = calc_deviation_measure(func, points)
    standard_deviation = calc_standard_deviation(func, points)

    return ApproximationResult(func, [a1, b1], points, measure, standard_deviation, func_text=func_text,
                               description='Экспоненциальная аппроксимация')
