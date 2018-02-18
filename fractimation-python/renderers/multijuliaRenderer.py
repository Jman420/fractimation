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

from .base.imageRenderer import ImageRenderer

class MultijuliaRenderer(ImageRenderer):
    """Fractal Renderer for Multi-Julia Sets"""

    _width = _height = None
    _constantRealNumber = _constantImaginaryNumber = None
    _power = _escapeValue = None
    _minRealNumber = _maxRealNumber = None
    _minImaginaryNumber = _maxImaginaryNumber = None

    _xIndexes = _yIndexes = None
    _realNumberValues = _imaginaryNumberValues = None
    _zValues = _cValue = None

    _imageArray = None
    _colorMap = _zoomCache = None

    def __init__(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax, 
                 constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap = "viridis"):
        self._zoomCache = [ ]

        self.initialize(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                       constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)

    def initialize(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                  constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap = "viridis"):
        # Prepare Image Location Indexes included for calculation
        xIndexes, yIndexes = numpy.mgrid[0:width, 0:height]

        # Calculate C Value and Initial Z Values
        realNumberValues = numpy.linspace(realNumberMin, realNumberMax, width)[xIndexes]
        imaginaryNumberValues = numpy.linspace(imaginaryNumberMin, imaginaryNumberMax, height)[yIndexes]
        cValue = numpy.complex(constantRealNumber, constantImaginaryNumber)

        zValues = numpy.multiply(numpy.complex(0,1), imaginaryNumberValues)
        zValues = numpy.add(zValues, realNumberValues)

        # Initialize Image Array
        imageArray = numpy.zeros(zValues.shape, dtype=int)
        imageArray = numpy.add(imageArray, -1)
        
        self._width = width
        self._height = height
        self._constantRealNumber = constantRealNumber
        self._constantImaginaryNumber = constantImaginaryNumber
        self._power = power
        self._escapeValue = escapeValue
        self._minRealNumber = realNumberMin
        self._maxRealNumber = realNumberMax
        self._minImaginaryNumber = imaginaryNumberMin
        self._maxImaginaryNumber = imaginaryNumberMax

        self._xIndexes = xIndexes
        self._yIndexes = yIndexes
        self._realNumberValues = realNumberValues
        self._imaginaryNumberValues = imaginaryNumberValues
        self._zValues = zValues
        self._cValue = cValue
        self._imageArray = imageArray
        self._colorMap = colorMap
        
        super().initialize()

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

    def zoomIn(self, startX, startY, endX, endY):
        prevZoom = zoomCacheItem(self._minRealNumber, self._maxRealNumber, self._minImaginaryNumber, self._maxImaginaryNumber)

        minRealNumber = self._realNumberValues[startX][startY]
        maxRealNumber = self._realNumberValues[endX][endY]
        minImaginaryNumber = self._imaginaryNumberValues[startX][startY]
        maxImaginaryNumber = self._imaginaryNumberValues[endX][endY]
        print("ZoomIn Parameters (minReal, maxReal) -> (minImaginary, maxImaginary) : ({}, {}) -> ({}, {})"
              .format(minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber))

        self.initialize(self._width, self._height, minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber,
                        self._constantRealNumber, self._constantImaginaryNumber, self._power, self._escapeValue, self._colorMap)
        self._zoomCache.append(prevZoom)

    def zoomOut(self):
        if len(self._zoomCache) < 1:
            return False

        prevZoom = self._zoomCache.pop()
        print("ZoomOut Parameters (minReal, maxReal) -> (minImaginary, maxImaginary) : ({}, {}) -> ({}, {})"
              .format(prevZoom.minRealNumber, prevZoom.maxRealNumber, prevZoom.minImaginaryNumber, prevZoom.maxImaginaryNumber))

        self.initialize(self._width, self._height, prevZoom.minRealNumber, prevZoom.maxRealNumber, prevZoom.minImaginaryNumber,
                       prevZoom.maxImaginaryNumber, self._constantRealNumber, self._constantImaginaryNumber, self._power,
                       self._escapeValue, self._colorMap)
        return True

class zoomCacheItem(object):
    minRealNumber = maxRealNumber = None
    minImaginaryNumber = maxImaginaryNumber = None

    def __init__(self, minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber):
        self.minRealNumber = minRealNumber
        self.maxRealNumber = maxRealNumber
        self.minImaginaryNumber = minImaginaryNumber
        self.maxImaginaryNumber = maxImaginaryNumber