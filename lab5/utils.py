from math import isclose
from lab_types import Point


def _check_nodes_equidistant(points: list[Point]) -> bool:
    step = points[1].x - points[0].x
    for i in range(1, len(points) - 1):
        if not isclose(points[i + 1].x - points[i].x, step):
            return False
    return True
