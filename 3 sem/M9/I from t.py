import matplotlib.pyplot as plt
from M9 import *

plt.figure(figsize=(12, 10))

# График тока в зависимости от эксперимента
plt.plot(range(len(currents)), currents, color="c")
plt.scatter(range(len(currents)), currents, [11]*len(currents), label="I(t)", color="c")
plt.xlabel("Эксперимент (t)")
plt.ylabel("I (А)")
plt.title("Зависимость I от t")
plt.grid()
plt.legend()

plt.show()
