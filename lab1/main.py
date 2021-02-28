from eq_system import solve_sle, to_triangular_matrix, calc_determinant, ExtendedMatrix, Decision
from input import read_matrix_from_stdin, read_matrix_from_file, EmptyMatrixError, InvalidExtendedMatrix
from sys import stdin, argv

def _format_var(x: int) -> str:
    return "{:<12.3e}".format(x)     

def format_variables(vars: list[int]) -> list[str]:
    return list(map(_format_var, vars))

def _format_triangular_matrix_var(x, row_index, col_index):
    if (col_index < row_index):
        return "{:<12}".format(x)
    return "{:<12.3e}".format(x)   

def _format_triangular_matrix_row(row, row_index):
    return list(map(lambda pair: _format_triangular_matrix_var(pair[1], row_index, pair[0]), enumerate(row)))


def print_triangular_matrix(matrix: ExtendedMatrix, new_order: list[int]):
    formatted = list(map(lambda x: "x{:<11}".format(x + 1), new_order))
    print("{} b".format(' '.join(formatted)))
    for index, row in enumerate(matrix):
        print("{}".format(' '.join(_format_triangular_matrix_row(row, index))))


matrix = [
    [1, 2, 3, 4, 5],
    [9, 1, 0, 2, 1],
    [-5, 2, 10, 5, 7],
    [1, 11, 22, 33, 55]
]
try:
    if (len(argv) > 1):
        matrix = read_matrix_from_file(argv[1])
    else:
        print("Введите квадратную расширенную матрицу")
        matrix = read_matrix_from_stdin()
except EmptyMatrixError:
    print("Ввод не должен быть пустой")
    exit(1)
except InvalidExtendedMatrix:
    print("Неправильный ввод матрицы: матрица должна быть квадратной с добавлением справа столбца свободных коэффициентов")
    exit(1)
except FileNotFoundError:
    print("Файл не найден")
    exit(1)                
decision, vars, deviations = solve_sle(matrix)
determinant = calc_determinant(matrix)
print("Определитель:")
print("{:.3e}".format(determinant))
new_var_order, _ = to_triangular_matrix(matrix)
print("Треугольная матрица:")
print_triangular_matrix(matrix, new_var_order)
print("Решение:")
if decision == Decision.SINGLE:
    print("{}".format(' '.join(format_variables(vars))))
    print("Невязки:")
    print("{}".format(' '.join(format_variables(deviations))))
elif decision == Decision.INFINITY:
    print("Решений бесконечное количество")
elif decision == Decision.NONE:
    print("Решений у системы нет")        