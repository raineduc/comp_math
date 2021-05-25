from lab_types import Function, Point


def build_lagrange_polynomial(points: list[Point]) -> Function:
    coefficients = []
    nodal_functions = []

    for i, point in enumerate(points):
        denominator = 1

        for index, p in enumerate(points):
            denominator *= (point.x - p.x) if index != i else 1

        def monomial(variable, closure_index=i) -> float:
            result = 1
            for index, p in enumerate(points):
                result *= (variable - p.x) if index != closure_index else 1
            return result

        nodal_functions.append(monomial)
        coefficients.append(point.y / denominator)

    def lagrange_polynomial(val: float) -> float:
        point_indices = range(len(points))
        return sum(map(lambda i: coefficients[i] * nodal_functions[i](val), point_indices))

    return lagrange_polynomial
