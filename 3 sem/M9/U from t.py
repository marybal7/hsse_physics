import matplotlib.pyplot as plt
from M9 import *

plt.figure(figsize=(12, 10))

# График напряжения в зависимости от эксперимента
plt.plot(range(len(currents)), U, color="springgreen")
plt.scatter(range(len(currents)), U, [11]*len(currents), label="U(t)", color="springgreen")
plt.xlabel("Эксперимент (t)")
plt.ylabel("U (В)")
plt.title("Зависимость U от t")
plt.grid()
plt.legend()

plt.show()
