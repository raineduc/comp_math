from typing import Callable, NamedTuple

Function = Callable[[float, float], float]


class Point(NamedTuple):
    x: float
    y: float


class Interval(NamedTuple):
    left: float
    right: float

