from typing import NamedTuple
from common_typings import Interval

class IllegalConditionException(Exception):
    pass

class Solution(NamedTuple):
    point: float
    value: float
    iterations_count: int

class IterationData(NamedTuple):
    interval: Interval
    point: float
    iteration: int

class SecantIterationData(NamedTuple):
    x: float
    x_n1: float
    x_n2: float
    iteration: int

class IterativeMethodIterationData(NamedTuple):
    x: float
    previous_x: float 
    iteration: int  

