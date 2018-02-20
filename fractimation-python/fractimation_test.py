import matplotlib.pylab as pylab
import numpy
import time

from plotplayer.player import PlotPlayer

from renderers.multibrotRenderer import MultibrotRenderer
from renderers.multijuliaRenderer import MultijuliaRenderer
from renderers.sierpinskiTriangleRenderer import SierpinskiTriangleRenderer
from renderers.sierpinskiCarpetRenderer import SierpinskiCarpetRenderer
from renderers.fibonacciSquareRenderer import FibonacciSquareRenderer
from renderers.goldenSpiralRenderer import GoldenSpiralRenderer
from renderers.newtonFractalRenderer import NewtonFractalRenderer

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
constantRealNumber, constantImaginaryNumber = 0.0, 0.0 # Initial Z Value
power = 2                                              # Power to raise Z value to for each iteration of fractal equation
escapeValue = 2.0                                      # Limit at which Z values will reach infinity
multibrotFractal = MultibrotRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax, 
                                      constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)
multibrotZoomHandler = ZoomHandler(multibrotFractal, multibrotViewer)
multibrotViewer.initializeAnimation(maxIterations, multibrotFractal.render, "multibrotFractal", maxIterations)
multibrotFractal.preheatRenderCache(maxIterations)

# Julia Set
multijuliaViewer = PlotPlayer("Julia Set")
realNumberMin, realNumberMax = -1.5, 1.5               # Min & Max values for X values in fractal equation
imaginaryNumberMin, imaginaryNumberMax = -1.5, 1.5     # Min & Max values for Y values in fractal equation
constantRealNumber, constantImaginaryNumber = 0.0, 0.8 # Constant C value
power = 2                                              # Power to raise Z value to for each iteration of fractal equation
escapeValue = 10.0                                     # Limit at which Z values will reach infinity
multijuliaFractal = MultijuliaRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                                        constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)
multijuliaZoomHandler = ZoomHandler(multijuliaFractal, multijuliaViewer)
multijuliaViewer.initializeAnimation(maxIterations, multijuliaFractal.render, "multijuliaFractal", maxIterations)
multijuliaFractal.preheatRenderCache(maxIterations)

# Newton Fractal
newtonFractalViewer = PlotPlayer("Newton Fractal")
realNumberMin, realNumberMax = -10, 10                 # Min & Max values for X values in fractal equation
imaginaryNumberMin, imaginaryNumberMax = -10, 10       # Min & Max values for Y values in fractal equation
constantRealNumber, constantImaginaryNumber = 1.0, 0.0 # Constant C value
coefficientArray = [ -1, 0, 0, 0, 1 ]                  # Representation of polynomial equation coefficients in accending order (ie. c + x + x**2 + ... + x**n)
escapeValue = 1e-4
newtonFractal = NewtonFractalRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                                      coefficientArray, constantRealNumber, constantImaginaryNumber, escapeValue, colorMap)
newtonZoomHandler = ZoomHandler(newtonFractal, newtonFractalViewer)
newtonFractalViewer.initializeAnimation(maxIterations, newtonFractal.render, "newtonFractal", maxIterations)
newtonFractal.preheatRenderCache(maxIterations)

# Sierpinski Triangle (3**iteration triangles per iteration)
sierpinskiTriangleViewer = PlotPlayer("Sierpinski Triangle", toolbarVisible=True)
sierpinskiTriangleIterations = 7                      # Be careful with this number; iterations explode at 3**iteration computations
sierpinskiTriangleLineWidths = numpy.linspace(1.0, 0.1, sierpinskiTriangleIterations)
sierpinskiTriangleFractal = SierpinskiTriangleRenderer(sierpinskiTriangleLineWidths)
sierpinskiTriangleViewer.initializeAnimation(sierpinskiTriangleIterations, sierpinskiTriangleFractal.render, "sierpinskiTriangle", sierpinskiTriangleIterations)
sierpinskiTriangleFractal.preheatRenderCache(sierpinskiTriangleIterations)

# Sierpinski Carpet (8**iteration rectangles per iteration)
sierpinskiCarpetViewer = PlotPlayer("Sierpinski Carpet", toolbarVisible=True)
sierpinskiCarpetIterations = 5                        # Be careful with this number; iterations explode at 8**iteration computations
sierpinskiCarpetLineWidths = numpy.linspace(1.0, 0.1, sierpinskiCarpetIterations)
sierpinskiCarpetFractal = SierpinskiCarpetRenderer(sierpinskiCarpetLineWidths)
sierpinskiCarpetViewer.initializeAnimation(sierpinskiCarpetIterations, sierpinskiCarpetFractal.render,  "sierpinskiCarpet", sierpinskiCarpetIterations)
sierpinskiCarpetFractal.preheatRenderCache(sierpinskiCarpetIterations)

# Fibonacci Square
fibonacciSquareViewer = PlotPlayer("Fibonocci Square", toolbarVisible=True)
fibonacciSquareIterations = 15
fibonacciSquareLineWidths = numpy.linspace(0.1, 1.0, fibonacciSquareIterations)
fibonacciSquareFractal = FibonacciSquareRenderer(fibonacciSquareLineWidths)
fibonacciSquareViewer.initializeAnimation(fibonacciSquareIterations, fibonacciSquareFractal.render, "fibonocciSquare", fibonacciSquareIterations)
fibonacciSquareFractal.preheatRenderCache(fibonacciSquareIterations)

# Golden Spiral
goldenSpiralViewer = PlotPlayer("Golden Spiral", toolbarVisible=True)
goldenSpiralIterations = 15
goldenSpiralLineWidths = numpy.linspace(0.01, 0.05, goldenSpiralIterations)
goldenSpiralFractal = GoldenSpiralRenderer(goldenSpiralLineWidths)
goldenSpiralViewer.initializeAnimation(goldenSpiralIterations, goldenSpiralFractal.render, "goldenSpiral", goldenSpiralIterations)
goldenSpiralFractal.preheatRenderCache(goldenSpiralIterations)

# Render Viewers
PlotPlayer.showPlayers()