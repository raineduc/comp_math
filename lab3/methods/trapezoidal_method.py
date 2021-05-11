from libs.function import Interval, Function
from libs.breaking_points import calculate_at_point
from .discontinuous_func import support_discontinuous


@support_discontinuous
def integrate(func: Function, interval: Interval, partition_count: int) -> float:
    left, right = interval
    step = (right - left) / partition_count
    x = left + step
    result = 0
    for _ in range(partition_count - 1):
        result += calculate_at_point(func, x)
        x += step
    result = (result * 2 + calculate_at_point(func, left) + calculate_at_point(func, right)) * step / 2
    return result
