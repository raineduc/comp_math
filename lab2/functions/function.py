from typing import Callable

class Function:
    def __init__(self, func: Callable[[float], float]):
        self.func = func
    def __call__(self, x: float) -> float:
        return self.func(x)     