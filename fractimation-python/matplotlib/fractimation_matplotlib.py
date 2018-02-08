from matplotlib import pyplot as plt
from matplotlib import animation

import mandelbrot_matplotlib

width, height = 1280, 720
xMin, xMax = -2.0, 0.5
yMin, yMax = -1.25, 1.25
escapeValue = 2.0
maxIterations = 25

fig = plt.figure()
canvas = plt.axes(xlim=(0, width), ylim=(0, height))
mandelbrotRenderer = mandelbrot_matplotlib.mandelbrot_matplotlib(width, height, xMin, xMax, yMin, yMax, escapeValue)

def animate(frameNumber):
    imageArray = mandelbrotRenderer.iterate(frameNumber)
    render = canvas.imshow(imageArray)
    return render,

anim = animation.FuncAnimation(fig, animate, frames=maxIterations, interval=40, blit=True, repeat=False)
plt.show()