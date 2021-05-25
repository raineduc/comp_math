from math import comb, factorial
from lab_types import Function


def build_first_polynomial(starting_point: float, step: float, func_values: list[float]) -> Function:
    points_count = len(func_values)
    finite_diffs = [_calc_finite_difference(func_values, i) for i in range(points_count)]

    def newton_polynomial(arg: float) -> float:
        t_param = (arg - starting_point) / step
        result = 0
        for i in range(points_count):
            gen_degree = _calc_generalized_degree(t_param, i)  # t(t - 1)...(t - (i-1))
            result += gen_degree * finite_diffs[i] / factorial(i)
        return result

    return newton_polynomial


def build_second_polynomial(starting_point: float, step: float, func_values: list[float]):
    points_count = len(func_values)
    finite_diffs = [_calc_finite_difference(func_values[i:], points_count - i - 1) for i in range(points_count)]

    def newton_polynomial(arg: float) -> float:
        t_param = (arg - (starting_point + step * (points_count - 1))) / step
        result = 0
        for i in range(points_count - 1, -1, -1):
            gen_degree = _calc_generalized_degree(t_param + i - 1, i)
            result += gen_degree * finite_diffs[points_count - i - 1] / factorial(i)
        return result

    return newton_polynomial


def _calc_finite_difference(values: list[float], order: int) -> float:
    result = 0
    for i in range(0, order + 1):
        result += ((-1) ** i) * comb(order, i) * values[order - i]
    return result


def _calc_generalized_degree(val: float, degree: int) -> float:
    result = 1
    for i in range(degree):
        result *= (val - i)
    return result
