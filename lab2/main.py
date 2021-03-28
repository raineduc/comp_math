from math import sin, cos, exp, log2
from sys import argv, stdin
from prettytable import PrettyTable
import argparse
from methods.solution import IllegalConditionException
from functions.polynomial import Polynomial
from functions.function import Function
from methods.chord_method import solve_polynomial, solve as chord_solve
from methods.secant_method import solve as secant_solve
from methods.iterative_method import solve as solve_iterative
from common_typings import Interval
from inputs import read_method, read_interval, read_precision, read_params_from_file, write_output_to_file, read_function, loop_read_interval_from_stdin, Method
from plot import draw_plot, save_plot_in_file, show_plot
from table import create_chord_method_row, create_secant_method_row, create_iterative_method_row

INPUT_STDIN = 1
INPUT_FILE = 2
OUTPUT_STDOUT = 1
OUTPUT_FILE = 2

methods_requirements = {
    Method.CHORD: "  -- f(x) непрерывна на [a, b]\n" \
                    "  -- f(a) * f(b) < 0\n" \
                    "  -- f'(x) и f''(x) сохраняют знаки на [a, b]",
    Method.SECANT: "  -- f(x) непрерывна на [a, b]\n" \
                    "  -- f(a) * f(b) < 0\n" \
                    "  -- f'(x) и f''(x) сохраняют знаки на [a, b]" \
                    "  -- производная f'(x) != 0",
    Method.ITERATIVE: "  -- Производная f'(x) сохраняет знак на [a, b] и не равна нулю\n" \
                        "  -- Точность гарантируется в случае 1/2 <= m / M\n" \
                        "  -- где m = min(|f'(x)|) и M = max(|f'(x)|)"
}

# func = Function(lambda x: sin(3*x) + exp(2*x) + cos(-2 * x))
# func = Polynomial([-3.64, 2.12, 10.73, 1.49])
func = Function(lambda x: log2(3*x**2 + 1)*x**3 - 2*x**2 -2*sin(3*x) - 5*x + 1)
try:
    method = None
    interval = None
    precision = None
    input_mode = INPUT_STDIN
    output_mode = OUTPUT_STDOUT
    output_filename = None
    input_filename = None
    parser = argparse.ArgumentParser(description='Вычисляет решения нелинейных уравнений')

    parser.add_argument('-i', '--input', help='Задает файл ввода. По умолчанию ввод осуществляется с клавиатуры')
    parser.add_argument('-o', '--output', help='Задает файл вывода. По умолчанию вывод осуществляется в консоль')
    parser.add_argument('-v', '--verbose', action='store_true', help='Вывести ходы решения метода')
    args = parser.parse_args()
    if (args.input):
        input_mode = INPUT_FILE
        input_filename = args.input
    if (args.output):
        output_mode = OUTPUT_FILE
        output_filename = args.output    
    
    if input_mode == INPUT_FILE:
        method, interval, precision, func = read_params_from_file(input_filename)
    else:    
        print("Введите метод:\n" \
            "*  chord - метод хорд\n"
            "*  secant - метод секущих\n" \
            "*  iterative - метод простой итерации"   
        ) 
        method = read_method(stdin)
        print("Условия корректности метода:")
        print(methods_requirements[method])
        print("Выберите функцию и задайте коэффициенты:\n" \
            "*  polynomial - ax^n + bx^(n-1) + ... + c\n"
            "*  function  -  a * sin(bx) + c * cos(dx) + f * exp(gx) + h*log2(jx) + polynomial")
        func = read_function(stdin)
        print("Введите необходимую точность:")
        precision = read_precision(stdin)
        print("Введите интервал:")
        interval = read_interval(stdin)
    result = table = None
    while(True):
        try:
            draw_plot(func, interval)    
            if (method == Method.CHORD):
                if isinstance(func, Polynomial):
                    result, iterations = solve_polynomial(func, interval, precision)
                else:
                    result, iterations = chord_solve(func, interval, precision)
                table = PrettyTable(['№ шага', 'a', 'b', 'x', 'f(a)', 'f(b)', 'f(x)', '|a-b|'])
                for row in iterations:
                    table.add_row(create_chord_method_row(func, row))
            if (method == Method.SECANT):
                result, iterations = secant_solve(func, interval, precision)
                table = PrettyTable(['№ шага', 'x_{k-1}', 'f(x_{k-1})', 'x_k', 'f(x_k)', 'x_{k+1}', 'f(x_{k+1})', '|x_k-x_{k+1}|'])
                for row in iterations:
                    table.add_row(create_secant_method_row(func, row))
            if (method == Method.ITERATIVE):
                result, iterations = solve_iterative(func, interval, precision)
                table = PrettyTable(['№ шага', 'x_k', 'f(x_k)', "x_{k+1} = p'(x_k)", '|x_k-x_{k+1}|'])
                for row in iterations:
                    table.add_row(create_iterative_method_row(func, row))  
            if (output_mode == OUTPUT_FILE):
                write_output_to_file(output_filename, 
                [
                    "Найденное решение: {}".format(result.point),
                    "Значение в этой точке: {}".format(result.value),
                    "Количество итераций: {}".format(result.iterations_count),
                    table.get_string() if args.verbose else ''
                ])
                save_plot_in_file("plot.png")
            else:    
                print("Найденное решение: {}".format(result.point))
                print("Значение в этой точке: {}".format(result.value))
                print("Количество итераций: {}".format(result.iterations_count))
                if args.verbose:
                    print(table)
                show_plot()
        except IllegalConditionException as e:
            print(e)
            if (output_mode == OUTPUT_FILE):
                save_plot_in_file("plot.png")
            else:
                show_plot()
        print("Введите интервал(для выхода наберите exit):")
        interval = loop_read_interval_from_stdin(stdin)                                 
except Exception as e:
    print("Произошла ошибка:")
    print(e)