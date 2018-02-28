import matplotlib.pylab as pylab
import numpy
import time

from plotplayer.plotplayer import PlotPlayer
from plotplayer.managers.window_manager import WindowManager

from fractimation.renderers.multibrotRenderer import MultibrotRenderer
from fractimation.renderers.multijuliaRenderer import MultijuliaRenderer
from fractimation.renderers.sierpinskiTriangleRenderer import SierpinskiTriangleRenderer
from fractimation.renderers.sierpinskiCarpetRenderer import SierpinskiCarpetRenderer
from fractimation.renderers.fibonacciSquareRenderer import FibonacciSquareRenderer
from fractimation.renderers.goldenSpiralRenderer import GoldenSpiralRenderer
from fractimation.renderers.newtonFractalRenderer import NewtonFractalRenderer

from fractimation.ui.zoomHandler import ZoomHandler

# General Brot & Julia Fractal Parameters
width, height = 1280, 720                              # Width and Height of the image
                                                       # ^^ quick ref : 480p;(640, 480) 720p;(1280, 720) 1080p;(1920, 1080) UHD/4K;(3840, 2160) 8K;(7680, 4320)
maxIterations = 50                                     # Total number of iterations of fractal equation
                                                       # ^^ Careful with this value; we are caching each frame
colorMap = "viridis"                                   # Any valid color map name or combination (default : viridis)
                                                       # ^^ reference : https://matplotlib.org/examples/color/colormaps_reference.html

# Mandelbrot Set
multibrotWindowMngr = WindowManager(window_title="Multibrot Set", toolbar_visible=False)
multibrotViewer = PlotPlayer(multibrotWindowMngr)
realNumberMin, realNumberMax = -2.0, 0.5               # Min & Max values for X values in fractal equation
imaginaryNumberMin, imaginaryNumberMax = -1.25, 1.25   # Min & Max values for Y values in fractal equation
constantRealNumber, constantImaginaryNumber = 0.0, 0.0 # Initial Z Value
power = 2                                              # Power to raise Z value to for each iteration of fractal equation
escapeValue = 2.0                                      # Limit at which Z values will reach infinity
multibrotFractal = MultibrotRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax, 
                                      constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)
multibrotZoomHandler = ZoomHandler(multibrotFractal, multibrotViewer)
multibrotViewer.initialize(maxIterations, multibrotFractal.render, "multibrotFractal")
multibrotFractal.preheatRenderCache(maxIterations)

# Julia Set
multijuliaWindowMngr = WindowManager(window_title="Julia Set", toolbar_visible=False)
multijuliaViewer = PlotPlayer(multijuliaWindowMngr)
realNumberMin, realNumberMax = -1.5, 1.5               # Min & Max values for X values in fractal equation
imaginaryNumberMin, imaginaryNumberMax = -1.5, 1.5     # Min & Max values for Y values in fractal equation
constantRealNumber, constantImaginaryNumber = 0.0, 0.8 # Constant C value
power = 2                                              # Power to raise Z value to for each iteration of fractal equation
escapeValue = 10.0                                     # Limit at which Z values will reach infinity
multijuliaFractal = MultijuliaRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                                        constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)
multijuliaZoomHandler = ZoomHandler(multijuliaFractal, multijuliaViewer)
multijuliaViewer.initialize(maxIterations, multijuliaFractal.render, "multijuliaFractal")
multijuliaFractal.preheatRenderCache(maxIterations)

# Newton Fractal
newtonFractalWindowMngr = WindowManager(window_title="Newton Fractal", toolbar_visible=False)
newtonFractalViewer = PlotPlayer(newtonFractalWindowMngr)
realNumberMin, realNumberMax = -5, 5                 # Min & Max values for X values in fractal equation
imaginaryNumberMin, imaginaryNumberMax = -5, 5       # Min & Max values for Y values in fractal equation
constantRealNumber, constantImaginaryNumber = 1.0, 0.0 # Constant C value
coefficientArray = [ -1, 0, 0, 0, 1 ]                  # Representation of polynomial equation coefficients in accending order (ie. c + x + x**2 + ... + x**n)
escapeValue = 1e-4
newtonFractal = NewtonFractalRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                                      coefficientArray, constantRealNumber, constantImaginaryNumber, escapeValue, colorMap)
newtonZoomHandler = ZoomHandler(newtonFractal, newtonFractalViewer)
newtonFractalViewer.initialize(maxIterations, newtonFractal.render, "newtonFractal")
newtonFractal.preheatRenderCache(maxIterations)

