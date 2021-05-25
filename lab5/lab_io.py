import matplotlib.pyplot as plt
import numpy as np
from typing import TextIO
from lab_types import Function, Point, Interval


def read_points(stream: TextIO) -> list[Point]:
    result = []
    line = stream.readline()
    while line and line != '\n':
        x, y = map(float, line.strip().split())
        result.append(Point(x, y))
        line = stream.readline()
    return result


def read_interval(stream: TextIO) -> Interval:
    left, right = map(float, stream.readline().split())
    return Interval(left, right)


def read_number(stream: TextIO) -> int:
    return int(stream.readline().strip())


def read_float(stream: TextIO) -> float:
    return float(stream.readline().strip())


def show_interpolation(points: list[Point], func: Function, title='Интерполяция', original_func=None):
    vectorized_func = np.vectorize(func)
    data_x = list(map(lambda point: point.x, points))
    data_y = list(map(lambda point: point.y, points))
    plt.title(title)
    plt.grid(True, which='both')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.ylim(_limit_axis(data_y, 0.5))

    x_values = np.linspace(min(data_x), max(data_x), 100)
    y_values = vectorized_func(x_values)

    plt.scatter(data_x, data_y, s=20, zorder=10, color='black')
    plt.plot(x_values, y_values, 'red', zorder=5, label='Интерполяционный многочлен')
    if original_func:
        original_values = np.vectorize(original_func)(x_values)
        plt.plot(x_values, original_values, 'blue', zorder=5, label='Изначальная функция')

    plt.legend(loc='lower center', fontsize='medium', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig('График {}.png'.format(title))
    plt.show()


def _limit_axis(data: list[float], relative_margin: float) -> tuple[float, float]:
    data_max = max(data)
    data_min = min(data)
    margin = relative_margin * (data_max - data_min)
    return data_min - margin, data_max + margin
