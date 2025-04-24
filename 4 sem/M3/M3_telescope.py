import numpy as np
import matplotlib.pyplot as plt


def draw_ray(ax, start, direction, length, color='orange', linestyle='-'):
    direction = direction / np.linalg.norm(direction)
    end = start + direction * length
    ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]],
            color=color, linestyle=linestyle, linewidth=1)


def draw_lens(ax, x_pos, radius, label):
    theta = np.linspace(0, 2 * np.pi, 100)
    y = radius * np.cos(theta)
    z = radius * np.sin(theta)
    x = np.full_like(theta, x_pos)
    ax.plot(x, y, z, color='blue', alpha=0.5)
    ax.text(x_pos, 0, radius + 0.3, label, color='blue')


# Параметры телескопа
object_x = -1000  # Положение объекта (мм), имитация бесконечности
objective_x = 0  # Положение объектива (мм)
f_obj = 50  # Фокусное расстояние объектива (мм)
f_eye = 25  # Фокусное расстояние окуляра (мм)
eyepiece_x = objective_x + f_obj + f_eye  # Окуляр на расстоянии f_obj + f_eye
object_height = 10  # Высота объекта (мм)
num_rays = 4  # Количество лучей
ray_length = 200  # Длина лучей для визуализации (мм)
d = 250  # Расстояние наилучшего зрения (мм)

fig = plt.figure(figsize=(18, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Модель телескопа Кеплера")

# Предмет
object_pos = np.array([object_x, 0, 0])
arrow_top = object_pos + np.array([0, 0, object_height])
ax.plot([object_pos[0], arrow_top[0]], [0, 0], [object_pos[2], arrow_top[2]],
        color='black', linewidth=2)

# Линзы
draw_lens(ax, objective_x, 5, "Объектив")
draw_lens(ax, eyepiece_x, 3, "Окуляр")

# Объектив
f_obj_left = objective_x - f_obj
f_obj_right = objective_x + f_obj
ax.scatter([f_obj_left, f_obj_right], [0, 0], [0, 0], color='red', s=30)
ax.text(f_obj_left, 0, 0.2, "F'", color='red')
ax.text(f_obj_right, 0, 0.2, "F", color='red')

# Окуляр
f_eye_left = eyepiece_x - f_eye
f_eye_right = eyepiece_x + f_eye
ax.scatter([f_eye_left, f_eye_right], [0, 0], [0, 0], color='blue', s=30)
ax.text(f_eye_left, 0, 0.2, "F'", color='blue')
ax.text(f_eye_right, 0, 0.2, "F", color='blue')

z_values = np.linspace(0.1, 5, num_rays)

# Промежуточное изображение
image_x_obj = objective_x + f_obj
magnification_obj = -f_obj / abs(object_x - objective_x)
image_height_obj = object_height * magnification_obj
int_image_bottom = np.array([image_x_obj, 0, 0])
int_image_top = np.array([image_x_obj, 0, image_height_obj])
ax.plot([int_image_bottom[0], int_image_top[0]], [0, 0], [0, image_height_obj],
        color='purple', linewidth=2)

print(f"Промежуточное изображение на {image_x_obj:.1f} мм (до окуляра: {eyepiece_x - image_x_obj:.1f} мм)")

for z in z_values:
    start = np.array([object_x, 0, z])

    draw_ray(ax, start, np.array([1, 0, 0]), abs(object_x - objective_x), color='orange')
    dz = -z / f_obj
    refracted_dir_obj = np.array([1, 0, dz])
    draw_ray(ax, np.array([objective_x, 0, z]), refracted_dir_obj, abs(image_x_obj - objective_x), color='orange')

    center_dir_obj = np.array([objective_x - object_x, 0, -z])
    draw_ray(ax, start, center_dir_obj, abs(object_x - image_x_obj), color='green', linestyle='dashed')

    int_image_z = z * magnification_obj
    int_image_pos = np.array([image_x_obj, 0, int_image_z])

    draw_ray(ax, int_image_pos, np.array([1, 0, 0]), abs(image_x_obj - eyepiece_x), color='orange')
    refracted_dir_eye = np.array([1, 0, -int_image_z / f_eye])
    draw_ray(ax, int_image_pos, refracted_dir_eye, ray_length, color='orange')

    center_dir_eye = np.array([eyepiece_x - image_x_obj, 0, -int_image_z])
    draw_ray(ax, int_image_pos, center_dir_eye, ray_length, color='green', linestyle='dashed')

# Итоговое мнимое изображение
image_x_eye = eyepiece_x - d
magnification_eye = d / f_eye
image_height_eye = image_height_obj * magnification_eye

for z in z_values:
    int_image_z = z * magnification_obj
    start_eye = np.array([eyepiece_x, 0, int_image_z])
    dir_eye = np.array([-1, 0, int_image_z / d])
    draw_ray(ax, start_eye, dir_eye, d, color='red', linestyle=':')

image_eye_bottom = np.array([image_x_eye, 0, 0])
image_eye_top = np.array([image_x_eye, 0, image_height_eye])
ax.plot([image_eye_bottom[0], image_eye_top[0]], [0, 0], [0, image_height_eye],
        color='purple', linestyle=':', linewidth=2)

magnification_total = abs(magnification_obj * magnification_eye)
print(f"\nПараметры телескопа:")
print(f"- Увеличение объектива (угловое) = {abs(magnification_obj):.3f}")
print(f"- Увеличение окуляра = {magnification_eye:.1f}")
print(f"- Общее увеличение = {magnification_total:.1f}")

ax.set_xlabel("X (оптическая ось, мм)")
ax.set_ylabel("Y (мм)")
ax.set_zlabel("Z (высота, мм)")
ax.set_xlim([object_x, eyepiece_x + 50])
ax.set_ylim([-10, 10])
ax.set_zlim([-10, 10])
plt.tight_layout()
plt.show()