PlotPlayer.show_players()

# Sierpinski Triangle (3**iteration triangles per iteration)
sierpinskiTriangleWindowMngr = WindowManager(window_title="Sierpinski Triangle")
sierpinskiTriangleViewer = PlotPlayer(sierpinskiTriangleWindowMngr)
sierpinskiTriangleViewer.get_render_manager().set_slider_visible(True)
sierpinskiTriangleIterations = 7                      # Be careful with this number; iterations explode at 3**iteration computations
sierpinskiTriangleLineWidths = numpy.linspace(1.0, 0.1, sierpinskiTriangleIterations + 1)
sierpinskiTriangleFractal = SierpinskiTriangleRenderer(sierpinskiTriangleLineWidths)
sierpinskiTriangleViewer.initialize(sierpinskiTriangleIterations, sierpinskiTriangleFractal.render, "sierpinskiTriangle")
sierpinskiTriangleFractal.preheatRenderCache(sierpinskiTriangleIterations)

# Sierpinski Carpet (8**iteration rectangles per iteration)
sierpinskiCarpetWindowMngr = WindowManager(window_title="Sierpinski Carpet")
sierpinskiCarpetViewer = PlotPlayer(sierpinskiCarpetWindowMngr)
sierpinskiCarpetViewer.get_render_manager().set_slider_visible(True)
sierpinskiCarpetIterations = 4                        # Be careful with this number; iterations explode at 8**iteration computations
sierpinskiCarpetLineWidths = numpy.linspace(1.0, 0.1, sierpinskiCarpetIterations + 1)
sierpinskiCarpetFractal = SierpinskiCarpetRenderer(sierpinskiCarpetLineWidths)
sierpinskiCarpetViewer.initialize(sierpinskiCarpetIterations, sierpinskiCarpetFractal.render,  "sierpinskiCarpet")
sierpinskiCarpetFractal.preheatRenderCache(sierpinskiCarpetIterations)

# Fibonacci Square
fibonacciSquareWindowMngr = WindowManager(window_title="Fibonocci Square")
fibonacciSquareViewer = PlotPlayer(fibonacciSquareWindowMngr)
fibonacciSquareViewer.get_render_manager().set_slider_visible(True)
fibonacciSquareIterations = 15
fibonacciSquareLineWidths = numpy.linspace(0.1, 1.0, fibonacciSquareIterations + 1)
fibonacciSquareFractal = FibonacciSquareRenderer(fibonacciSquareLineWidths)
fibonacciSquareViewer.initialize(fibonacciSquareIterations, fibonacciSquareFractal.render, "fibonocciSquare")
fibonacciSquareFractal.preheatRenderCache(fibonacciSquareIterations)

# Golden Spiral
goldenSpiralWindowMngr = WindowManager(window_title="Golden Spiral")
goldenSpiralViewer = PlotPlayer(goldenSpiralWindowMngr)
goldenSpiralViewer.get_render_manager().set_slider_visible(True)
goldenSpiralIterations = 15
goldenSpiralLineWidths = numpy.linspace(0.01, 0.05, goldenSpiralIterations + 1)
goldenSpiralFractal = GoldenSpiralRenderer(goldenSpiralLineWidths)
goldenSpiralViewer.initialize(goldenSpiralIterations, goldenSpiralFractal.render, "goldenSpiral")
goldenSpiralFractal.preheatRenderCache(goldenSpiralIterations)

# Render Viewers
PlotPlayer.show_players()
