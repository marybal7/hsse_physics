import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

g = 9.81  # Ускорение свободного падения, м/с^2
m = 1.0  # Масса тела, кг
k = 10  # Коэффициент вязкого сопротивления воздуха
c = 100  # Коэффициент лобового сопротивления воздуха
v0 = 80  # Начальная скорость
theta = 45  # Угол броска
x0, y0 = 0, 0  # Начальные координаты
dt_start = 0  # Начальная дельта
epsilon = 0.00005  # Погрешность


# Аналитическое решение для вязкого трения
class AnalyticSolution:
    def getFlightTime(self):
        theta_rad = np.radians(theta)
        v0y = v0 * np.sin(theta_rad)
        d = v0y ** 2 + 2 * g * y0
        if d < 0:
            print("incorrent input")
            return
        x1 = (v0y - math.sqrt(d)) / g
        x2 = (v0y + math.sqrt(d)) / g
        if (x1 > 0 and x2 > 0):
            self.flight_time = min(x1, x2)
        elif (x1 >= 0 or x2 >= 0):
            self.flight_time = max(x1, x2)
        else:
            print("incorrent input")
        return self.flight_time

    def getFinalX(self, drag_type):
        v0x = v0 * np.cos(np.radians(theta))
        if drag_type == 'linear':
            self.x_linear = x0 + v0x * m * (1 - math.exp(-k * self.flight_time / m)) / k
            return self.x_linear


def motion_model(dt, drag, model='linear'):
    # Начальные условия
    k = drag
    theta_rad = np.radians(theta)  # Угол в радианах
    vx = v0 * np.cos(theta_rad)  # Начальная скорость по оси x
    vy = v0 * np.sin(theta_rad)  # Начальная скорость по оси y

    x, y = x0, y0  # Начальные координаты
    t = 0  # Время
    trajectory_x, trajectory_y = [x], [y]  # Массивы для хранения траектории

    while y >= 0:  # Пока тело не достигло земли
        # Сила тяжести
        fx = 0
        fy = -m * g

        # Сила сопротивления воздуха
        if model == 'linear':
            # Вязкое трение (пропорционально скорости)
            fx -= k * vx
            fy -= k * vy
        elif model == 'quadratic':
            # Лобовое сопротивление (пропорционально квадрату скорости)
            speed = np.sqrt(vx ** 2 + vy ** 2)
            fx -= k * vx * speed
            fy -= k * vy * speed

        # Ускорение
        ax = fx / m
        ay = fy / m

        vx += ax * dt
        vy += ay * dt
        # Обновление координат
        x += vx * dt
        y += vy * dt

        v = np.sqrt(vx ** 2 + vy ** 2)
        a = np.sqrt(ax ** 2 + ay ** 2)
        dt = epsilon * (v / a)

        # Сохранение траектории
        trajectory_x.append(x)
        trajectory_y.append(y)

        # Обновление времени
        t += dt
    print("max x real: ", trajectory_x[-1])
    return trajectory_x, trajectory_y


# Функция для анимации траектории
def animate_trajectory(dt, drag, model='linear'):
    # Получение траектории
    x, y = motion_model(dt, drag, model)

    # Настройка графика
    fig, ax = plt.subplots()
    ax.set_xlim(0, 1.1 * max(x))
    ax.set_ylim(0, 1.1 * max(y))
    line, = ax.plot([], [], 'o-', lw=1, c='mediumslateblue', ms=2.2)
    ax.set_xlabel('Расстояние (м)')
    ax.set_ylabel('Высота (м)')
    ax.set_title(f'Анимация полета: v0={v0} м/с, угол={theta}°')

    # Функция для инициализации графика
    def init():
        line.set_data([], [])
        return line,

    # Функция для обновления кадров
    def update(num):
        num = num * 10000
        line.set_data(x[:num], y[:num])
        if num >= len(x): ani.event_source.stop()
        return line,

    # Создание анимации
    ani = FuncAnimation(fig, update, frames=len(x), init_func=init, interval=dt * 100, blit=True)
    plt.grid(True)
    plt.show()


# Исследование траектории для вязкого трения и лобового сопротивления
theoretic_sol = AnalyticSolution()
print("flight time: ", theoretic_sol.getFlightTime())

# Анимация траектории для обоих случаев
print("Final x, linear drag: ", theoretic_sol.getFinalX("linear"))
animate_trajectory(dt_start, k, model='linear')  # Вязкое трение
animate_trajectory(dt_start, c, model='quadratic')  # Лобовое сопротивление