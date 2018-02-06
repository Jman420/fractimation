from numpy import *

class mandelbrot_videofig(object):
    """Fractal Renderer for Mandelbrot Set"""

    _escapeValue = None
    _xIndexes = _yIndexes = None
    _zValues = _cValues = None
    _imageArray = _render = None
    _cache = None
    _initialized = False

    def __init__(self, width, height, xMin, xMax, yMin, yMax, escapeValue):
        xIndexes, yIndexes = mgrid[0:width, 0:height]

        xValues = linspace(xMin, xMax, width)[xIndexes]
        yValues = linspace(yMin, yMax, height)[yIndexes]
        cValues = xValues + complex(0,1) * yValues
        zValues = copy(cValues)
        imageArray = zeros(cValues.shape, dtype=int)
        del xValues, yValues

        self._escapeValue = escapeValue
        self._xIndexes = xIndexes
        self._yIndexes = yIndexes
        self._zValues = zValues
        self._cValues = cValues
        self._imageArray = imageArray
        self._initialized = False

    def iterate(self, frameNumber, axes):
        if not len(self._zValues):
            return

        multiply(self._zValues, self._zValues, self._zValues)
        add(self._zValues, self._cValues, self._zValues)

        remainingIndexes = abs(self._zValues) > self._escapeValue
        self._imageArray[self._xIndexes[remainingIndexes], self._yIndexes[remainingIndexes]] = frameNumber

        removableIndexes = ~remainingIndexes
        self._xIndexes, self._yIndexes = self._xIndexes[removableIndexes], self._yIndexes[removableIndexes]
        self._zValues = self._zValues[removableIndexes]
        self._cValues = self._cValues[removableIndexes]
        
        if (self._initialized):
            self._render.set_data(self._imageArray.T)
            self._render.autoscale()
        else:
            self._render = axes.imshow(self._imageArray.T, origin='lower left')
            self._initialized = True