import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

width, height = 800, 600
xmin, xmax = -2, 0.5
ymin, ymax = -1.25, 1.25

ix, iy = np.mgrid[0:width, 0:height]
x = np.linspace(xmin, xmax, width)[ix]
y = np.linspace(ymin, ymax, height)[iy]
c = x+complex(0,1)*y
del x, y

canvas = np.zeros(c.shape, dtype=int)
imageShape = width * height
ix.shape = imageShape
iy.shape = imageShape
c.shape = imageShape
z = np.copy(c)

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, width), ylim=(0, height))

# initialization function: plot the background of each frame
def init():
    print('Iteration init')
    print(canvas.T)

    render = ax.imshow(canvas.T, origin='lower left')
    return render,

# animation function.  This is called sequentially
def animate(i):
    global ix, iy, c, z, canvas

    if not len(z):
        render = ax.imshow(canvas.T, origin='lower left')
        return render,

    np.multiply(z, z, z)
    np.add(z, c, z)
    rem = np.abs(z)>2.0
    canvas[ix[rem], iy[rem]] = i

    rem = ~rem
    z = z[rem]
    ix, iy = ix[rem], iy[rem]
    c = c[rem]

    render = ax.imshow(canvas.T, origin='lower left')
    return render,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=100, interval=20, blit=True, repeat=False)

plt.show()