import plotplayer
import matplotlib.pylab as pylab
import numpy

from renderers.multibrotRenderer import multibrotRenderer
from renderers.multijuliaRenderer import multijuliaRenderer
from renderers.sierpinskiTriangleRenderer import sierpinskiTriangleRenderer
from renderers.sierpinskiCarpetRenderer import sierpinskiCarpetRenderer
from renderers.fibonocciSquareRenderer import fibonacciSquareRenderer

from ui.zoomHandler import zoomHandler

# General Brot & Julia Fractal Parameters
width, height = 1280, 720                              # Width and Height of the image
                                                       # ^^ quick ref : 480p;(640, 480) 720p;(1280, 720) 1080p;(1920, 1080) UHD/4K;(3840, 2160) 8K;(7680, 4320)
maxIterations = 50                                     # Total number of iterations of fractal equation
                                                       # ^^ Careful with this value; we are caching each frame
colorMap = "viridis"                                   # Any valid color map name or combination (default : viridis)
                                                       # ^^ reference : https://matplotlib.org/examples/color/colormaps_reference.html

# Mandelbrot Set
multibrotViewer = plotplayer.plotplayer("Mandelbrot Set")
realNumberMin, realNumberMax = -2.0, 0.5               # Min & Max values for X values in fractal equation
imaginaryNumberMin, imaginaryNumberMax = -1.25, 1.25   # Min & Max values for Y values in fractal equation
constantRealNumber, constantImaginaryNumber = 0.0, 0.0 # Needs some experimentation in Multibrot Set (non-standard)
power = 2                                              # Power to raise Z value to for each iteration of fractal equation
escapeValue = 2.0                                      # Limit at which Z values will reach infinity
multibrotRenderer = multibrotRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax, 
                                      constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)
multibrotViewer.initializeAnimation(maxIterations, multibrotRenderer.render, "multibrotSet")
multibrotZoomHandler = zoomHandler(multibrotRenderer, multibrotViewer)

# Julia Set
multijuliaViewer = plotplayer.plotplayer("Julia Set")
realNumberMin, realNumberMax = -1.5, 1.5
imaginaryNumberMin, imaginaryNumberMax = -1.5, 1.5
constantRealNumber, constantImaginaryNumber = 0.0, 0.8 # Constant C value for Julia Set
power = 2
escapeValue = 2.0
multijuliaRenderer = multijuliaRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                                        constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)
multijuliaViewer.initializeAnimation(maxIterations, multijuliaRenderer.render, "multijuliaSet")
juliaZoomHandler = zoomHandler(multijuliaRenderer, multijuliaViewer)

# Sierpinski Triangle (3**iteration triangles per iteration)
sierpinskiTriangleIterations = 7                      # Be careful with this number; iterations explode at 3**iteration computations
sierpinskiTriangleLineWidths = numpy.linspace(1.0, 0.1, sierpinskiTriangleIterations)
sierpinskiTriangleViewer = plotplayer.plotplayer("Sierpinski Triangle", hideToolbar=False)
sierpinskiTriangleRenderer = sierpinskiTriangleRenderer(sierpinskiTriangleLineWidths)
sierpinskiTriangleViewer.initializeAnimation(sierpinskiTriangleIterations, sierpinskiTriangleRenderer.render, "sierpinskiTriangle", sierpinskiTriangleIterations // 2)

# Sierpinski Carpet (8**iteration rectangles per iteration)
sierpinskiCarpetIterations = 5                        # Be careful with this number; iterations explode at 8**iteration computations
sierpinskiCarpetLineWidths = numpy.linspace(1.0, 0.1, sierpinskiCarpetIterations)
sierpinskiCarpetViewer = plotplayer.plotplayer("Sierpinski Carpet", hideToolbar=False)
sierpinskiCarpetRenderer = sierpinskiCarpetRenderer(sierpinskiCarpetLineWidths)
sierpinskiCarpetViewer.initializeAnimation(sierpinskiCarpetIterations, sierpinskiCarpetRenderer.render,  "sierpinskiCarpet", sierpinskiCarpetIterations // 2)

# Fibonocci Square
fibonocciSquareIterations = 30
fibonocciSquareLineWidths = numpy.linspace(0.1, 1.0, fibonocciSquareIterations)
fibonocciSquareViewer = plotplayer.plotplayer("Fibonocci Square", hideToolbar=False)
fibonocciSquareRenderer = fibonacciSquareRenderer(fibonocciSquareLineWidths)
fibonocciSquareViewer.initializeAnimation(fibonocciSquareIterations, fibonocciSquareRenderer.render, "fibonocciSquare")

fibonocciSquareViewer.play()
fibonocciSquareViewer.show()

# Render Viewers and Play Animations
multibrotViewer.show(False)
multijuliaViewer.show(False)
sierpinskiTriangleViewer.show(False)

multibrotViewer.play()
multijuliaViewer.play()
sierpinskiTriangleViewer.play()
sierpinskiCarpetViewer.play()

sierpinskiCarpetViewer.show()