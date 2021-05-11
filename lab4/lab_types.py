from typing import NamedTuple, Callable


class Point(NamedTuple):
    x: float
    y: float


class ApproximationResult(NamedTuple):
    function: Callable[[float], float]
    coefficients: list[float]
    points: list[Point]
    deviation_measure: float
    standard_deviation: float
    func_text: str = 'function'
    description: str = 'Аппроксимация'


