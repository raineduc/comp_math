from .functions.polynomial import Polynomial
from .methods.chord_method import solve_polynomial, solve
from .methods.secant_method import solve as secant_solve
from .methods.iterative_method import solve as solve_iterative
from .common_typings import Interval

func = Polynomial([-3.64, 2.12, 10.73, 1.49])
interval = Interval(2, 2.5)
result1 = secant_solve(func, interval, 0.0001)
result2 = solve_polynomial(func, interval, 0.0001)
result3 = solve_iterative(func, interval, 0.0001)
print(result1)
print(result2)
print(result3)