
from enum import Enum
from math import exp, log2, sin, cos
from typing import Callable, TextIO
from lab_io import TextIOBase
from sys import stdin
from common_typings import Interval
from functions.function import Function 
from functions.polynomial import Polynomial

POLYNOMIAL = 'polynomial'
FUNCTION = 'function'
FUNCTION_COEFS_LEN_MIN = 8
STOP_WORD = 'exit'

class Method(Enum):
    CHORD = 1
    SECANT = 2
    ITERATIVE = 3

class WrongMethod(Exception):
    pass

def read_params_from_file(filename: str) -> tuple[Method, Interval, float, Function]:
    with open(filename, 'r') as file:
        method = read_method(file)
        interval = read_interval(file)
        precision = read_precision(file)
        func = read_function
        return method, interval, precision, func

def write_output_to_file(filename: str, lines: list[str]):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')

def read_method(stream: TextIOBase) -> Method:
    method = stream.readline().rstrip('\n')
    if method == 'chord':
        return Method.CHORD
    if method == 'secant':
        return Method.SECANT
    if method == 'iterative':
        return Method.ITERATIVE
    raise WrongMethod("Specified method doesn't exist")

def read_interval(stream: TextIOBase) -> Interval:
    left, right = map(float, stream.readline().split())
    return Interval(left, right)

def loop_read_interval_from_stdin(stream: TextIO):  
    word = stream.readline().strip()
    if word == STOP_WORD:
        exit(0)
    left, right = map(float, word.split())
    return Interval(left, right)    
def read_precision(stream: TextIOBase) -> float:
    return float(stream.readline())

def read_function(stream: TextIOBase) -> Function:
    func_type = stream.readline().rstrip('\n')
    coefs = list(map(float, stream.readline().split()))
    if func_type == FUNCTION:
        if len(coefs) < FUNCTION_COEFS_LEN_MIN:
            raise Exception("Недостаточно коэффициентов: должно быть минимум 8")
        return create_function(coefs)
    elif func_type == POLYNOMIAL:
        return Polynomial(coefs)
    else:
        raise Exception("Указанного метода не существует") 

def create_function(coefs: list[float]) -> Callable[[float], float]:
    a, b, c, d, f, g, h, j, *rest = coefs
    print(coefs)
    rest = Polynomial(rest)

    if h == 0.0:
        return lambda x: a*sin(b*x) + c*cos(d*x) + f * exp(g * x) + rest(x)
    return lambda x: a*sin(b*x) + c*cos(d*x) + f * exp(g * x) + h * log2(j * x) + rest(x)  
