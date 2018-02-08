import videofig
import multibrot_videofig

width, height = 1280, 720  # Width and Height of the image
xMin, xMax = -2.0, 0.5     # Min & Max values for X values in fractal equation
yMin, yMax = -1.25, 1.25   # Min & Max values for Y values in fractal equation
power = 2                  # Power to raise Z value to for each iteration of fractal equation
escapeValue = 2.0          # Limit at which Z values will reach infinity
maxIterations = 25         # Total number of iterations of fractal equation
                           #  ^^ Careful with this value; we are caching each frame

mandelbrotRenderer = multibrot_videofig.multibrot_videofig(width, height, xMin, xMax, yMin, yMax, power, escapeValue)
videofig.videofig(maxIterations, mandelbrotRenderer.iterate)