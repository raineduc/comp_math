from ..functions.function import Function
from ..functions.polynomial import Polynomial
from ..derivation.polynomial_diff import differentiate
from ..common_typings import Interval

def solve(function: Function, interval: Interval, precision: float) -> float:
    if (function(interval.left) * function(interval.right) >= 0):
        raise Exception("Интервал должен удовлетворять условию f(a)*f(b) < 0")
    return _common_method(function, interval, precision, interval.right)

def solve_polynomial(function: Polynomial, interval: Interval, precision: float) -> float:
    left, right = interval

    if (function(left) * function(right) >= 0):
        raise Exception("Интервал должен удовлетворять условию f(a)*f(b) < 0")

    derivative = differentiate(function)
    second_derivative = differentiate(derivative)

    # вторая производная линейная или константа, тогда при f''(a)*f''(b) > 0
    # она сохраняет знак 
    if (function.degree < 4 and second_derivative(left) * second_derivative(right) > 0):
        if (function(left) * second_derivative(left) > 0):
            return _fast_method_fixed_left(function, interval, precision, right)
        elif (function(right) * second_derivative(right) > 0):
            return _fast_method_fixed_right(function, interval, precision, left)
    return _common_method(function, interval, precision, interval.right)    

def _common_method(function: Function, interval: Interval, precision: float, previous_point: float) -> float:
    next_point = _calc_next_point(function, interval)
    if (abs(next_point - previous_point) <= precision):
        return next_point
    next_interval = _define_next_interval(function, interval, next_point)    
    return _common_method(function, next_interval, precision, next_point)    

def _fast_method_fixed_left(function: Function, interval: Interval, precision: float, previous_point: float) -> float:
    left, _ = interval
    point_func_value, left_func_value = function(previous_point), function(left)
    next_point = previous_point - (left - previous_point) * point_func_value / (left_func_value - point_func_value)  
    if (abs(next_point - previous_point) <= precision):
        return next_point     
    next_interval = Interval(left, next_point)
    return _fast_method_fixed_left(function, next_interval, precision, next_point)

def _fast_method_fixed_right(function: Function, interval: Interval, precision: float, previous_point: float) -> float:
    _, right = interval
    point_func_value, right_func_value = function(previous_point), function(right)
    next_point = previous_point - (right - previous_point) * point_func_value / (right_func_value - point_func_value)
    if (abs(next_point - previous_point) <= precision):
        return next_point     
    next_interval = Interval(next_point, right)
    return _fast_method_fixed_right(function, next_interval, precision, next_point)

def _calc_next_point(function: Function, interval: Interval) -> float:
    left, right = interval
    left_func_value, right_func_value = function(left), function(right)
    return (left * right_func_value - right * left_func_value) / (right_func_value - left_func_value)

def _define_next_interval(function: Function, current_interval: Interval, point: float) -> Interval:
    left, right = current_interval
    if (function(left) * function(point) < 0):
        return Interval(left, point)
    return Interval(point, right)    


