from matplotlib import pyplot as plt
import csv

_MU_G_COL=19
_MU_N_COL=18

_CU_START=13
_CU_END=52

_PB_START=109
_PB_END=150

_AL_START=53
_AL_END=108

_FILE = 'gamma2.csv'
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

#extract all mu_gross values for Cu
def getReadings(start, end, col):
    readings=[]
    for i in range(start, end):
        rdg = table[i][col]
        #rdg = if rdg == '' then 0 else float(rdg)
        if (rdg!=''):
            readings+=[float(rdg)]
    return readings

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

plt.xlabel("Z")
plt.ylabel(r"$\mu_N$ $(cm^2/g)$")
x=[13,29,82]
y=[0.28,0.16,0.15]
err=[0.1,0.17,0.2]
plt.errorbar(x,y,yerr=err, fmt='-o')
plt.savefig('trend.png')
#plt.show()
# print(readings)
