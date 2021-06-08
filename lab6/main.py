from sys import stdin
from math import exp, sin, cos
from lab_io import read_number, read_interval, read_point, read_float, show_table, show_graph
from methods.euler import calc_euler_ODE
from methods.runge_kutte import calc_runge_kutte_ODE

functions = [
    lambda x, y: y + sin(x),
    lambda x, y: x * y + 2*x,
    lambda x, y: -3 * (y ** 2) + y
]

exact_solutions = [
    lambda c, x: c * exp(x) - sin(x) / 2 - cos(x) / 2,
    lambda c, x: c * exp(x**2 / 2) - 2,
    lambda c, x: exp(x) / (c + 3*exp(x))
]

coef_calculators = [
    lambda x0, y0: (y0 + sin(x0) / 2 + cos(x0) / 2) / exp(x0),
    lambda x0, y0: (y0 + 2) / exp(x0**2 / 2),
    lambda x0, y0: (exp(x0) / y0) - 3*exp(x0)
]

print('Введите номер функции:')
print(
    "1) y' = y + sin(x)\n" +
    "2) y' = xy + 2x\n" +
    "3) y' = -3 * y^2 + y (лучше вводи 0 < y < 0.333...)"
)
func_index = read_number(stdin) - 1
func = functions[func_index]

print('Введите интервал дифференцирования:')
interval = read_interval(stdin)

print('Введите начальные условия:')
start_point = read_point(stdin)

print('Введите шаг:')
step = read_float(stdin)

euler_points = calc_euler_ODE(func, start_point, interval, step)
runge_kutte_points = calc_runge_kutte_ODE(func, start_point, interval, step)

euler_half_step_points = calc_euler_ODE(func, start_point, interval, step / 2)
runge_kutte_half_step_points = calc_runge_kutte_ODE(func, start_point, interval, step / 2)

euler_errors = []
runge_kutte_errors = []

for i in range(len(euler_half_step_points)):
    if i % 2 == 0:
        euler_errors.append(abs(euler_half_step_points[i].y - euler_points[i // 2].y) / 3)
        runge_kutte_errors.append(abs(runge_kutte_half_step_points[i].y - runge_kutte_points[i // 2].y) / 15)

coef = coef_calculators[func_index](*start_point)
exact_values = [exact_solutions[func_index](coef, p.x) for p in euler_points]

try:
    print('Таблица для метода Эйлера:')
    show_table(euler_points, exact_values, euler_errors, func)
    print('Таблица для метода Рунге-Кутты:')
    show_table(runge_kutte_points, exact_values, runge_kutte_errors, func)
    show_graph(euler_points, interval, exact_solutions[func_index], coef, title='Метод Эйлера')
    show_graph(runge_kutte_points, interval, exact_solutions[func_index], coef, title='Метод Рунге-Кутта')
except ValueError:
    print('Начальная точка не принадлежит решению')
