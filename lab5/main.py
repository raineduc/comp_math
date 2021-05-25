import argparse
from numpy import linspace
from sys import stdin
from math import sin
from utils import _check_nodes_equidistant
from methods.lagrange import build_lagrange_polynomial
from methods.newton import build_first_polynomial, build_second_polynomial
from lab_io import *

FUNCTION_SELECTION = 0b001
DATA_ASSIGNMENT = 0b010
CALCULATING_VALUE = 0b100
USER_ACTIONS = [
    FUNCTION_SELECTION + DATA_ASSIGNMENT + CALCULATING_VALUE,
    DATA_ASSIGNMENT + CALCULATING_VALUE,
    CALCULATING_VALUE,
]
user_state = USER_ACTIONS[0]


functions = [
    lambda x: sin(x) ** 3
]
chosen_func = None
are_nodes_equidistant = False
step = None

arg_parser = argparse.ArgumentParser(description="Программа вычисляет аппроксимации функций")
arg_parser.add_argument('-i', '--input', help='Задает файл ввода. По умолчанию ввод осуществляется с клавиатуры')
args = arg_parser.parse_args()

sample = None
func_num = 1

while True:
    if args.input and not sample:
        file = open(args.input, 'r')
        sample = read_points(file)
        are_nodes_equidistant = _check_nodes_equidistant(sample)
        step = sample[1].x - sample[0].x if are_nodes_equidistant else None
    else:
        if user_state & FUNCTION_SELECTION:
            print("Введите цифру для выбора функции:")
            print("1) sin^3(x)")
            print("2) Табличный способ задания")
            func_num = read_number(stdin)

        if user_state & DATA_ASSIGNMENT:
            if func_num == 1:
                print("Введите интервал:")
                left, right = read_interval(stdin)
                print("Введите количество узлов (больше или равно двух):")
                points_count = read_number(stdin)
                chosen_func = functions[0]
                are_nodes_equidistant = True
                step = (right - left) / (points_count - 1)
                sample = [Point(x, chosen_func(x)) for x in linspace(left, right, points_count)]
            else:
                print("Введите узлы интерполяции:")
                sample = sorted(read_points(stdin), key=lambda p: p.x)
                are_nodes_equidistant = _check_nodes_equidistant(sample)
                step = sample[1].x - sample[0].x if are_nodes_equidistant else None

    print("Введите аргумент:")
    argument = read_float(stdin)
    lagrange_polynomial = build_lagrange_polynomial(sample)
    show_interpolation(sample, lagrange_polynomial, title='Интерполяция Лагранжа', original_func=chosen_func)
    print("Значение полинома Лагранжа в указанной точке: {:.3f}".format(lagrange_polynomial(argument)))

    if are_nodes_equidistant:
        sample_center = (sample[-1].x - sample[0].x) / 2
        values = list(map(lambda p: p.y, sample))
        if argument <= sample_center:
            newton_polynomial = build_first_polynomial(sample[0].x, step, values)
            show_interpolation(sample, newton_polynomial, title='Первая интерполяция Ньютона',
                               original_func=chosen_func)
            print("Значение первого полинома Ньютона в указанной точке: {:.3f}".format(newton_polynomial(argument)))
        else:
            newton_polynomial = build_second_polynomial(sample[0].x, step, values)
            show_interpolation(sample, newton_polynomial, title='Вторая интерполяция Ньютона',
                               original_func=chosen_func)
            print("Значение второго полинома Ньютона в указанной точке: {}".format(newton_polynomial(argument)))
    else:
        print("Для интерполяции Ньютона необходимы равноотстоящие узлы!")
    print("Выберите дальнейшее действие:")
    print(
        "1) Выбор функции\n" +
        "2) Ввод данных\n" +
        "3) Ввод аргумента\n" +
        "4) Выход"
    )
    next_action = read_number(stdin)
    if next_action < 4:
        user_state = USER_ACTIONS[next_action - 1]
        continue
    exit(0)
