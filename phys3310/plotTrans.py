import csv
import math
import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt

_FILENAME = 'rg-6u.csv'
_INPUT = []
_MAX_LINE = -1

_F_COL=0
_X_COL=7

def read_file(filename=_FILENAME, startline=2, endline=_MAX_LINE):
    """General csv reading"""
    global _INPUT
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count >= startline and (line_count <= endline or endline==-1):
                _INPUT += [row]


def extract_col(input, col_num):
    res=[]
    for line in input:
        # print(line[col_num])
        res+=[float(line[col_num])]
    return res

# data fitting: referred to http://scipy-lectures.org/intro/scipy/auto_examples/plot_curve_fit.html
def test_func(f, Z, F):
    # return abs(1/(2*math.pi*f*C)-2*math.pi*f*L)
    return [abs(Z/(math.tan(2*math.pi*_f/F))) for _f in f]

read_file()

x_data=extract_col(_INPUT, _F_COL)
y_data=extract_col(_INPUT, _X_COL)

params, params_covariance = optimize.curve_fit(test_func, 
    x_data,
    y_data,
    p0=[1e1, 1e-9])
    #p0=None)

plt.figure(figsize=(6, 4))
plt.scatter(x_data, y_data, label='Data')
plt.plot(x_data, test_func(x_data, params[0], params[1]),
         label='Fitted function')

plt.legend(loc='best')

plt.show()

print(params)