import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from time import sleep as sleep
import random
radius1 = 1
radius2 = 4
fig = plt.figure()
ax = plt.axes(xlim=(-10, 11), ylim=(-10, 10))
line, = ax.plot([], [])
plt.axis('off')
def init():
    # creating an empty plot/frame
    line.set_data([], [])
    return line,
xdata, ydata = [], []

speed_def = 1

def animate(i):
    global xdata, ydata
    global speed_def
    global radius1
    global radius2
    global count
    theta1 = i
    theta2 = theta1*speed_def
    x1 = radius1 * np.cos(theta1) + 1
    y1 = radius1 * np.sin(theta1)
    x2 = radius2 * np.cos(theta2)
    y2 = radius2 * np.sin(theta2)
    xdata.append(x1)
    xdata.append(x2)
    ydata.append(y1)
    ydata.append(y2)
    line.set_data(xdata, ydata)
    if i == 2 * np.pi:
        xdata, ydata = [], []
        speed_def = random.randint(0, count)
        sleep(4)
        radius1 = 1 + random.randint(0, 10)
        radius2 = random.randint(0, 10)
        count = random.randint(10,200)
        print(f'speed deference = {speed_def}')
    return line,



count = 100
frame_count = np.linspace(0, 2*np.pi, count)
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frame_count, interval=30, blit=True)
plt.show()


