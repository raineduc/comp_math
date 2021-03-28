from methods.solution import IterationData, SecantIterationData, IterativeMethodIterationData
from functions.function import Function
 
def create_chord_method_row(function: Function, iter_data: IterationData) -> tuple[int, str, str, str, str, str, str, str]:
    left, right = iter_data.interval
    f_a = _format(function(left))
    f_b = _format(function(right))
    f_x = _format(function(iter_data.point))
    interval_delta = _format(abs(right - left))
    return iter_data.iteration, _format(left), _format(right), _format(iter_data.point), f_a, f_b, f_x, interval_delta

def create_secant_method_row(function: Function, iter_data: SecantIterationData) -> tuple[int, str, str, str, str, str, str, str]:
    x, x_n1, x_n2, iteration = iter_data
    f_x_n2 = _format(function(x_n1))
    f_x_n1 = _format(function(x_n2))
    f_x = _format(function(x))
    delta = _format(abs(x_n1 - x))
    return iteration, _format(x_n2), f_x_n2, _format(x_n1), f_x_n1, _format(x), f_x, delta

def create_iterative_method_row(function: Function, iter_data: IterativeMethodIterationData) -> tuple[int, float, float, float, float]:
    x, previous_x, iteration = iter_data
    f_previous_x = _format(function(previous_x))
    delta = _format(abs(previous_x - x))
    return iteration, _format(previous_x), f_previous_x, _format(x), delta

def _format(num: float) -> str:
    return "{:.3f}".format(num)    

