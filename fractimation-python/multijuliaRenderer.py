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

from numpy import *

class multijuliaRenderer(object):
    """Fractal Renderer for Multi-Julia Sets"""

    _power = _escapeValue = None
    _xIndexes = _yIndexes = None
    _zValues = _cValues = None
    _imageArray = _canvas = None
    _prevFrameNumber = _cache = None
    _initialized = False

    def __init__(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax, 
                 constantRealNumber, constantImaginaryNumber, power, escapeValue):
        self.initialize(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                       constantRealNumber, constantImaginaryNumber, power, escapeValue)
        self._initialized = False

    def initialize(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                  constantRealNumber, constantImaginaryNumber, power, escapeValue):
        xIndexes, yIndexes = mgrid[0:width, 0:height]

        realNumberValues = linspace(realNumberMin, realNumberMax, width)[xIndexes]
        imaginaryNumberValues = linspace(imaginaryNumberMin, imaginaryNumberMax, height)[yIndexes]
        zValues = realNumberValues + complex(0,1) * imaginaryNumberValues
        del realNumberValues, imaginaryNumberValues

        cValues = complex(constantRealNumber, constantImaginaryNumber)
        imageArray = zeros(zValues.shape, dtype=int) - 1
        
        self._power = power
        self._escapeValue = escapeValue
        self._xIndexes = xIndexes
        self._yIndexes = yIndexes
        self._zValues = zValues
        self._cValues = cValues
        self._imageArray = imageArray
        self._cache = { }
        self._prevFrameNumber = 0

    def render(self, frameNumber, axes):
        if frameNumber in self._cache:
            self._canvas.set_data(self._cache[frameNumber])
            self._canvas.autoscale()
            return

        finalImage = None
        for frameCounter in range(self._prevFrameNumber, frameNumber + 1):
            if len(self._zValues) <= 0:
                # Nothing left to calculate, so just store the last image in the cache
                finalImage = self._cache[len(self._cache) - 1]
                self._cache.update({ frameCounter : finalImage })
            else:
                exponentValue = copy(self._zValues)
                for exponentCounter in range(0, self._power - 1):
                    multiply(exponentValue, self._zValues, self._zValues)

                add(self._zValues, self._cValues, self._zValues)

                remainingIndexes = abs(self._zValues) > self._escapeValue
                self._imageArray[self._xIndexes[remainingIndexes], self._yIndexes[remainingIndexes]] = frameCounter

                removableIndexes = ~remainingIndexes
                self._xIndexes, self._yIndexes = self._xIndexes[removableIndexes], self._yIndexes[removableIndexes]
                self._zValues = self._zValues[removableIndexes]

                recoloredImage = copy(self._imageArray)
                recoloredImage[recoloredImage == -1] = frameCounter + 1
                finalImage = recoloredImage.T
                self._cache.update({ frameCounter : finalImage })
        
        self._prevFrameNumber = frameCounter + 1
        if (self._initialized):
            self._canvas.set_data(finalImage)
            self._canvas.autoscale()
        else:
            self._canvas = axes.imshow(finalImage)
            self._initialized = True