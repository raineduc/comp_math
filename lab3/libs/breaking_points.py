from math import isfinite
from .function import Function

dx = 1e-3


class UndefinedOnIntervalException(Exception):
    pass


def is_point_singularity(func: Function, x: float) -> bool:
    try:
        value = func(x)
        return not isfinite(value)
    except Exception:
        return True


def calculate_at_point(func: Function, x: float) -> float:
    if not is_point_singularity(func, x):
        return func(x)
    left, right = x - dx, x + dx

    if is_point_singularity(func, left) or is_point_singularity(func, right):
        raise UndefinedOnIntervalException
    return (func(left) + func(right)) / 2
