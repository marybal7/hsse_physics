import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

H = 0.01  # расстояние между пластинами, м
S = 0.0001  # площадь пластин, м^2
N = 40  # число слоёв
h = H / N  # толщина слоя

# Физические константы
e = 1.6e-19  # заряд электрона, Кл
m = 9.1e-31  # масса электрона, кг
e_m = e / m  # удельный заряд электрон, м^2/с^2
dt = 1e-8  # временной шаг, с
stability = 1e-6  # критерий стабилизации
iter_max = 2228  # максимальное число итераций

# Загрузка данных
with open('file.txt', 'r') as f:
    currents = [float(line) for line in f]

U = []
x = np.linspace(0, H, N)

# Создание графика
fig, ax = plt.subplots()
line, = ax.plot(x, np.zeros(N), 'r', lw=2)
ax.set_xlabel('x (м)')
ax.set_ylabel('ρ (Кл/м³)')
ax.set_title('Эволюция зарядовой плотности')
ax.set_ylim(-1e-4, 1e-4)

# Анимация
rho_history = []


def compute_rho(I):
    q0 = 0  # начальный заряд анода
    rho = np.zeros(N)
    phi = np.zeros(N)
    E = np.zeros(N)
    v = np.ones(N) * 1000
    j = np.zeros(N)

    for it in range(iter_max):
        rho_old = rho.copy()
        j[0] = I / S

        for k in range(1, N):
            E[k] = E[k - 1] + h * rho[k]
            phi[k] = phi[k - 1] - h * E[k]
            v[k] = np.sqrt(2 * e_m * max(0, -phi[k]))
            j[k] = rho[k] * v[k]

        for k in range(1, N):
            rho[k] -= (j[k] - j[k - 1]) * dt / h

        q0 += I * dt
        rho[0] = q0 / (h * S)
        rho_history.append(rho.copy())

        if np.max(np.abs(rho - rho_old)) < stability:
            break

    U.append(-phi[-1])


def update(frame):
    line.set_ydata(rho_history[frame])
    return line,


# Запуск вычислений для первого тока
compute_rho(currents[0])
ani = FuncAnimation(fig, update, frames=len(rho_history), interval=50, blit=True)

plt.show()
