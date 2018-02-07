from matplotlib import pyplot as plt
from matplotlib import animation

import mandelbrot_matplotlib

width, height = 1024, 768
xmin, xmax = -2, 0.5
ymin, ymax = -1.25, 1.25
escapeValue = 2.0

fig = plt.figure()
canvas = plt.axes(xlim=(0, width), ylim=(0, height))
mandelbrotRenderer = mandelbrot_matplotlib.mandelbrot_matplotlib(width, height, xmin, xmax, ymin, ymax, escapeValue)

def animate(frameNumber):
    imageArray = mandelbrotRenderer.iterate(frameNumber)
    render = canvas.imshow(imageArray)
    #render.write_png('output\\mandel_matplotlib_' + str(frameNumber) + '.png')
    return render,

anim = animation.FuncAnimation(fig, animate, frames=25, interval=100, blit=True, repeat=False)
plt.show()