import matplotlib.pylab as pylab
import numpy

from plotplayer import PlotPlayer

from renderers.multibrotRenderer import multibrotRenderer
from renderers.multijuliaRenderer import multijuliaRenderer
from renderers.sierpinskiTriangleRenderer import sierpinskiTriangleRenderer
from renderers.sierpinskiCarpetRenderer import sierpinskiCarpetRenderer
from renderers.fibonacciSquareRenderer import fibonacciSquareRenderer
from renderers.goldenSpiralRenderer import goldenSpiralRenderer

from ui.zoomHandler import ZoomHandler

# General Brot & Julia Fractal Parameters
width, height = 1280, 720                              # Width and Height of the image
                                                       # ^^ quick ref : 480p;(640, 480) 720p;(1280, 720) 1080p;(1920, 1080) UHD/4K;(3840, 2160) 8K;(7680, 4320)
maxIterations = 50                                     # Total number of iterations of fractal equation
                                                       # ^^ Careful with this value; we are caching each frame
colorMap = "viridis"                                   # Any valid color map name or combination (default : viridis)
                                                       # ^^ reference : https://matplotlib.org/examples/color/colormaps_reference.html

# Mandelbrot Set
multibrotViewer = PlotPlayer("Mandelbrot Set")
realNumberMin, realNumberMax = -2.0, 0.5               # Min & Max values for X values in fractal equation
imaginaryNumberMin, imaginaryNumberMax = -1.25, 1.25   # Min & Max values for Y values in fractal equation
constantRealNumber, constantImaginaryNumber = 0.0, 0.0 # Needs some experimentation in Multibrot Set (non-standard)
power = 2                                              # Power to raise Z value to for each iteration of fractal equation
escapeValue = 2.0                                      # Limit at which Z values will reach infinity
multibrotFractal = multibrotRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax, 
                                      constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)
multibrotViewer.initializeAnimation(maxIterations, multibrotFractal.render)
multibrotZoomHandler = ZoomHandler(multibrotFractal, multibrotViewer)

# Julia Set
multijuliaViewer = PlotPlayer("Julia Set")
realNumberMin, realNumberMax = -1.5, 1.5
imaginaryNumberMin, imaginaryNumberMax = -1.5, 1.5
constantRealNumber, constantImaginaryNumber = 0.0, 0.8 # Constant C value for Julia Set
power = 2
escapeValue = 10.0
multijuliaFractal = multijuliaRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                                        constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)
multijuliaViewer.initializeAnimation(maxIterations, multijuliaFractal.render)
juliaZoomHandler = ZoomHandler(multijuliaFractal, multijuliaViewer)

# Sierpinski Triangle (3**iteration triangles per iteration)
sierpinskiTriangleViewer = PlotPlayer("Sierpinski Triangle", hideToolbar=False)
sierpinskiTriangleIterations = 7                      # Be careful with this number; iterations explode at 3**iteration computations
sierpinskiTriangleLineWidths = numpy.linspace(1.0, 0.1, sierpinskiTriangleIterations)
sierpinskiTriangleFractal = sierpinskiTriangleRenderer(sierpinskiTriangleLineWidths)
sierpinskiTriangleViewer.initializeAnimation(sierpinskiTriangleIterations, sierpinskiTriangleFractal.render, "sierpinskiTriangle", sierpinskiTriangleIterations // 2)
#sierpinskiTriangleRenderer.preheatCache(sierpinskiTriangleIterations)

# Sierpinski Carpet (8**iteration rectangles per iteration)
sierpinskiCarpetViewer = PlotPlayer("Sierpinski Carpet", hideToolbar=False)
sierpinskiCarpetIterations = 5                        # Be careful with this number; iterations explode at 8**iteration computations
sierpinskiCarpetLineWidths = numpy.linspace(1.0, 0.1, sierpinskiCarpetIterations)
sierpinskiCarpetFractal = sierpinskiCarpetRenderer(sierpinskiCarpetLineWidths)
sierpinskiCarpetViewer.initializeAnimation(sierpinskiCarpetIterations, sierpinskiCarpetFractal.render,  "sierpinskiCarpet", sierpinskiCarpetIterations // 2)
#sierpinskiCarpetRenderer.preheatCache(sierpinskiCarpetIterations)

# Fibonacci Square
fibonacciSquareViewer = PlotPlayer("Fibonocci Square", hideToolbar=False)
fibonacciSquareIterations = 15
fibonacciSquareLineWidths = numpy.linspace(0.1, 1.0, fibonacciSquareIterations)
fibonacciSquareFractal = fibonacciSquareRenderer(fibonacciSquareLineWidths)
fibonacciSquareViewer.initializeAnimation(fibonacciSquareIterations, fibonacciSquareFractal.render, "fibonocciSquare")

# Golden Spiral
goldenSpiralViewer = PlotPlayer("Golden Spiral", hideToolbar=False)
goldenSpiralIterations = 15
goldenSpiralLineWidths = numpy.linspace(0.01, 0.05, goldenSpiralIterations)
goldenSpiralFractal = goldenSpiralRenderer(goldenSpiralLineWidths)
goldenSpiralViewer.initializeAnimation(goldenSpiralIterations, goldenSpiralFractal.render, "goldenSpiral")

# Render Viewers
PlotPlayer.showPlayers()