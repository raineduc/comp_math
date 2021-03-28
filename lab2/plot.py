from matplotlib import pyplot
import numpy
from functions.function import Function
from common_typings import Interval

def draw_plot(function: Function, interval: Interval):
    left, right = interval
    x = numpy.linspace(left - 1, right + 1, 10000)
    fig, ax = pyplot.subplots()
    ax.plot(x, numpy.vectorize(function)(x), label='Заданная функция')
    ax.plot([left - 1, right + 1], [0, 0], label='y=0')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("График заданной функции")   
    pyplot.legend(loc="upper left")

def save_plot_in_file(filename: str):
    pyplot.savefig(filename)

def show_plot():
    pyplot.show()