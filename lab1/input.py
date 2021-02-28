from eq_system import ExtendedMatrix
from io import TextIOBase
from sys import stdin


class InputMatrixException(Exception):
    Exception

class EmptyMatrixError(InputMatrixException):
    pass

class InvalidExtendedMatrix(InputMatrixException):
    pass

def read_matrix_from_text_stream(stream: TextIOBase) -> ExtendedMatrix:
    matrix = []
    first_line = stream.readline()
    values = list(map(lambda x: float(x), first_line.split()))
    if len(values) == 0 :
        raise EmptyMatrixError('Input should not be empty')
    row_len = len(values)
    remaining_rows = row_len - 2
    matrix.append(values)
    for _ in range(remaining_rows):
        line = stream.readline()
        values = list(map(lambda x: float(x), line.split()))
        if len(values) != row_len:
            raise InvalidExtendedMatrix("Extended matrix must have n+1 columns and n rows")
        matrix.append(values)  
    return matrix

def read_matrix_from_file(filename: str) -> ExtendedMatrix:
    with open(filename, 'r') as file:
        matrix = read_matrix_from_text_stream(file)
        last_line = file.readline()
        if last_line:
            raise InvalidExtendedMatrix("Extended matrix must have n+1 columns and n rows")
        return matrix     

def read_matrix_from_stdin() -> ExtendedMatrix:
    return read_matrix_from_text_stream(stdin)