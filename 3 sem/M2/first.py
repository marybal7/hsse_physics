import matplotlib.pyplot as plt
import matplotlib.animation as ani

r, x0, y0, vx0, vy0 = 5, 20, 20, 4, 2

def updateFrame(body):
    global x0, y0, vx0, vy0
    vx0 = -vx0 if x0 + r > 100 or x0 - r < 0 else vx0
    vy0 = -vy0 if y0 + r > 100 or y0 - r < 0 else vy0

    x0 += vx0
    y0 += vy0
    print((vx0 ** 2 + vy0 ** 2) / 2)

    ax.clear()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect('equal')

    circle1 = plt.Circle((x0, y0), r, color='m')
    ax.add_artist(circle1)

fig, ax = plt.subplots()
ani = ani.FuncAnimation(fig, updateFrame, frames=400, interval=1)

plt.show()