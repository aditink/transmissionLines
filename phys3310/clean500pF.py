import csv
import math
import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt

_FILENAME = '500pF-bindingport.csv'
_INPUT = []
_MAX_LINE = 200

_F_COL=0
_X_COL=6

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

# read_file()

# x_data=extract_col(_INPUT, _F_COL)
# y_data=extract_col(_INPUT, _X_COL)

# params, pcov = optimize.curve_fit(test_func, 
#     x_data,
#     y_data,
#     p0=[500e-12, 90e-9])
#     #p0=None)

# plt.figure(figsize=(6, 4))
# plt.scatter(x_data, y_data, label='Data')
# plt.plot(x_data, test_func(x_data, params[0], params[1]),
#          label='Fitted function')
# plt.plot(x_data, test_func(x_data, params[0], params[1]),
#          label='Fitted function')

# plt.legend(loc='best')

# plt.show()

c=[]
cerr=[]
x=[]
y=[]
y2=[]
for start in range(30,31):
    for end in range(170, 220):
        params, err=analyze(start, end)
        print(start)
        print(end)
        print(params[0])
        print(err[0])
        x+=[end]
        y+=[params[0]]
        y2+=[err[1]]

plt.plot(x,y,label="C")
plt.plot(x,y2,label=r"$\sigma$")
plt.ylabel('value of best fit C')
plt.xlabel('starting frequency point number')
plt.title('Data cleaning: Start frequency')
plt.legend()
# plt.show()
plt.savefig('500pFstartFrequency.png')
# print(params)
# perr = np.sqrt(np.diag(pcov))
# print(perr)