from array import array
from copy import deepcopy
from itertools import product
from enum import Enum

class Decision(Enum):
    SINGLE = 1
    INFINITY = 2
    NONE = 3

ExtendedMatrix = list[list[float]]
    

def solve_sle(matrix: ExtendedMatrix) -> tuple[Decision, list[float], list[float]]:
    new_matrix = deepcopy(matrix)
    new_order, changes = to_triangular_matrix(new_matrix)
    if (calc_determinant(new_matrix) == 0):
        return _find_zero_determinant_decision(new_matrix), [], []
    vars = _calc_variables(new_matrix)    
    vars_with_order = [var[1] for var in sorted(zip(new_order, vars))]
    deviations = _calc_deviations(matrix, vars_with_order)
    return Decision.SINGLE, vars_with_order, deviations

def calc_determinant(matrix: ExtendedMatrix) -> float:
    new_matrix = deepcopy(matrix)
    new_order, changes = to_triangular_matrix(new_matrix)
    result = (-1)**changes
    for index in range(len(new_matrix)):
        result *= new_matrix[index][index]
    return result    

def to_triangular_matrix(matrix: ExtendedMatrix) -> tuple[list[int], int]:
    row_len = len(matrix)
    col_changes_count = 0
    new_var_order = [i for i in range(row_len)]
    for row in range(row_len):
        _change_to_non_empty_row(matrix, row)
        max_main = abs(matrix[row][row])
        max_matrix_col = row
        for col in range(row, row_len):
            if abs(matrix[row][col]) > max_main:
                max_main = matrix[row][col]
                max_matrix_col = col

        if max_main == 0:
            continue
        if max_matrix_col != row:
            _change_columns(matrix, row, max_matrix_col)
            new_var_order[row], new_var_order[max_matrix_col] = new_var_order[max_matrix_col], new_var_order[row]
            col_changes_count += 1
            .0
        _exclude_var(matrix, row)
    return new_var_order, col_changes_count

def _change_to_non_empty_row(matrix: ExtendedMatrix, row: int):
    for i in range(row, len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != 0:
                matrix[i], matrix[row] = matrix[row], matrix[i]
                return


def _calc_deviations(matrix: ExtendedMatrix, vars: list[float]) -> list[float]:
    deviations = []
    right_part_index = len(matrix)
    for row in matrix:
        sum = 0
        for index, var in enumerate(vars):
            sum += var * row[index]
        deviations.append(sum - row[right_part_index])
    return deviations        

def _calc_variables(matrix: ExtendedMatrix) -> list[float]:
    row_len = len(matrix)
    col_len = row_len + 1
    vars = []
    for row in range(row_len - 1, -1, -1):
        right_part = matrix[row][col_len - 1]
        for var_index, known_var in enumerate(vars):
            right_part -= known_var * matrix[row][row_len - 1 - var_index]
        
        new_var = right_part / matrix[row][row]
        vars.append(new_var)
    vars.reverse()    
    return vars

def _find_zero_determinant_decision(matrix: ExtendedMatrix) -> Decision:
    row_len = len(matrix)
    for i in range(row_len):
        if matrix[i][i] == 0 and matrix[i][row_len] != 0:
            return Decision.NONE
    return Decision.INFINITY        

def _exclude_var(matrix: ExtendedMatrix, var_index: int):
    row_len = len(matrix)
    col_len = row_len + 1
    if var_index < row_len - 1:
        for row in range(var_index + 1, row_len):
            coef = - matrix[row][var_index] / matrix[var_index][var_index]
            for col in range(var_index, col_len):
                if col == var_index:
                    matrix[row][col] = 0
                    continue
                matrix[row][col] += coef * matrix[var_index][col]  
    return            

def _change_columns(matrix: ExtendedMatrix, col1: int, col2: int):
    r_len = len(matrix)
    for r in range(r_len):
        matrix[r][col1], matrix[r][col2] = matrix[r][col2], matrix[r][col1]
    return
