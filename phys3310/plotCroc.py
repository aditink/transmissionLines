import csv
import math
import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt

_FILENAME = '1000pF-croc.csv'
_INPUT = []
_MAX_LINE = 100
_IMG_NAME = '1000pFCroc'

_F_COL=0
_X_COL=6

residuals=True

def read_file(filename=_FILENAME, startline=30, endline=_MAX_LINE):
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
def test_func(f, C, L):
    # return abs(1/(2*math.pi*f*C)-2*math.pi*f*L)
    return [abs(1/(2*math.pi*_f*C)-2*math.pi*_f*L) for _f in f]

def analyze(start, end):
    """returns params, pcov"""
    read_file(_FILENAME, start, end)
    x_data=extract_col(_INPUT, _F_COL)
    y_data=extract_col(_INPUT, _X_COL)
    params, pcov = optimize.curve_fit(test_func, 
    x_data,
    y_data,
    p0=[500e-12, 90e-9])
    perr = np.sqrt(np.diag(pcov))
    return params, perr

read_file()

x_data=extract_col(_INPUT, _F_COL)
y_data=extract_col(_INPUT, _X_COL)

params, pcov = optimize.curve_fit(test_func, 
    x_data,
    y_data,
    p0=[500e-12, 300e-9])
    #p0=None)

def residual(x_data, p0, p1, y_data):
    res=[]
    for i in range(len(y_data)):
        res+=[y_data[i]-test_func(x_data, params[0], params[1])[i]]
    return res

if residuals:
    plt.figure(figsize=(6, 4))
    plt.ylabel('residual(F)')
    plt.xlabel('Frequency(Hz)')
    plt.title('500pF capacitor fit')
    plt.plot(x_data, residual(x_data, params[0], params[1],y_data),
         label='Residuals', color='red')
    plt.legend(loc='best')
    plt.savefig("{}_residuals.png".format(_IMG_NAME))

plt.figure(figsize=(6, 4))
plt.ylabel('F')
plt.xlabel('Frequency(Hz)')
plt.title('500pF capacitor fit')
plt.scatter(x_data, y_data, label='Data')
plt.plot(x_data, test_func(x_data, params[0], params[1]),
         label='Fitted function', color='red')

plt.legend(loc='best')

plt.savefig("{}.png".format(_IMG_NAME))

# c=[]
# cerr=[]
# x=[]
# y=[]
# for start in range(2,50):
#     for end in range(170, 171):
#         params, err=analyze(start, end)
#         print(start)
#         print(params[0])
#         x+=[start]
#         y+=[params[0]]

# plt.plot(x,y)
# plt.show()

perr = np.sqrt(np.diag(pcov))
print(perr)
print("{} {}".format(params[0], perr[0]))
print("{} {}".format(params[1], perr[1]))