import csv
import math
import numpy as np
from scipy import optimize
from scipy import stats
from matplotlib import pyplot as plt

_FILENAME = 'long-rg6u.csv'
_INPUT = []
_MAX_LINE = -1
_IMG_NAME = 'longRg6u_peaks'

_F_COL=0
_X_COL=7

def read_file(filename=_FILENAME, startline=5, endline=_MAX_LINE):
    """General csv reading"""
    _IRAW=[]
    global _INPUT
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count >= startline and (line_count <= endline or endline==-1):
                _IRAW += [row]
    for i in range(len(_IRAW)-1):
        if (float(_IRAW[i][_X_COL])>float(_IRAW[i-1][_X_COL]) and float(_IRAW[i][_X_COL])>float(_IRAW[i+1][_X_COL])):
            _INPUT += [_IRAW[i]]


def extract_col(input, col_num):
    res=[]
    for line in input:
        # print(line[col_num])
        res+=[float(line[col_num])]
    return res

# data fitting: referred to http://scipy-lectures.org/intro/scipy/auto_examples/plot_curve_fit.html
def test_func(f, Z, F):
    return [(Z*_f)+F for _f in f] #y-mx+c where Z=m, c=F

def residual(x_data, p0, p1, y_data):
    res=[]
    for i in range(len(y_data)):
        res+=[y_data[i]-test_func(x_data, params[0], params[1])[i]]
    return res

read_file()

x_data=extract_col(_INPUT, _F_COL)
y_data=extract_col(_INPUT, _X_COL)

_fit=True
_calc_SE=False
_residual=True

if (_fit):
    params, pcov = optimize.curve_fit(test_func, 
    x_data,
    y_data,
    p0=[ 85.8792202, 9e06])
    #p0=None)

if _calc_SE:
    params=[ 85.8792202, 0.13e04]

if (_residual):
    plt.figure(figsize=(6, 4))
    # plt.scatter(x_data, y_data, label='Data')
    plt.plot(x_data, residual(x_data, params[0], params[1], y_data),
            label='Residual', color='red')
    plt.ylabel(r'Impedence($\Omega$)')
    plt.xlabel('Frequency(Hz)')
    plt.title("Resonance peak amplitudes")
    plt.legend(loc='best')
    plt.savefig("{}_{}".format(_IMG_NAME,'residual.png'))

# xx_data=[]
# dx=50
# for i in range(1, int(x_data[-1]/dx)):
#     xx_data+=[i*dx]
# print(xx_data)
plt.figure(figsize=(6, 4))
plt.scatter(x_data, y_data, label='Data')
plt.plot(x_data, test_func(x_data, params[0], params[1]),
        label='Fitted function', color='red')
plt.ylabel(r'Impedence($\Omega$)')
plt.xlabel('Frequency(Hz)')
plt.title("Resonance peak amplitudes")
plt.legend(loc='best')
plt.savefig("{}.png".format(_IMG_NAME))

print(params)
if(_fit):
    perr = np.sqrt(np.diag(pcov))
    print(perr)
else:
    (x,p) = stats.chisquare(y_data, f_exp=test_func(x_data, params[0], params[1]))
    print(x)
    print(p)
    tf=test_func(x_data, params[0], params[1])
    for i in range(len(tf)):
        # print('{}: {}-{}'.format(i, x_data[i], tf[i]))
        pass