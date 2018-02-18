from abc import ABC, abstractmethod
import numpy

from .fractimationRenderer import FractimationRenderer

class ZoomableComplexPolynomialRenderer(FractimationRenderer, ABC):
    """Base Class for Zoomable Complex Polynomial Fractal Equation Renderers"""

    _minRealNumber = _maxRealNumber = None
    _minImaginaryNumber = _maxImaginaryNumber = None
    _realNumberValues = _imaginaryNumberValues = None

    _zoomCache = None

    def __init__(self):
        _zoomCache = [ ]

    def initialize(self, xIndexes, yIndexes, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax, spacingFunc=numpy.linspace):
        super().initialize()

        realNumberValues = spacingFunc(realNumberMin, realNumberMax, width)[xIndexes]
        imaginaryNumberValues = spacingFunc(imaginaryNumberMin, imaginaryNumberMax, height)[yIndexes]

        self._minRealNumber = realNumberMin
        self._maxRealNumber = realNumberMax
        self._minImaginaryNumber = imaginaryNumberMin
        self._maxImaginaryNumber = imaginaryNumberMax
        self._realNumberValues = realNumberValues
        self._imaginaryNumberValues = imaginaryNumberValues

    def zoomIn(self, startX, startY, endX, endY):
        prevZoom = zoomCacheItem(self._minRealNumber, self._maxRealNumber, self._minImaginaryNumber, self._maxImaginaryNumber)

        minRealNumber = self._realNumberValues[startX][startY]
        maxRealNumber = self._realNumberValues[endX][endY]
        minImaginaryNumber = self._imaginaryNumberValues[startX][startY]
        maxImaginaryNumber = self._imaginaryNumberValues[endX][endY]
        print("ZoomIn Parameters (minReal, maxReal) -> (minImaginary, maxImaginary) : ({}, {}) -> ({}, {})"
              .format(minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber))

        self._minRealNumber = minRealNumber
        self._maxRealNumber = maxRealNumber
        self._minImaginaryNumber = minImaginaryNumber
        self._maxImaginaryNumber = maxImaginaryNumber

        self.reinitialize()
        self._zoomCache.append(prevZoom)

    def zoomOut(self):
        if len(self._zoomCache) < 1:
            return False

        prevZoom = self._zoomCache.pop()
        print("ZoomOut Parameters (minReal, maxReal) -> (minImaginary, maxImaginary) : ({}, {}) -> ({}, {})"
              .format(prevZoom.minRealNumber, prevZoom.maxRealNumber, prevZoom.minImaginaryNumber, prevZoom.maxImaginaryNumber))

        self._minRealNumber = prevZoom.minRealNumber
        self._maxRealNumber = prevZoom.maxRealNumber
        self._minImaginaryNumber = prevZoom.minImaginaryNumber
        self._maxImaginaryNumber = prevZoom.maxImaginaryNumber

        self.reinitialize()
        return True

    @abstractmethod
    def reinitialize(self):
        pass

class zoomCacheItem(object):
    minRealNumber = maxRealNumber = None
    minImaginaryNumber = maxImaginaryNumber = None

    def __init__(self, minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber):
        self.minRealNumber = minRealNumber
        self.maxRealNumber = maxRealNumber
        self.minImaginaryNumber = minImaginaryNumber
        self.maxImaginaryNumber = maxImaginaryNumber