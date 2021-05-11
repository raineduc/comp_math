import argparse
from sys import stdin
from metrics import calc_pearson_coefficient
from lab_types import Point, ApproximationResult
from methods.exponential import calc_exponential_least_squares
from lab_io import show_approximations, show_approximation_table, read_points, draw
from methods.linear import calc_linear_least_squares
from methods.logarithmic import calc_logarithmic_least_squares
from methods.power import calc_power_least_squares
from methods.quadratic import calc_quadratic_least_squares

error_messages = [
    'Экспоненциальная аппроксимация невозможна',
    'Линейная аппроксимация невозможна',
    'Логарифмическая аппроксимация невозможна',
    'Степенная аппроксимация невозможна',
    'Квадратичная аппроксимация невозможна'
]
methods = [calc_exponential_least_squares, calc_linear_least_squares,
           calc_logarithmic_least_squares, calc_power_least_squares,
           calc_quadratic_least_squares]


def calc_approximations(points: list[Point]) -> list[ApproximationResult]:
    results = []
    for i, method in enumerate(methods):
        result = method(points)
        if result is None:
            print(error_messages[i])
            continue
        results.append(result)
    return results


arg_parser = argparse.ArgumentParser(description="Программа вычисляет аппроксимации функций")
arg_parser.add_argument('-i', '--input', help='Задает файл ввода. По умолчанию ввод осуществляется с клавиатуры')
args = arg_parser.parse_args()

if args.input:
    file = open(args.input, 'r')
    sample = read_points(file)
else:
    sample = read_points(stdin)

approximations = calc_approximations(sample)

if len(approximations) == 0:
    print('Невозможно аппроксимировать входящие данные')
else:
    pearson_coef = calc_pearson_coefficient(sample)
    print('Коэффициент корреляции Пирсона: {:.3f}'.format(pearson_coef))
    best_approx = min(approximations, key=lambda a: a.standard_deviation)
    show_approximation_table(best_approx)
    show_approximations(approximations)
    draw(approximations, sample)
