from matplotlib import pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
from numpy import arange,array,ones
import csv

_PEAK_COL=9
_TH_COL=7
# _START_COL=1

_CU_START=13
_CU_END=52

_PB_START=109
_PB_END=150

_AL_START=53
_AL_END=108

_FILE = 'book4.csv'
table=[]

def read_file(file = _FILE):
    global table
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            table+=[row]
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(row)
                line_count += 1
            print(f'Processed {line_count} lines.')
        return csv_reader

read_file()

def getReadingsPair(start, end, colx, coly):
    rx=[]
    ry=[]
    for i in range(start, end):
        x = table[i][colx]
        y = table[i][coly]        
        #rdg = if rdg == '' then 0 else float(rdg)
        if (x!='' and y!=''):
            rx+=[float(x)]
            ry+=[float(y)]
    return (rx, ry)

#plot the values
def plotMu(readings, caption, x='x', y='y', show=True, filename='placeholder'):
    plt.plot(readings[0::3], label="590-740kEv")
    plt.plot(readings[1::3], label="600-740kEv")
    plt.plot(readings[2::3], label="630-700kEv")
    plt.legend()
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(caption)
    plt.show() if show else plt.savefig(filename)

readings=getReadingsPair(_CU_START, _CU_END, _TH_COL, _PEAK_COL)

slope, intercept, r_value, p_value, std_err = stats.linregress(readings[0],readings[1])
line = [slope*i + intercept for i in readings[0]]

plt.plot(readings[0], readings[1], 'ro', readings[0], line, 'r', label="Cu")

readings=getReadingsPair(_AL_START, _AL_END, _TH_COL, _PEAK_COL)

slope, intercept, r_value, p_value, std_err = stats.linregress(readings[0],readings[1])
line = [slope*i + intercept for i in readings[0]]

plt.plot(readings[0], readings[1], 'go', readings[0], line, 'g', label="Al")

readings=getReadingsPair(_PB_START, _PB_END, _TH_COL, _PEAK_COL)

slope, intercept, r_value, p_value, std_err = stats.linregress(readings[0],readings[1])
line = [slope*i + intercept for i in readings[0]]

plt.plot(readings[0], readings[1], 'bo', readings[0], line, 'b', label="Pb")


plt.title("peak vs thickness")
plt.legend()
plt.xlabel("thickness(cm)")
plt.ylabel(r"peak(KeV)")
#plt.show()
plt.savefig('peak_vs_thickness.png')
