from typing import Optional
from lab_types import Point, ApproximationResult
from eq_system import solve_sle, Decision
from metrics import calc_deviation_measure, calc_standard_deviation


def calc_quadratic_least_squares(points: list[Point]) -> Optional[ApproximationResult]:
    sx = sy = sx2 = sx3 = sx4 = sxy = sx2y = 0
    number_of_points = len(points)

    for x, y in points:
        sx += x
        sx2 += x ** 2
        sx3 += x ** 3
        sx4 += x ** 4
        sy += y
        sxy += x * y
        sx2y += x ** 2 * y

    matrix = [
        [number_of_points, sx, sx2, sy],
        [sx, sx2, sx3, sxy],
        [sx2, sx3, sx4, sx2y]
    ]

    decision_count, decisions, _ = solve_sle(matrix)
    if decision_count != Decision.SINGLE:
        return None
    a0, a1, a2 = decisions

    def func(arg):
        return a0 + a1 * arg + a2 * arg ** 2
    func_text = '{:3f} + {:.3f} * x + {:.3f} * x^2'.format(a0, a1, a2)

    measure = calc_deviation_measure(func, points)
    standard_deviation = calc_standard_deviation(func, points)

    return ApproximationResult(func, [a0, a1, a2], points, measure, standard_deviation, func_text=func_text, description='Квадратичная аппроксимация')
