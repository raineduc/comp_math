from math import sin, exp
from sys import stdin
from prettytable import PrettyTable
from inputs import read_number, read_interval, read_float
from libs.function import Function, DiscontinuousFunction, Interval
from methods.rectangle_method import integrate_left, integrate_right, integrate_middle
from methods.trapezoidal_method import integrate as trapezoidal_integrate
from methods.simpson_method import integrate as simpson_integrate
from methods import IntegrateMethod
from integration_result import Result

functions = [
    Function(lambda x: - x**3 - x**2 - 2 * x + 1),
    DiscontinuousFunction(lambda x: 1 / x, [0]),
    DiscontinuousFunction(lambda x: sin(x) / x, [0]),
    Function(lambda x: exp(x ** 2))
]

methods = [
    integrate_left,
    integrate_middle,
    integrate_right,
    trapezoidal_integrate,
    simpson_integrate
]

MAX_PARTITIONS = 1000000


def integrate_with_decision(func: Function, interval: Interval, precision: float, method: IntegrateMethod) -> list[Result]:
    partition_count = 8
    previous_result = None
    result = method(func, interval, partition_count)
    results = []
    i = 1
    while previous_result is None or abs(result - previous_result) >= precision:
        previous_result = result
        partition_count *= 2
        result = method(func, interval, partition_count)
        results.append(Result(result, i, partition_count, abs(result - previous_result)))
        i += 1
    return results


def show_result_table(results: list[Result]):
    table = PrettyTable(["Номер итерации", "Значение", "Количество разбиений", "Точность"])
    for i, r in enumerate(results):
        if i == 10 and len(results) > 11:
            table.add_row(["...", "...", "...", "..."])
            last = results[-1]
            table.add_row([last.iteration, last.value, last.partitions, last.precision])
            break
        table.add_row([r.iteration, r.value, r.partitions, r.precision])
    print(table)

print("Выберите функцию:\n" \
      "1) - x^3 - x^2 - 2 * x + 1 \n"
      "2) 1/x \n" \
      "3) sin(x) / x \n" \
      "4) e^(x^2)"
      )
func = functions[read_number(stdin) - 1]

print("Выберите метод:\n" \
      "1) Метод левых прямоугольников \n" \
      "2) Метод прямоугольников(средних значений) \n" \
      "3) Метод правых прямоугольников \n" \
      "4) Метод трапеций \n" \
      "5) Метод Симпсона"
      )
method = methods[read_number(stdin) - 1]

print("Введите интервал:")
interval = read_interval(stdin)

print("Введите точность:")
precision = read_float(stdin)

results = integrate_with_decision(func, interval, precision, method)

show_result_table(results)
