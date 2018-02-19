import numpy

from .base.cachedImageRenderer import CachedImageRenderer
from .base.zoomableComplexPolynomialRenderer import ZoomableComplexPolynomialRenderer
from helpers.fractalAlgorithmHelper import evaluatePolynomial1D
from helpers.renderHelper import recolorUnexplodedIndexes
from helpers.fractalAlgorithmHelper import removeIndexes

class ComplexPolynomialRenderer(CachedImageRenderer, ZoomableComplexPolynomialRenderer):
    """Fractal Renderer for Generic Complex Polynomial Equations"""

    _width = _height = None
    _constantRealNumber = _constantImaginaryNumber = None
    _coefficientArray = _escapeValue = None

    _xIndexes = _yIndexes = None
    _zValues = _cValue = None

    _imageArray = None

    def __init__(self, width, height, minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber,
                 coefficientArray, constantRealNumber, constantImaginaryNumber, escapeValue, colorMap = "viridis"):
        super().__init__()

        self.initialize(width, height, minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber,
                        coefficientArray, constantRealNumber, constantImaginaryNumber, escapeValue, colorMap)

    def initialize(self, width, height, minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber,
                   coefficientArray, constantRealNumber, constantImaginaryNumber, escapeValue, colorMap = "viridis"):
        # Prepare Image Location Indexes included for calculation
        xIndexes, yIndexes = numpy.mgrid[0:width, 0:height]

        # Setup Real and Imaginary Number Spaces
        ZoomableComplexPolynomialRenderer.initialize(self, xIndexes, yIndexes, width, height, minRealNumber,
                                                    maxRealNumber, minImaginaryNumber, maxImaginaryNumber)

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
        self._coefficientArray = coefficientArray
        self._escapeValue = escapeValue

        self._xIndexes = xIndexes
        self._yIndexes = yIndexes
        self._zValues = zValues
        self._cValue = cValue
        self._imageArray = imageArray
        
    def reinitialize(self):
        self.initialize(self._width, self._height, self._minRealNumber, self._maxRealNumber, self._minImaginaryNumber,
                       self._maxImaginaryNumber, self._coefficientArray, self._constantRealNumber, self._constantImaginaryNumber,
                       self._escapeValue, self._colorMap)

    def preheatRenderCache(self, maxIterations):
        print("Preheating Generic Complex Polynomial Render Cache")
        super().preheatRenderCache(maxIterations)

    def iterate(self):
        if len(self._zValues) <= 0:
            # Nothing left to calculate, so just store the last image in the cache
            finalImage = self._renderCache[len(self._renderCache) - 1]
            self._renderCache.update({ self._nextIterationIndex : finalImage })
            self._nextIterationIndex += 1
            return

        # Evaluate Polynomial
        zValuesNew = evaluatePolynomial1D(self._coefficientArray, self._zValues, self._cValue)

        # Update indexes which have exceeded the Escape Value
        explodedIndexes = numpy.abs(zValuesNew) > self._escapeValue
        self._imageArray[self._xIndexes[explodedIndexes], self._yIndexes[explodedIndexes]] = self._nextIterationIndex

        # Recolor Indexes which have not exceeded the Escape Value
        recoloredImage = recolorUnexplodedIndexes(self._imageArray, -1, self._nextIterationIndex + 1)
        finalImage = recoloredImage.T

        # Update cache and prepare for next iteration
        self._renderCache.update({ self._nextIterationIndex : finalImage })
        self._nextIterationIndex += 1

        # Remove Exploded Indexes since we don't need to calculate them anymore
        remainingIndexes = ~explodedIndexes
        self._xIndexes, self._yIndexes, self._zValues = removeIndexes([ self._xIndexes, self._yIndexes, zValuesNew ],
                                                                     remainingIndexes)