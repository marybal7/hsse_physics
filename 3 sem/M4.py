import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
from scipy.special import ellipk

# Константы
g = 9.81  # ускорение свободного падения, м/с^2
L = 1.0   # расстояние до центра масс, м
m = 1.0   # масса маятника, кг
b = 0.5   # коэффициент сопротивления воздуха (0 для идеального маятника)
a = 0.2
r = 1
I1 = (1 / 3) * m * L**2  # момент инерции (для тонкого стержня)
I2 = m * r**2 / 2 # момент инерции (для диска)
I3 = m * r**2 # момент инерции (для цилиндра)
I4 = (1 / 6) * m * a**2 + m * L**2 # момент инерции (для куба)

I = I3

# Начальные условия
theta0 = np.radians(50)  # начальное отклонение, рад
omega0 = 0.0             # начальная угловая скорость, рад/с
y0 = [theta0, omega0]    # начальные условия (угол и угловая скорость)

# Временной интервал моделирования
dt = 0.01  # шаг времени, с
t_max = 10  # время моделирования, с
time = np.arange(0, t_max, dt)

# Уравнения движения с учетом момента инерции и сопротивления воздуха
def equations_with_drag(y, t):
    theta, omega = y
    dtheta_dt = omega
    domega_dt = -(m * g * L * np.sin(theta)) / I - b * omega / I
    return [dtheta_dt, domega_dt]

# Решение уравнения методом Рунге-Кутта
solution_drag = odeint(equations_with_drag, y0, time)
theta_drag = solution_drag[:, 0]  # Угол

# Анимация движения маятника
fig, ax = plt.subplots()
ax.set_xlim(-L - 0.2, L + 0.2)
ax.set_ylim(-L - 0.2, L + 0.2)
ax.set_aspect('equal')
ax.grid(True)

line, = ax.plot([], [], 'o-', lw=2, label="Маятник")
trail, = ax.plot([], [], 'r-', lw=1, alpha=0.5, label="Траектория")
ax.legend()

def init():
    line.set_data([], [])
    trail.set_data([], [])
    return line, trail

def update(frame):
    x = L * np.sin(theta_drag[frame])
    y = -L * np.cos(theta_drag[frame])
    line.set_data([0, x], [0, y])
    trail.set_data(L * np.sin(theta_drag[:frame]), -L * np.cos(theta_drag[:frame]))
    return line, trail

ani = FuncAnimation(fig, update, frames=len(time), init_func=init, blit=True, interval=dt * 1000)

plt.title("Движение маятника с учетом момента инерции и сопротивления воздуха")
plt.show()
plt.close()

def T_exact(theta0):
    k = np.sin(theta0 / 2)**2
    return 4 * np.sqrt(I / (m * g * L)) * ellipk(k)

def T_analytical(theta0):
    return 2 * np.pi * np.sqrt(I / (m * g * L)) * (1 + (theta0**2) / 16 + (11 * theta0**4) / 3072)

theta = np.linspace(0, np.pi/2, 150)

T_num = T_exact(theta)
T_small = T_analytical(theta)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(theta * 180 / np.pi, T_num, label="Численное решение", color="b")
plt.plot(theta * 180 / np.pi, T_small, label="Аналитическое решение (с поправками)", linestyle="--", color="r")
plt.xlabel("Амплитуда θ₀ (градусы)")
plt.ylabel("Период T (с)")
plt.title("Зависимость периода от амплитуды")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()