from ..functions.polynomial import Polynomial

def differentiate(function: Polynomial) -> Polynomial:
    new_coefs = []
    degree, coefficients = function.degree, function.coefficients
    for i in range(function.degree, -1, -1):
        if i == 0: break
        new_coefs.append(coefficients[degree - i] * i)
    return Polynomial(new_coefs)

def calc_derivative(function: Polynomial, point: float) -> float:
    new_polynomial = differentiate(function)
    return new_polynomial(point)

