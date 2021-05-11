from typing import NamedTuple

class Result(NamedTuple):
    value: float
    iteration: int
    partitions: int
    precision: float

