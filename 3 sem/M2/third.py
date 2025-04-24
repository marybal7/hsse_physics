import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

r, x01, y01, x02, y02, vx1, vy1, vx2, vy2 = 5, 20, 20, 80, 80, 3, 5, 2, 1

def updateAxes():
    axes.clear()
    axes.set_xlim(0, 100)
    axes.set_ylim(0, 100)
    axes.set_aspect('equal')

    firstCircle = plt.Circle((x01, y01), r, color='lightpink')
    axes.add_artist(firstCircle)
    secondCircle = plt.Circle((x02, y02), r, color='tan')
    axes.add_artist(secondCircle)

def proccessCollision():
    global vx1, vx2, vy1, vy2
    distance = math.sqrt((x01 - x02) ** 2 + (y01 - y02) ** 2)
    if distance <= 2 * r:
        dx, dy = x02 - x01, y02 - y01
        nx, ny = dx / distance, dy / distance  # нормальный вектор

        # Скорости вдоль нормали
        v1n = vx1 * nx + vy1 * ny
        v2n = vx2 * nx + vy2 * ny

        # Обмен импульсами вдоль нормали (абсолютно упругий удар)
        v1n_new = v2n
        v2n_new = v1n

        vx1 += (v1n_new - v1n) * nx
        vy1 += (v1n_new - v1n) * ny
        vx2 += (v2n_new - v2n) * nx
        vy2 += (v2n_new - v2n) * ny

        vx1, vx2 = vx2, vx1
        vy1, vy2 = vy2, vy1
        print("first ball energy:", (vx1 ** 2 + vy1 ** 2) / 2)
        print("second ball energy:", (vx2 ** 2 + vy2 ** 2) / 2)
        print("summary energy:", (vx1 ** 2 + vy1 ** 2) / 2 + (vx2 ** 2 + vy2 ** 2) / 2)
        print("---------------------------")


def updateFrame(body):
    global x01, y01, x02, y02, vx1, vy1, vx2, vy2
    vx1 = -abs(vx1) if x01 + r >= 100 else abs(vx1) if x01 - r <= 0 else vx1
    vy1 = -abs(vy1) if y01 + r >= 100 else abs(vy1) if y01 - r <= 0 else vy1
    vx2 = -abs(vx2) if x02 + r >= 100 else abs(vx2) if x02 - r <= 0 else vx2
    vy2 = -abs(vy2) if y02 + r >= 100 else abs(vy2) if y02 - r <= 0 else vy2
    proccessCollision()
    x01 += vx1
    y01 += vy1
    x02 += vx2
    y02 += vy2
    updateAxes()


fig, axes = plt.subplots()
ani = animation.FuncAnimation(fig, updateFrame, frames=400, interval=1)

plt.show()