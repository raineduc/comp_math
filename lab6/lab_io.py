import matplotlib.pyplot as plt
import numpy as np
from typing import TextIO
from prettytable import PrettyTable
from lab_types import Function, Point, Interval


def read_point(stream: TextIO) -> Point:
    line = stream.readline()
    x, y = map(float, line.strip().split())
    return Point(x, y)


def read_interval(stream: TextIO) -> Interval:
    left, right = map(float, stream.readline().split())
    return Interval(left, right)


def read_number(stream: TextIO) -> int:
    return int(stream.readline().strip())


def read_float(stream: TextIO) -> float:
    return float(stream.readline().strip())


def show_table(points: list[Point], exact_values, errors: list[float], func: Function):
    x_values = [p.x for p in points]
    y_values = [p.y for p in points]
    vector_len = len(x_values)

    func_values = [func(x_values[i], y_values[i]) for i in range(vector_len)]
    table = PrettyTable()
    table.add_column("Индекс", [i + 1 for i in range(vector_len)])
    table.add_column("x", x_values)
    table.add_column("y", y_values)
    table.add_column("f(x, y)", func_values)
    table.add_column("Точное решение", exact_values)
    table.add_column("Погрешность", errors)
    print(table)


def show_graph(points: list[Point], interval: Interval, exact_solution: Function, coef: float, title='График решения'):
    data_x = list(map(lambda point: point.x, points))
    data_y = list(map(lambda point: point.y, points))
    plt.title(title)
    plt.grid(True, which='both')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.ylim(_limit_axis(data_y, 0.5))

    x_values = np.linspace(interval.left, interval.right, 100)
    y_values = [exact_solution(coef, x) for x in x_values]

    plt.scatter(data_x, data_y, s=20, zorder=10, color='black', label='Приближенное решение')
    plt.plot(x_values, y_values, 'red', zorder=5, label='Точное решение')
    plt.legend(loc='lower center', fontsize='medium', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig('График {}.png'.format(title))
    plt.show()


def _limit_axis(data: list[float], relative_margin: float) -> tuple[float, float]:
    data_max = max(data)
    data_min = min(data)
    margin = relative_margin * (data_max - data_min)
    return data_min - margin, data_max + margin
