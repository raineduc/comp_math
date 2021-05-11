from typing import Optional
from lab_types import Point, ApproximationResult
from metrics import calc_deviation_measure, calc_standard_deviation


def calc_linear_least_squares(points: list[Point]) -> Optional[ApproximationResult]:
    sx = sxx = sy = sxy = 0
    number_of_points = len(points)

    for point in points:
        sx += point.x
        sxx += point.x ** 2
        sy += point.y
        sxy += point.x * point.y

    determinant = sxx * number_of_points - sx * sx
    if determinant == 0:
        return None

    a = (sxy * number_of_points - sx * sy) / determinant
    b = (sxx * sy - sx * sxy) / determinant

    def func(x):
        return a * x + b

    func_text = '{:.3f} * x + {:.3f}'.format(a, b)

    measure = calc_deviation_measure(func, points)
    standard_deviation = calc_standard_deviation(func, points)

    return ApproximationResult(func, [a, b], points, measure, standard_deviation, func_text=func_text,
                               description='Линейная аппроксимация')
