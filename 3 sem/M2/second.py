import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation

r, v, k, m = 0.1, 0.2, 80, 1

x0, y0 = 0.2, 0.2
vx0, vy0 = -v * 1, v * 2
interval = 0.02
prev_time = time.time()

def updateAxes():
    global axes
    axes.clear()
    axes.set_xlim(0, 1)
    axes.set_ylim(0, 1)
    axes.set_aspect('equal')

def printEnergy():
    global prev_time
    if time.time() - prev_time > 0.2:
        print("energy:", m * (vx0 ** 2 + vy0 ** 2) / 2)
        prev_time = time.time()


def updatePositions(frame):
    global x0, y0, vx0, vy0
    vx0 = vx0 + interval * (k * ((abs(x0 - r)) ** (3 / 2))) / m if x0 - r <= 0 else vx0 - interval * (
                    k * ((abs(x0 + r - 1)) ** (3 / 2))) / m if x0 + r >= 1 else vx0
    vy0 = vy0 + interval * (k * ((abs(y0 - r)) ** (3 / 2))) / m if y0 - r <= 0 else vy0 - interval * (
                    k * ((abs(y0 + r - 1)) ** (3 / 2))) / m if y0 + r >= 1 else vy0

    x0 += vx0 * interval
    y0 += vy0 * interval
    printEnergy()
    updateAxes()

    circle = plt.Circle((x0, y0), r, color='m')
    axes.add_artist(circle)

fig, axes = plt.subplots()
ani = animation.FuncAnimation(fig, updatePositions, frames=400, interval=10)

plt.show()