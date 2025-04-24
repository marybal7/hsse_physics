import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def draw_ray(ax, start, direction, length, color='orange', linestyle='-'):
    direction = direction / np.linalg.norm(direction)
    end = start + direction * length
    ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]],
            color=color, linestyle=linestyle, linewidth=1)


def update_plot(object_x):
    ax.clear()

    # Параметры
    lens_x = 0  # Положение линзы
    focus_lens = -5  # Фокус линзы
    height = 5  # Высота предмета
    num_rays = 4  # Кол-во лучей из вершины стрелки
    ray_length = 30

    ax.set_title("Ход лучей через тонкую рассеивающую линзу")

    # Предмет
    object_pos = np.array([object_x, 0, 0])
    arrow_top = object_pos + np.array([0, 0, height])
    ax.plot([object_pos[0], arrow_top[0]], [0, 0], [object_pos[2], arrow_top[2]],
            color='black', linewidth=2)

    # Линза
    theta = np.linspace(0, 2 * np.pi, 100)
    r = 2
    x = np.zeros_like(theta)
    y = r * np.cos(theta)
    z = r * np.sin(theta)
    ax.plot(x, y, z, color='blue', alpha=0.5)

    # Фокусы
    focus_left = lens_x - focus_lens
    focus_right = lens_x + focus_lens
    ax.scatter([focus_left, focus_right], [0, 0], [0, 0], color='red', s=50)
    ax.text(focus_left, 0, 0.5, "F'", color='red')
    ax.text(focus_right, 0, 0.5, "F", color='red')

    # Построение лучей
    z_values_rays = np.linspace(0.1, height, num_rays)
    z_values_center_rays = np.linspace(0.1, height, num_rays)

    for z in z_values_rays:
        start = np.array([object_x, 0, z])
        intersection = np.array([lens_x, 0, z])
        draw_ray(ax, start, np.array([1, 0, 0]), -object_x, color='orange')
        dz = -z / focus_lens
        refracted_dir = np.array([1, 0, dz])
        draw_ray(ax, np.array([lens_x, 0, z]), refracted_dir, ray_length, color='red')
        draw_ray(ax, np.array([lens_x, 0, z]), -refracted_dir, ray_length, color='red', linestyle='dotted')

    for z in z_values_center_rays:
        start = np.array([object_x, 0, z])
        center_dir = np.array([lens_x - object_x, 0, -z])
        draw_ray(ax, start, center_dir, ray_length * 2, color='green', linestyle='dashed')

    # Изображение
    a = abs(object_x - lens_x)
    f = focus_lens
    b = 1 / (1 / f - 1 / a)
    magnification = -b / a
    image_x = lens_x + b
    image_height = height * magnification

    image_bottom = np.array([image_x, 0, 0])
    image_top = np.array([image_x, 0, image_height])
    ax.plot([image_bottom[0], image_top[0]], [0, 0], [0, image_height],
            color='purple', linewidth=2)

    ax.set_xlabel("X (оптическая ось)")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z (высота)")
    ax.set_xlim([-15, 15])
    ax.set_ylim([-5, 5])
    ax.set_zlim([-5, 5])
    fig.canvas.draw_idle()


fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111, projection='3d')

plt.subplots_adjust(bottom=0.25)

ax_slider = plt.axes([0.15, 0.1, 0.65, 0.03])
slider = Slider(ax_slider, 'Object X', -20, -1, valinit=-8, valstep=0.1)


def update(val):
    object_x = slider.val
    update_plot(object_x)


slider.on_changed(update)

update_plot(-8)

plt.tight_layout()
plt.show()
