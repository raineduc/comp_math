from functions.function import Function
from common_typings import Interval
from derivation.approximal_diff import calc_approximate_derivative
from .solution import Solution, IterativeMethodIterationData, IllegalConditionException

# Условия сходимости при использовании метода релаксации:
# -2 < lambda * f'(x) < 0
# При lambda = - 1/M, M = max(f'(x)) на [a, b]
# сходимость достигается при знакопостоянстве f'(x) на [a, b]
# Программно это проверяется так: при любом n |x_(n+1) - x_n| < |x_n - x_(n-1)|
# Заданная точность гарантируется при max(|1 + lambda * f'(x)|) <= 1/2
# Иначе: 1/2 <= f'(x) / M <= 3/2 <=> 1/2 <= m / M
# где m = min(f'(x)) на [a, b]
# т.е отрезок не должен содержать относительно маленькую и относительно большую
# производную одновременно
# 
# Константа M в самом методе изначально примет значение исходя из теоремы Лагранжа:
# M = f(b) - f(a) / (b - a) = f'(c) так гарантируется ненулевое значение M
# далее в случае f'(x_n) > M  M = f'(x_n)
# это справедливо, т.к не имеет значение, какое приближение на отрезке [a,b] берется
# получается новый итерационный процесс, но уже с более точным начальным приближением
# так не придется вычислять максимум производной и выполнится условие
# |1 - f'(x)/M | < 1 при знакопостоянстве f'(x)
def solve(function: Function, interval: Interval, precision: float) -> tuple[Solution, list[IterativeMethodIterationData]]:
    if (function(interval.left) * function(interval.right) >= 0):
        raise IllegalConditionException("Интервал должен удовлетворять условию f(a)*f(b) < 0")

    left, right = interval
    M_value = function(right) - function(left) / (right - left) # т. Лагранжа
    phi = _transform_equation(function, M_value)

    if (abs(calc_approximate_derivative(function, left)) > abs(M_value)):
        M_value = calc_approximate_derivative(function, left)
        phi = _transform_equation(function, M_value)
    previous_x = left    
    x = phi(previous_x)

    iterations_count = 1

    iterations = []

    iterations.append(IterativeMethodIterationData(x, previous_x, iterations_count))

    while (abs(x - previous_x) >= precision or iterations_count <= 2):
        derivate_at_point = calc_approximate_derivative(function, x)
        if (abs(derivate_at_point) > abs(M_value)):
            M_value = derivate_at_point
            phi = _transform_equation(function, M_value)
        last_approximation = abs(x - previous_x)
        previous_x = x
        x = phi(previous_x)
        if (abs(x - previous_x) >= last_approximation):
            raise IllegalConditionException("Метод итерации не сходится")
        iterations_count += 1
        iterations.append(IterativeMethodIterationData(x, previous_x, iterations_count))
    return Solution(x, function(x), iterations_count), iterations


def _transform_equation(function: Function, M: float) -> Function:
    lambda_ = - 1 / M
    return lambda x: x + lambda_ * function(x)