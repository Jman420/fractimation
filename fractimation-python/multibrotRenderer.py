# Algorithm modified from : https://thesamovar.wordpress.com/2009/03/22/fast-fractals-with-python-and-numpy/
# Multibrot Fractal Definitions : C = realNumber + imaginaryNumber
#                                 Z = Z**power + C
#                                 Z0 = complex(constantRealNumber, constantImaginaryNumber) + C

# Mandelbrot Parameters :
#realNumberMin, realNumberMax = -2.0, 0.5
#imaginaryNumberMin, imaginaryNumberMax = -1.25, 1.25
#constantRealNumber, constantImaginaryNumber = 0, 0
#power = 2
#escapeValue = 2.0

import numpy
from fractimationRenderer import fractimationRenderer

class multibrotRenderer(fractimationRenderer):
    """Fractal Renderer for Multibrot Sets"""
    COORDS_CAPTION = "({}, {})"

    _power = _escapeValue = None
    _xIndexes = _yIndexes = None
    _realNumberValues = _imaginaryNumberValues = None
    _zValues = _cValues = None
    _imageArray = _imageCanvas = None
    _colorMap = None
    _currentFrameNumber = _cache = None
    _initialized = False

    def __init__(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap = "viridis"):
        self.initialize(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                       constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)
        self._initialized = False

    def initialize(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                  constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap = "viridis"):
        xIndexes, yIndexes = numpy.mgrid[0:width, 0:height]

        realNumberValues = numpy.linspace(realNumberMin, realNumberMax, width)[xIndexes]
        imaginaryNumberValues = numpy.linspace(imaginaryNumberMin, imaginaryNumberMax, height)[yIndexes]
        cValues = realNumberValues + numpy.complex(0,1) * imaginaryNumberValues
        zValues = numpy.complex(constantRealNumber, constantImaginaryNumber) + cValues
        imageArray = numpy.zeros(cValues.shape, dtype=int) - 1
        
        self._power = power
        self._escapeValue = escapeValue
        self._xIndexes = xIndexes
        self._yIndexes = yIndexes
        self._realNumberValues = realNumberValues
        self._imaginaryNumberValues = imaginaryNumberValues
        self._zValues = zValues
        self._cValues = cValues
        self._imageArray = imageArray
        self._colorMap = colorMap
        self._cache = { }
        self._currentFrameNumber = 0

    def renderZoomCaption(self, axes):
        if (self._renderZoomBox):
            startX, startY = self.getMinZoomCoords()
            endX, endY = self.getMaxZoomCoords()
            
            minRealNumber = self._realNumberValues[startX][startY]
            minImaginaryNumber = self._imaginaryNumberValues[startX][startY]
            minValuesCaption = self.COORDS_CAPTION.format(minRealNumber, minImaginaryNumber)
            axes.text(startX, startY, minValuesCaption, fontsize=8)

            maxRealNumber = self._imaginaryNumberValues[endX][endY]
            maxImaginaryNumber = self._imaginaryNumberValues[endX][endY]
            maxValuesCaption = self.COORDS_CAPTION.format(maxRealNumber, maxImaginaryNumber)
            axes.text(endX, endY, maxValuesCaption, fontsize=8)

    def render(self, frameNumber, axes):
        if frameNumber in self._cache:
            self._imageCanvas.set_data(self._cache[frameNumber])
            self._imageCanvas.autoscale()

            self.renderZoomCaption(axes)
            return

        finalImage = None
        for frameCounter in range(self._currentFrameNumber, frameNumber + 1):
            if len(self._zValues) <= 0:
                # Nothing left to calculate, so just store the last image in the cache
                finalImage = self._cache[len(self._cache) - 1]
                self._cache.update({ frameCounter : finalImage })
            else:
                exponentValue = numpy.copy(self._zValues)
                for exponentCounter in range(0, self._power - 1):
                    numpy.multiply(exponentValue, self._zValues, self._zValues)

                numpy.add(self._zValues, self._cValues, self._zValues)

                remainingIndexes = numpy.abs(self._zValues) > self._escapeValue
                self._imageArray[self._xIndexes[remainingIndexes], self._yIndexes[remainingIndexes]] = frameCounter

                removableIndexes = ~remainingIndexes
                self._xIndexes, self._yIndexes = self._xIndexes[removableIndexes], self._yIndexes[removableIndexes]
                self._zValues = self._zValues[removableIndexes]
                self._cValues = self._cValues[removableIndexes]

                recoloredImage = numpy.copy(self._imageArray)
                recoloredImage[recoloredImage == -1] = frameCounter + 1
                finalImage = recoloredImage.T
                self._cache.update({ frameCounter : finalImage })
        
        self._currentFrameNumber = frameCounter + 1
        if (self._initialized):
            self._imageCanvas.set_data(finalImage)
            self._imageCanvas.autoscale()
        else:
            self._imageCanvas = axes.imshow(finalImage, cmap=self._colorMap)
            self._initialized = True

        self.renderZoomCaption(axes)
        super().render(frameNumber, axes)