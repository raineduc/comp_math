from lab_types import Function, Point, Interval

dx = 1e-6

def calc_euler_ODE(func: Function, start_point: Point, interval: Interval, step=4) -> list[Point]:
    result = [start_point]
    left, right = interval
    x, y = start_point

    while x >= left and x + step <= right + dx:
        intermediate_y = y + step * func(x, y)
        y = y + step / 2 * (func(x, y) + func(x + step, intermediate_y))
        x = x + step
        result.append(Point(x, y))

    return result
