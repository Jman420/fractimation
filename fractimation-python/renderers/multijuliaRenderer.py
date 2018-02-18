# Algorithm modified from : https://thesamovar.wordpress.com/2009/03/22/fast-fractals-with-python-and-numpy/
#                           http://www.relativitybook.com/CoolStuff/julia_set.html
# Multi-Julia Fractal Definitions :
#  C = complex(constantRealNumber, constantImaginaryNumber)
#  Z = Z**power + C
#  Z0 = realNumber + imaginaryNumber
# Multi-Julia Rendering Instructions :
#   - Map range of real and imaginary number values evenly to the image x and y pixel coordinates
#   - For each iteration 
#     * For each unexploded pixel in the image
#       @ Retrieve associated real and imaginary number values for pixel coordinates
#       @ Perform provided Multi-Julia equation variant
#       @ Set pixel value equal to number of iterations for Z to exceed the Escape Value
#     * Remove exploded pixel coordinates from calculation indexes

# Julia Set Parameters
#realNumberMin, realNumberMax = -1.5, 1.5
#imaginaryNumberMin, imaginaryNumberMax = -1.5, 1.5
#constantRealNumber, constantImaginaryNumber = any values between -1 and 1
#power = 2
#escapeValue = 10.0

import numpy

from .base.cachedImageRenderer import CachedImageRenderer
from .base.zoomableComplexPolynomialRenderer import ZoomableComplexPolynomialRenderer

DEFAULT_COLOR_MAP = "viridis"

class MultijuliaRenderer(CachedImageRenderer, ZoomableComplexPolynomialRenderer):
    """Fractal Renderer for Multi-Julia Sets"""

    _width = _height = None
    _constantRealNumber = _constantImaginaryNumber = None
    _power = _escapeValue = None

    _xIndexes = _yIndexes = None
    _zValues = _cValue = None

    _imageArray = None

    def __init__(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax, 
                 constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap = DEFAULT_COLOR_MAP):
        self._zoomCache = [ ]

        self.initialize(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                       constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)

    def initialize(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                  constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap = DEFAULT_COLOR_MAP):
        # Prepare Image Location Indexes included for calculation
        xIndexes, yIndexes = numpy.mgrid[0:width, 0:height]

        # Setup Real and Imaginary Number Spaces
        ZoomableComplexPolynomialRenderer.initialize(self, xIndexes, yIndexes, width, height, realNumberMin,
                                                    realNumberMax, imaginaryNumberMin, imaginaryNumberMax)

        # Calculate C Value and Initial Z Values
        cValue = numpy.complex(constantRealNumber, constantImaginaryNumber)

        zValues = numpy.multiply(numpy.complex(0,1), self._imaginaryNumberValues)
        zValues = numpy.add(zValues, self._realNumberValues)

        # Initialize Image Array
        imageArray = numpy.zeros(zValues.shape, dtype=int)
        imageArray = numpy.add(imageArray, -1)

        # Initialize Image Cache
        CachedImageRenderer.initialize(self, colorMap)
        
        self._width = width
        self._height = height
        self._constantRealNumber = constantRealNumber
        self._constantImaginaryNumber = constantImaginaryNumber
        self._power = power
        self._escapeValue = escapeValue

        self._xIndexes = xIndexes
        self._yIndexes = yIndexes
        self._zValues = zValues
        self._cValue = cValue
        self._imageArray = imageArray

    def reinitialize(self):
        self.initialize(self._width, self._height, self._minRealNumber, self._maxRealNumber, self._minImaginaryNumber,
                       self._maxImaginaryNumber, self._constantRealNumber, self._constantImaginaryNumber, self._power,
                       self._escapeValue, self._colorMap)

    def preheatRenderCache(self, maxIterations):
        print("Preheating Multi-Julia Render Cache")
        super().preheatRenderCache(maxIterations)

    def iterate(self):
        if len(self._zValues) <= 0:
            # Nothing left to calculate, so just store the last image in the cache
            finalImage = self._renderCache[len(self._renderCache) - 1]
            self._renderCache.update({ self._nextIterationIndex : finalImage })
            self._nextIterationIndex += 1
            return

        # Calculate exponent piece of Multijulia Equation
        zValuesNew = numpy.copy(self._zValues)
        exponentValue = numpy.copy(self._zValues)
        for exponentCounter in range(0, self._power - 1):
            numpy.multiply(exponentValue, zValuesNew, zValuesNew)

        # Add C piece of Multijulia Equation
        numpy.add(zValuesNew, self._cValue, zValuesNew)

        # Get update indexes which have exceeded the Escape Value
        explodedIndexes = numpy.abs(zValuesNew) > self._escapeValue
        self._imageArray[self._xIndexes[explodedIndexes], self._yIndexes[explodedIndexes]] = self._nextIterationIndex

        # Recolor Indexes which have not exceeded the Escape Value
        recoloredImage = numpy.copy(self._imageArray)
        recoloredImage[recoloredImage == -1] = self._nextIterationIndex + 1
        finalImage = recoloredImage.T

        # Update cache and prepare for next iteration
        self._renderCache.update({ self._nextIterationIndex : finalImage })
        self._nextIterationIndex += 1

        # Remove Exploded Indexes since we don't need to calculate them anymore
        remainingIndexes = ~explodedIndexes
        self._xIndexes, self._yIndexes = self._xIndexes[remainingIndexes], self._yIndexes[remainingIndexes]
        self._zValues = zValuesNew[remainingIndexes]