from matplotlib import pyplot as plt
from scipy import stats
import csv

_MU_COL=6
_TH_COL=4

_CU_N_START=3
_CU_N_END=21

_CU_G_START=22
_CU_G_END=40

_AL_N_START=41
_AL_N_END=83

_AL_G_START=84
_AL_G_END=126

_PB_N_START=127
_PB_N_END=157

_PB_G_START=158
_PB_G_END=188

_FILE = 'book3.csv'
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

mu=getReadings(_CU_N_START, _CU_N_END, _MU_COL)
thickness=getReadings(_CU_N_START, _CU_N_END, _TH_COL)

slope, intercept, r_value, p_value, std_err = stats.linregress(thickness,mu)
line = [slope*i + intercept for i in thickness]
plt.plot(thickness, mu, 'ro', label="Cu, ignoring background")
plt.plot(thickness, line, 'r')

mu=getReadings(_CU_G_START, _CU_G_END, _MU_COL)
thickness=getReadings(_CU_G_START, _CU_G_END, _TH_COL)
slope, intercept, r_value, p_value, std_err = stats.linregress(thickness,mu)
line = [slope*i + intercept for i in thickness]
#plt.plot(thickness, mu, 'mo', thickness, line, 'm', label="Cu, including background")
plt.plot(thickness, mu, 'mo', label="Cu, including background")
plt.plot(thickness, line, 'm')

mu=getReadings(_AL_N_START, _AL_N_END, _MU_COL)
thickness=getReadings(_AL_N_START, _AL_N_END, _TH_COL)
slope, intercept, r_value, p_value, std_err = stats.linregress(thickness,mu)
line = [slope*i + intercept for i in thickness]
#plt.plot(thickness, mu, 'bo', thickness, line, 'b', label="Al, ignoring background")
plt.plot(thickness, mu, 'bo', label="Al, ignoring background")
plt.plot(thickness, line, 'b')

mu=getReadings(_AL_G_START, _AL_G_END, _MU_COL)
thickness=getReadings(_AL_G_START, _AL_G_END, _TH_COL)
slope, intercept, r_value, p_value, std_err = stats.linregress(thickness,mu)
line = [slope*i + intercept for i in thickness]
#plt.plot(thickness, mu, 'co', thickness, line, 'c', label="Al, including background")
plt.plot(thickness, mu, 'co', label="Al, including background")
plt.plot(thickness, line, 'c')

mu=getReadings(_PB_N_START, _PB_N_END, _MU_COL)
thickness=getReadings(_PB_N_START, _PB_N_END, _TH_COL)
slope, intercept, r_value, p_value, std_err = stats.linregress(thickness,mu)
line = [slope*i + intercept for i in thickness]
#plt.plot(thickness, mu, 'yo', thickness, line, 'y', label="Pb, ignoring background")
plt.plot(thickness, mu, 'yo', label="Pb, ignoring background")
plt.plot(thickness, line, 'y')

mu=getReadings(_PB_G_START, _PB_G_END, _MU_COL)
thickness=getReadings(_PB_G_START, _PB_G_END, _TH_COL)
slope, intercept, r_value, p_value, std_err = stats.linregress(thickness,mu)
line = [slope*i + intercept for i in thickness]
#plt.plot(thickness, mu, 'go', thickness, line, 'g', label="Pb, ignoring background")
plt.plot(thickness, mu, 'go', label="Pb, including background")
plt.plot(thickness, line, 'g')

plt.title("coefficient decreases with thickness")
plt.legend()
plt.xlabel("thickness(cm)")
plt.ylabel(r"coefficient ($cm^2/g$)")
#plt.show()
plt.savefig('mu_vs_thickness_lines.png')
