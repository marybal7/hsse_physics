import numpy as np

f = open('file.txt', "r+")
f.truncate(0)

currents = np.linspace(10**(-6), 10**(-2), 30)  # значения тока для ускорения
for i in range(len(currents)):
    value = currents[i]
    f.write(str(value)+'\n')
f.close()
