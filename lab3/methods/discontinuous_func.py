from typing import Callable
from libs.function import Function, DiscontinuousFunction, Interval

IntegrateMethod = Callable[[Function, Interval, int], float]


def support_discontinuous(method: IntegrateMethod) -> IntegrateMethod:
    def wrapper(func: Function, interval, partition_count) -> float:
        if isinstance(func, DiscontinuousFunction):
            intervals = func.extract_intervals_of_continuity(interval)
            result = 0
            for i in intervals:
                result += method(func, i, partition_count)
            return result
        return method(func, interval, partition_count)
    return wrapper


