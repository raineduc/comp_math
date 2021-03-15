from .function import Function

class Polynomial(Function):
    coefficients = []
    degree = 0
    def __init__(self, coefficients: list[float]):
        self.coefficients = coefficients if len(coefficients) > 0 else [0]
        self.degree = len(coefficients) - 1 if len(coefficients) > 0 else 0
    def __call__(self, x: float) -> float:
        sum = 0
        for i in range(self.degree, -1, -1):
            sum += self.coefficients[self.degree - i] * x**i
        return sum 