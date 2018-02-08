import videofig
import matplotlib.pylab as pylab

import multibrotRenderer as multibrot
import multijuliaRenderer as multijulia

width, height = 1280, 720                              # Width and Height of the image
maxIterations = 50                                     # Total number of iterations of fractal equation
                                                       #  ^^ Careful with this value; we are caching each frame

# Mandelbrot Set
realNumberMin, realNumberMax = -2.0, 0.5               # Min & Max values for X values in fractal equation
imaginaryNumberMin, imaginaryNumberMax = -1.25, 1.25   # Min & Max values for Y values in fractal equation
constantRealNumber, constantImaginaryNumber = 0.0, 0.0 # Needs some experimentation in Mandelbrot Set (non-standard)
power = 2                                              # Power to raise Z value to for each iteration of fractal equation
escapeValue = 2.0                                      # Limit at which Z values will reach infinity
multibrotRenderer = multibrot.multibrotRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                                                constantRealNumber, constantImaginaryNumber, power, escapeValue)
mandelbrot = videofig.videofig("Mandelbrot Set")
mandelbrot.initializeAnimation(maxIterations, multibrotRenderer.render)
pylab.plt.show(False)

# Julia Set
realNumberMin, realNumberMax = -1.5, 1.5
imaginaryNumberMin, imaginaryNumberMax = -1.5, 1.5
constantRealNumber, constantImaginaryNumber = 0.0, 0.8 # Constant C value for Julia Set
power = 2
escapeValue = 10.0
multijuliaRenderer = multijulia.multijuliaRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                                                   constantRealNumber, constantImaginaryNumber, power, escapeValue)
julia = videofig.videofig("Julia Set")
julia.initializeAnimation(maxIterations, multijuliaRenderer.render)

mandelbrot.play()
julia.play()

try:
    pylab.plt.show()
except AttributeError:
    pass