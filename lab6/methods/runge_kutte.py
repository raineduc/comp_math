from lab_types import Function, Point, Interval

dx = 1e-6

def calc_runge_kutte_ODE(func: Function, start_point: Point, interval: Interval, step=4) -> list[Point]:
    result = [start_point]
    left, right = interval
    x, y = start_point

    while x >= interval.left and x + step <= right + dx:
        k1 = step * func(x, y)
        k2 = step * func(x + step / 2, y + k1 / 2)
        k3 = step * func(x + step / 2, y + k2 / 2)
        k4 = step * func(x + step, y + k3)
        y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x = x + step
        result.append(Point(x, y))

    return result
