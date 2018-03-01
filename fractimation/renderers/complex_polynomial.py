import numpy

from .base.cached_image_renderer import CachedImageRenderer
from .functionality.zoomable_complex_range import ZoomableComplexRange
from ..helpers.fractal_algorithm import evaluate_polynomial_1d
from ..helpers.list_tools import update_indexes_with_value, remove_indexes

class ComplexPolynomial(CachedImageRenderer, ZoomableComplexRange):
    """Fractal Renderer for Generic Complex Polynomial Equations"""

    _constantRealNumber = _constantImaginaryNumber = None
    _coefficientArray = _escapeValue = None

    _zValues = _cValue = None

    def __init__(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                 coefficientArray, constantRealNumber, constantImaginaryNumber, escapeValue, colorMap = "viridis"):
        CachedImageRenderer.__init__(self)
        ZoomableComplexRange.__init__(self)

        self.initialize(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                        coefficientArray, constantRealNumber, constantImaginaryNumber, escapeValue, colorMap)

    def initialize(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                   coefficientArray, constantRealNumber, constantImaginaryNumber, escapeValue, colorMap = "viridis"):
        # Setup Included Indexes and the Real and Imaginary Number Spaces
        ZoomableComplexRange.initialize(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin,
                                       imaginaryNumberMax)

        # Calculate C Value and Initial Z Values
        cValue = numpy.complex(constantRealNumber, constantImaginaryNumber)

        zValues = numpy.multiply(numpy.complex(0,1), self._imaginaryNumberValues)
        zValues = numpy.add(zValues, self._realNumberValues)

        self._zValues = zValues
        self._cValue = cValue

        # Initialize Image Cache
        CachedImageRenderer.initialize(self, width, height, zValues.shape, colorMap)
        
        self._constantRealNumber = constantRealNumber
        self._constantImaginaryNumber = constantImaginaryNumber
        self._coefficientArray = coefficientArray
        self._escapeValue = escapeValue
        
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
        zValuesNew = evaluate_polynomial_1d(self._coefficientArray, self._zValues, self._cValue)

        # Update indexes which have exceeded the Escape Value
        explodedIndexes = numpy.abs(zValuesNew) > self._escapeValue
        self._imageArray[self._xIndexes[explodedIndexes], self._yIndexes[explodedIndexes]] = self._nextIterationIndex

        # Recolor Indexes which have not exceeded the Escape Value
        recoloredImage = update_indexes_with_value(self._imageArray, -1, self._nextIterationIndex + 1)
        finalImage = recoloredImage.T

        # Update cache and prepare for next iteration
        self._renderCache.update({ self._nextIterationIndex : finalImage })
        self._nextIterationIndex += 1

        # Remove Exploded Indexes since we don't need to calculate them anymore
        remainingIndexes = ~explodedIndexes
        self._xIndexes, self._yIndexes, self._zValues = remove_indexes([ self._xIndexes, self._yIndexes, zValuesNew ],
                                                                     remainingIndexes)