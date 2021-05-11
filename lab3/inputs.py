from typing import TextIO
from libs.function import Interval


def read_interval(stream: TextIO) -> Interval:
    left, right = map(float, stream.readline().split())
    return Interval(left, right)


def read_number(stream: TextIO) -> int:
    return int(stream.readline().strip())


def read_float(stream: TextIO) -> float:
    return float(stream.readline().strip())
