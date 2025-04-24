import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

H = 0.01  # расстояние между пластинами, м
S = 0.0001  # площадь пластин, м^2
N = 40  # число слоёв
h = H / N  # толщина слоя
e = 1.6e-19  # заряд электрона, Кл
m = 9.1e-31  # масса электрона, кг
e_m = e / m  # удельный заряд электрон, м^2/с^2
dt = 10**(-8)  # увеличенный временной шаг для ускорения, с
stability = 10**(-6)  # критерий стабилизации
iter_max = 2228 # ограничение на число итераций

f = open('file.txt', 'r+')
data = f.read().splitlines()
currents = []

for i in range(len(data)):
    currents.append(float(data[i]))

U = []
rho_history = []
v_history = []


# Расчёты
for I in currents:
    q0 = 0  # начальный заряд анода
    rho = np.zeros(N)  # зарядовая плотность, Кл/м^3
    phi = np.zeros(N)  # потенциал, B
    E = np.zeros(N)  # электрическое поле, В/м
    v = np.ones(N) * 1000  # начальная скорость зарядов, м/с
    j = np.zeros(N)  # плотность тока, А/м^2

    rho_current_history = []
    v_current_history = []

    for it in range(iter_max):
        rho_old = rho.copy()
        j[0] = I / S

        for k in range(1, N):
            E[k] = E[k - 1] + h * rho[k]  # Расчёт поля E
            phi[k] = phi[k - 1] - h * E[k]  # Расчёт потенциала phi
            v[k] = np.sqrt(2 * e_m * max(0, -phi[k]))  # Расчёт скоростей зарядов v
            j[k] = rho[k] * v[k]  # Расчёт плотности тока j

        for k in range(1, N):
            rho[k] -= (j[k] - j[k - 1]) * dt / h

        q0 += I * dt
        rho[0] = q0 / (h * S)

        rho_current_history.append(rho.copy())
        if it > 20:
            v_current_history.append(v.copy())

        if np.max(np.abs(rho - rho_old)) < stability:
            break

    U.append(-phi[-1])
    v_history.append(v_current_history)
    rho_history.append(rho_current_history)


rho_history_last = rho_history[-1]
v_history_last = v_history[-1]

fig, ax = plt.subplots()
x = np.linspace(0, H, N)
line, = ax.plot(x, v_history_last[0], 'blue', lw=2)
ax.set_xlabel('x, м')
ax.set_ylabel('v, м/с')
ax.set_title('Анимация скорости')
ax.set_ylim(0, 2000)
ax.set_xlim(0.000255, H)

def update(frame):
    line.set_ydata(v_history_last[frame])
    return line,

ani = FuncAnimation(fig, update, frames=len(v_history_last), interval=1, blit=True, repeat=False)
ani.pause()

plt.show()



