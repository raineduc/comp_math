from typing import Callable
from libs.function import Function, Interval

IntegrateMethod = Callable[[Function, Interval, int], float]

