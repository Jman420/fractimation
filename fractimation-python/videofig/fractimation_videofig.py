import videofig
import multibrot_videofig
import multijulia_videofig

width, height = 1280, 720                              # Width and Height of the image
maxIterations = 50                                     # Total number of iterations of fractal equation
                                                       #  ^^ Careful with this value; we are caching each frame

# Mandelbrot Set
realNumberMin, realNumberMax = -2.0, 0.5               # Min & Max values for X values in fractal equation
imaginaryNumberMin, imaginaryNumberMax = -1.25, 1.25   # Min & Max values for Y values in fractal equation
power = 2                                              # Power to raise Z value to for each iteration of fractal equation
escapeValue = 2.0                                      # Limit at which Z values will reach infinity
renderer = multibrot_videofig.multibrot_videofig(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax, power, escapeValue)
videofig.videofig(maxIterations, renderer.iterate)

# Julia Set
realNumberMin, realNumberMax = -1.5, 1.5
imaginaryNumberMin, imaginaryNumberMax = -1.5, 1.5
constantRealNumber, constantImaginaryNumber = 0.0, 0.8
power = 2
escapeValue = 10.0
renderer = multijulia_videofig.multijulia_videofig(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax, constantRealNumber,
                                                  constantImaginaryNumber, power, escapeValue)
videofig.videofig(maxIterations, renderer.iterate)