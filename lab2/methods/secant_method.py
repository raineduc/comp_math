from ..functions.function import Function
from ..common_typings import Interval
from ..derivation.approximal_diff import calc_higher_order_derivative

def solve(function: Function, interval: Interval, precision: float) -> float:
    if (function(interval.left) * function(interval.right) >= 0):
        raise Exception("Интервал должен удовлетворять условию f(a)*f(b) < 0")

    left, right = interval    
    x0 = x1 = None
    if function(left) * calc_higher_order_derivative(function, left, 2) > 0:
        x0, x1 = left, right
    else:
        x0, x1 = right, left
    return _calc_approximate_point(function, precision, x0, x1)    

def _calc_approximate_point(function: Function, precision: float, x0: float, x1: float) -> float:
    x = x1 - (x1 - x0) * function(x1) / (function(x1) - function(x0))
    if (abs(x - x1) <= precision):
        return x
    return _calc_approximate_point(function, precision, x1, x)    
