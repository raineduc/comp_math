import matplotlib.pyplot as plt
import numpy as np
from typing import TextIO
from prettytable import PrettyTable
from lab_types import ApproximationResult, Point

PLOT_COLORS = [
    'blue',
    'red',
    'green',
    'black',
    'orange'
]


def read_points(stream: TextIO) -> list[Point]:
    result = []
    line = stream.readline()
    while line:
        x, y = map(float, line.strip().split())
        result.append(Point(x, y))
        line = stream.readline()
    return result


def _limit_axis(data: list[float], relative_margin: float) -> tuple[float, float]:
    data_max = max(data)
    data_min = min(data)
    margin = relative_margin * (data_max - data_min)
    return data_min - margin, data_max + margin


def draw(approximations: list[ApproximationResult], points: list[Point]):
    colors = PLOT_COLORS.copy()
    data_x = list(map(lambda point: point.x, points))
    data_y = list(map(lambda point: point.y, points))
    plt.title = 'Графики полученных приближенных функций'
    plt.grid(True, which='both')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.ylim(_limit_axis(data_y, 0.5))
    plt.scatter(data_x, data_y, s=20, zorder=10)

    for i in range(len(approximations)):
        approx = approximations[i]
        x = np.linspace(min(data_x), max(data_x), 100)
        func = np.vectorize(approx.function)(x)

        plt.plot(x, func, colors.pop(), label=approx.description, zorder=5)

    # ---
    plt.legend(loc='lower center', fontsize='medium', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig('graph.png')
    plt.show()


def show_approximation_table(approx: ApproximationResult):
    cols = ["№ п.п"] + [str(i + 1) for i in range(len(approx.points))]
    x_row = ["X"]
    y_row = ["Y"]
    func_row = ["p(x) = {}".format(approx.func_text)]
    delta_row = ["E_i"]
    table = PrettyTable(cols, float_format=".4")

    for x, y in approx.points:
        x_row.append(x)
        y_row.append(y)
        func_row.append(approx.function(x))
        delta_row.append(approx.function(x) - y)

    table.add_row(x_row)
    table.add_row(y_row)
    table.add_row(func_row)
    table.add_row(delta_row)
    print(table)


def show_approximations(approx_results: list[ApproximationResult]):
    table = PrettyTable(["Вид функции", "a", "b", "c", "Мера отклонения", "Среднеквадратичное отклонение"],
                        float_format=".4")
    for approx in approx_results:
        coefs = approx.coefficients
        table.add_row([
            approx.func_text,
            coefs[0],
            coefs[1],
            '-' if len(coefs) <= 2 else coefs[2],
            approx.deviation_measure,
            approx.standard_deviation
        ])
    print(table)
