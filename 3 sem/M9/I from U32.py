import matplotlib.pyplot as plt
from M9 import *

plt.figure(figsize=(12, 10))

# График I в зависимости от U^(3/2)
plt.plot(U32, currents, label="I from U^(3/2)", color="tan", marker="o", markersize=4)
plt.plot(U32_values, analytical_I_U32, label="Прямая I = k * U^(3/2)", color="y", alpha=0.5)
plt.xlabel("U^(3/2) (В^(3/2))")
plt.ylabel("I (А)")
plt.title("Зависимость I от U^3/2")
plt.grid()
plt.legend()

plt.show()
