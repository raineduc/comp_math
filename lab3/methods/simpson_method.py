from libs.function import Interval, Function
from libs.breaking_points import calculate_at_point
from .discontinuous_func import support_discontinuous


@support_discontinuous
def integrate(func: Function, interval: Interval, partition_count: int) -> float:
    left, right = interval
    step = (right - left) / partition_count
    result = calculate_at_point(func, left) + calculate_at_point(func, right)
    odd_part = even_part = 0

    x = left + step

    for i in range(1, partition_count):
        if i % 2 == 0:
            even_part += calculate_at_point(func, x)
        else:
            odd_part += calculate_at_point(func, x)
        x += step

    result = (result + 4 * odd_part + 2 * even_part) * step / 3
    return result
