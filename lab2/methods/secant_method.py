from functions.function import Function
from common_typings import Interval
from derivation.approximal_diff import calc_higher_order_derivative
from .solution import Solution, SecantIterationData, IllegalConditionException

def solve(function: Function, interval: Interval, precision: float) -> tuple[Solution, list[SecantIterationData]]:
    if (function(interval.left) * function(interval.right) >= 0):
        raise IllegalConditionException("Интервал должен удовлетворять условию f(a)*f(b) < 0")

    left, right = interval    
    x0 = x1 = None
    if function(left) * calc_higher_order_derivative(function, left, 2) > 0:
        x0, x1 = left, left + 0.01
    else:
        x0, x1 = right, right - 0.01
    return _calc_approximate_point(function, precision, x0, x1)    

def _calc_approximate_point(function: Function, precision: float, x0: float, x1: float, 
iteration: int = 1, iterations_data: list[SecantIterationData] = []) -> tuple[Solution, list[SecantIterationData]]:
    x = x1 - (x1 - x0) * function(x1) / (function(x1) - function(x0))
    iterations_data.append(SecantIterationData(x, x1, x0, iteration)) 
    if (abs(x - x1) <= precision and iteration > 2):
        return Solution(x, function(x), iteration), iterations_data
    return _calc_approximate_point(function, precision, x1, x, iteration + 1)    
