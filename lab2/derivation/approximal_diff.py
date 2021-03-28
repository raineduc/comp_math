from functions.function import Function

dx = 1.0E-6 # конечная величина вместо бесконечно малой 

# метод двусторонней разности (остаток O(h^2) вместо O(h), h = dx)
def calc_approximate_derivative(function: Function, point: float) -> float:
    return (function(point + dx) - function(point - dx)) / (2 * dx)

def calc_higher_order_derivative(function: Function, point: float, n: int) -> float:
    if n <= 0:
        return function(point)
    value_delta = (calc_higher_order_derivative(function, point + dx, n - 1) - calc_higher_order_derivative(function, point - dx, n - 1))   
    return value_delta / (2 * dx)    
