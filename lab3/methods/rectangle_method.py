from libs.function import Interval, Function
from libs.breaking_points import calculate_at_point
from .discontinuous_func import support_discontinuous


@support_discontinuous
def integrate_left(func: Function, interval: Interval, partition_count: int) -> float:
    left, right = interval
    step = (right - left) / partition_count
    x = left
    result = 0
    for _ in range(partition_count):
        result += calculate_at_point(func, x)
        x += step
    result *= step
    return result


@support_discontinuous
def integrate_right(func: Function, interval: Interval, partition_count: int) -> float:
    left, right = interval
    step = (right - left) / partition_count
    x = left + step
    result = 0

    for _ in range(partition_count):
        result += calculate_at_point(func, x)
        x += step
    result *= step
    return result


@support_discontinuous
def integrate_middle(func: Function, interval: Interval, partition_count: int) -> float:
    left, right = interval
    step = (right - left) / partition_count
    x = left + step / 2
    result = 0

    for _ in range(partition_count):
        result += calculate_at_point(func, x)
        x += step
    result *= step
    return result
