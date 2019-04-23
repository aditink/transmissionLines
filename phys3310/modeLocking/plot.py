import csv
import math
import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt

_FILENAME = 'modelocking.csv'
_INPUT = []
_MAX_LINE = 160

_golden_mean_0 = 0.618
_golden_mean_1 = 1.618

_x_list = [0.25, 0.33]
_y_list = [0.54, 0.59]

def plot(filename='plot.jpg', xlabel = 'x', ylabel='y'):
    plt.plot(_x_list, _y_list)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.subplots_adjust(bottom=.25, left=.25)
    plt.savefig(filename)
    # plt.show()
    plt.clf()

def generate_x(_max, dx):
    """x list to evaluate functions"""
    return [i*dx for i in range(_max/dx)]

def populate_irr(_type = 1):
    """populate x_list and y_list from input matrix"""
    global _x_list, _y_list
    _x_list = []
    _y_list = []
    _w_col = 0
    _omega_col = 5
    mean = _golden_mean_0 if _type==1 else  _golden_mean_1
    for row in _INPUT:
        _x_list += [abs(float(row[_w_col]) - mean)]
        _y_list += [row[_omega_col]]
    list.reverse(_x_list)
    list.reverse(_y_list)


def read_file(filename=_FILENAME, startline=0, endline=_MAX_LINE):
    """General csv reading"""
    global _INPUT
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count >= startline and line_count <= endline:
                _INPUT += [row]

def plot_irrationals(_type=1, filename=_FILENAME):
    """Plot for comparing irrationality to omega width"""
    global _INPUT
    _INPUT = []
    startline = 115 if _type==1 else 124
    endline = 118 if _type==1 else 128
    read_file(startline=startline, endline=endline)
    populate_irr(_type)
    plot(filename, xlabel='distance from golden mean', ylabel='region of mode locking')

# plot_irrationals(1, 'irr1.jpg')
# plot_irrationals(2, 'irr2.jpg')

plot('width_of_triplets2.jpg', xlabel='width of triplets', ylabel='D')

# data fitting: referred to http://scipy-lectures.org/intro/scipy/auto_examples/plot_curve_fit.html
# def test_func(x, a, b):
#     return a * np.sin(b * x)

# params, params_covariance = optimize.curve_fit(test_func, _x_list, _y_list,
#                                                p0=[2, 2])

# test_x = generate_x(max(_x_list), 0.01)
# test_y
# _x_list+=

# print(params)
