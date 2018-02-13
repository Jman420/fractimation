# Algorithm modified from : https://thesamovar.wordpress.com/2009/03/22/fast-fractals-with-python-and-numpy/
#                           http://www.relativitybook.com/CoolStuff/julia_set.html
# Multi-Julia Fractal Definitions : C = complex(constantRealNumber, constantImaginaryNumber)
#                                   Z = Z**power + C
#                                   Z0 = realNumber + imaginaryNumber

# Julia Set Parameters
#realNumberMin, realNumberMax = -1.5, 1.5
#imaginaryNumberMin, imaginaryNumberMax = -1.5, 1.5
#constantRealNumber, constantImaginaryNumber = any values between -1 and 1
#power = 2
#escapeValue = 10.0

import numpy

class multijuliaRenderer(object):
    """Fractal Renderer for Multi-Julia Sets"""

    _width = _height = None
    _constantRealNumber = _constantImaginaryNumber = None
    _power = _escapeValue = None
    _minRealNumber = _maxRealNumber = None
    _minImaginaryNumber = _maxImaginaryNumber = None

    _xIndexes = _yIndexes = None
    _realNumberValues = _imaginaryNumberValues = None
    _zValues = _cValue = None

    _imageArray = _imageCanvas = None
    _colorMap = _nextIterationIndex = None
    _imageCache = _zoomCache = None

    def __init__(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax, 
                 constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap = "viridis"):
        self._zoomCache = [ ]

        self.initialize(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                       constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)

    def initialize(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                  constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap = "viridis"):
        xIndexes, yIndexes = numpy.mgrid[0:width, 0:height]

        realNumberValues = numpy.linspace(realNumberMin, realNumberMax, width)[xIndexes]
        imaginaryNumberValues = numpy.linspace(imaginaryNumberMin, imaginaryNumberMax, height)[yIndexes]
        zValues = realNumberValues + numpy.complex(0,1) * imaginaryNumberValues
        cValue = numpy.complex(constantRealNumber, constantImaginaryNumber)
        imageArray = numpy.zeros(zValues.shape, dtype=int) - 1
        
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
        self._imageCache = { }
        self._nextIterationIndex = 0

    def preheatCache(self, maxIterations):
        if maxIterations < len(self._imageCache):
            return

        print("Preheating Multijulia Cache to {} iterations...".format(maxIterations))
        for iterationCounter in range(len(self._imageCache), maxIterations):
            print("Multijulia iteration {} processing...".format(iterationCounter))
            self.iterate()

        print("Completed preheating Multijulia cache!")

    def iterate(self):
        exponentValue = numpy.copy(self._zValues)
        for exponentCounter in range(0, self._power - 1):
            numpy.multiply(exponentValue, self._zValues, self._zValues)

        numpy.add(self._zValues, self._cValue, self._zValues)

        explodedIndexes = numpy.abs(self._zValues) > self._escapeValue
        self._imageArray[self._xIndexes[explodedIndexes], self._yIndexes[explodedIndexes]] = self._nextIterationIndex

        remainingIndexes = ~explodedIndexes
        self._xIndexes, self._yIndexes = self._xIndexes[remainingIndexes], self._yIndexes[remainingIndexes]
        self._zValues = self._zValues[remainingIndexes]

        recoloredImage = numpy.copy(self._imageArray)
        recoloredImage[recoloredImage == -1] = self._nextIterationIndex + 1
        finalImage = recoloredImage.T
        self._imageCache.update({ self._nextIterationIndex : finalImage })
        self._nextIterationIndex += 1

    def render(self, frameNumber, axes):
        if frameNumber in self._imageCache:
            self._imageCanvas.set_data(self._imageCache[frameNumber])
            self._imageCanvas.autoscale()
            return

        finalImage = None
        for frameCounter in range(self._nextIterationIndex, frameNumber + 1):
            if len(self._zValues) <= 0:
                # Nothing left to calculate, so just store the last image in the cache
                finalImage = self._imageCache[len(self._imageCache) - 1]
                self._imageCache.update({ frameCounter : finalImage })
            else:
                self.iterate()
                finalImage = self._imageCache[frameCounter]

        if self._imageCanvas == None:
            self._imageCanvas = axes.imshow(finalImage, cmap=self._colorMap, origin="upper")
        else:
            self._imageCanvas.set_data(finalImage)
            self._imageCanvas.autoscale()

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