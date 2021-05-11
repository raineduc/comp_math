from typing import Optional
from math import exp, log
from lab_types import Point, ApproximationResult
from metrics import calc_deviation_measure, calc_standard_deviation


def calc_power_least_squares(points: list[Point]) -> Optional[ApproximationResult]:
    sx = sxx = sy = sxy = 0
    number_of_points = len(points)

    # X = ln(x)
    # Y = ln(y)
    for point in points:
        if point.x <= 0:
            return None
        sx += log(point.x)
        sxx += log(point.x) ** 2
        sy += point.y
        sxy += log(point.x) * point.y

    determinant = sxx * number_of_points - sx * sx
    if determinant == 0:
        return None

    a = (sxy * number_of_points - sx * sy) / determinant
    b = (sxx * sy - sx * sxy) / determinant

    a1 = exp(a)  # a = ln(a1)
    b1 = b

    def func(x):
        return a1 * x ** b1

    func_text = '{:.3f} * x^{:.3f}'.format(a1, b1)

    measure = calc_deviation_measure(func, points)
    standard_deviation = calc_standard_deviation(func, points)

    return ApproximationResult(func, [a1, b1], points, measure, standard_deviation, func_text=func_text,
                               description='Степенная аппроксимация')
