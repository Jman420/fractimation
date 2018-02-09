import videofig
import matplotlib.pylab as pylab

import multibrotRenderer as multibrot
import multijuliaRenderer as multijulia
import uiHandler

width, height = 1280, 720                              # Width and Height of the image
                                                       # ^^ quick ref : 480p;(640, 480) 720p;(1280, 720) 1080p;(1920, 1080) UHD/4K;(3840, 2160) 8K;(7680, 4320)
maxIterations = 50                                     # Total number of iterations of fractal equation
                                                       #  ^^ Careful with this value; we are caching each frame
colorMap = "viridis"                                   # Any valid color map name or combination (default : viridis)
                                                       # ^^ reference : https://matplotlib.org/examples/color/colormaps_reference.html

# Mandelbrot Set
realNumberMin, realNumberMax = -2.0, 0.5               # Min & Max values for X values in fractal equation
imaginaryNumberMin, imaginaryNumberMax = -1.25, 1.25   # Min & Max values for Y values in fractal equation
constantRealNumber, constantImaginaryNumber = 0.0, 0.0 # Needs some experimentation in Mandelbrot Set (non-standard)
power = 2                                              # Power to raise Z value to for each iteration of fractal equation
escapeValue = 2.0                                      # Limit at which Z values will reach infinity
multibrotRenderer = multibrot.multibrotRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                                                constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)

multibrotFigure = pylab.plt.figure()
mandelbrotViewer = videofig.videofig("Mandelbrot Set", multibrotFigure)
mandelbrotViewer.initializeAnimation(maxIterations, multibrotRenderer.render)

#multibrotUiHandler = uiHandler.uiHandler(multibrotRenderer, mandelbrotViewer)
#multibrotFigure.canvas.mpl_connect("button_press_event", multibrotUiHandler.imageMouseButtonPress)
#multibrotFigure.canvas.mpl_connect("button_release_event", multibrotUiHandler.imageMouseButtonRelease)
#multibrotFigure.canvas.mpl_connect("motion_notify_event", multibrotUiHandler.imageMouseMotion)

mandelbrotViewer.play()
mandelbrotViewer.show(False)

# Julia Set
realNumberMin, realNumberMax = -1.5, 1.5
imaginaryNumberMin, imaginaryNumberMax = -1.5, 1.5
constantRealNumber, constantImaginaryNumber = 0.0, 0.8 # Constant C value for Julia Set
power = 2
escapeValue = 10.0
multijuliaRenderer = multijulia.multijuliaRenderer(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                                                   constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)
juliaViewer = videofig.videofig("Julia Set")
juliaViewer.initializeAnimation(maxIterations, multijuliaRenderer.render)

juliaViewer.play()

juliaViewer.show(True)