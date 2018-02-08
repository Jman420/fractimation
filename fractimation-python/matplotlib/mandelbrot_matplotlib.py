# Algorithm modified from : https://thesamovar.wordpress.com/2009/03/22/fast-fractals-with-python-and-numpy/
#    - Further optimized algorithm is within comments; includes ability to calculate multiple iterations in a single calculation

from numpy import *

class mandelbrot_matplotlib(object):
    """Fractal Renderer for Mandelbrot Set"""

    _escapeValue = None
    _xIndexes = _yIndexes = None
    _zValues = _cValues = None
    _imageArray = None

    def __init__(self, width, height, xMin, xMax, yMin, yMax, escapeValue):
        self.initialize(width, height, xMin, xMax, yMin, yMax, escapeValue)
        self._initialized = False

    def initialize(self, width, height, xMin, xMax, yMin, yMax, escapeValue):
        xIndexes, yIndexes = mgrid[0:width, 0:height]

        xValues = linspace(xMin, xMax, width)[xIndexes]
        yValues = linspace(yMin, yMax, height)[yIndexes]
        cValues = xValues + complex(0,1) * yValues
        zValues = copy(cValues)
        imageArray = zeros(cValues.shape, dtype=int) - 1
        del xValues, yValues

        self._escapeValue = escapeValue
        self._xIndexes = xIndexes
        self._yIndexes = yIndexes
        self._zValues = zValues
        self._cValues = cValues
        self._imageArray = imageArray

    def iterate(self, frameNumber):
        if len(self._zValues) <= 0:
            render = canvas.imshow(self._imageArray.T, origin='lower left')
            return render

        multiply(self._zValues, self._zValues, self._zValues)
        add(self._zValues, self._cValues, self._zValues)

        remainingIndexes = abs(self._zValues) > self._escapeValue
        self._imageArray[self._xIndexes[remainingIndexes], self._yIndexes[remainingIndexes]] = frameNumber + 1

        removableIndexes = ~remainingIndexes
        self._xIndexes, self._yIndexes = self._xIndexes[removableIndexes], self._yIndexes[removableIndexes]
        self._zValues = self._zValues[removableIndexes]
        self._cValues = self._cValues[removableIndexes]

        recoloredImage = copy(self._imageArray)
        recoloredImage[recoloredImage == -1] = frameNumber + 1

        return recoloredImage.T