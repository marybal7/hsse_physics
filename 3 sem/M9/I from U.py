import matplotlib.pyplot as plt
from M9 import *

plt.figure(figsize=(12, 10))

# График зависимости тока от U
plt.plot(U, currents, label="I from U", marker="o", color="gold", markersize=4)
plt.plot(x_values, analytical_I, label="I = k * U^(3/2)", color="rebeccapurple", alpha=0.5)
plt.xlabel("U (В)")
plt.ylabel("I (А)")
plt.title("Зависимость I от U")
plt.grid()
plt.legend()

plt.show()
