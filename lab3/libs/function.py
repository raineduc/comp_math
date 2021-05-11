from typing import Callable, NamedTuple

dx = 1e-3

RealCallable = Callable[[float], float]


class Interval(NamedTuple):
    left: float
    right: float


class Function:
    def __init__(self, func: RealCallable):
        self.func = func

    def __call__(self, x: float) -> float:
        return self.func(x)


class DiscontinuousFunction(Function):
    def __init__(self, func: RealCallable, singularities: list[float]):
        super().__init__(func)
        self.func = func
        self.singularities = sorted(singularities)

    def extract_intervals_of_continuity(self, interval: Interval) -> list[Interval]:
        result = []
        new_left, new_right = interval  # границы нового интервала
        left, right = interval
        for s in self.singularities:
            if s == left:
                new_left = new_left + dx
            elif s == right:
                new_right = right - dx
            if left < s < right:
                result.append(Interval(new_left, s - dx))
                new_left = s + dx
        result.append(Interval(new_left, new_right))
        return result
