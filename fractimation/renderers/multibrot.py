# Algorithm modified from : https://thesamovar.wordpress.com/2009/03/22/fast-fractals-with-python-and-numpy/
# Multibrot Fractal Definitions : 
#   C = realNumber + imaginaryNumber
#   Z = Z**power + C
#   Z0 = complex(initialRealNumber, initialImaginaryNumber) + C
# Multibrot Rendering Instructions :
#   - Map range of real and imaginary number values evenly to the image x and y pixel coordinates
#   - For each iteration 
#     * For each unexploded pixel in the image
#       @ Retrieve associated real and imaginary number values for pixel coordinates
#       @ Perform provided Multibrot equation variant
#       @ Set pixel value equal to number of iterations for Z to exceed the Escape Value
#     * Remove exploded pixel coordinates from calculation indexes

# Mandelbrot Parameters :
#realNumberMin, realNumberMax = -2.0, 0.5
#imaginaryNumberMin, imaginaryNumberMax = -1.25, 1.25
#constantRealNumber, constantImaginaryNumber = 0, 0
#power = 2
#escapeValue = 2.0

import numpy

from .base.cachedImageRenderer import CachedImageRenderer
from .functionality.zoomableComplexRange import ZoomableComplexRange
from ..helpers.fractalAlgorithm import removeIndexes, multibrotAlgorithm
from ..helpers.render import recolorUnexplodedIndexes

DEFAULT_COLOR_MAP = "viridis"

class Multibrot(CachedImageRenderer, ZoomableComplexRange):
    """Fractal Renderer for Multibrot Sets"""

    _initialRealNumber = _initialImaginaryNumber = None
    _power = _escapeValue = None

    _zValues = _cValues = None

    def __init__(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                initialRealNumber, initialImaginaryNumber, power, escapeValue, colorMap = DEFAULT_COLOR_MAP):
        CachedImageRenderer.__init__(self)
        ZoomableComplexRange.__init__(self)

        self.initialize(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                       initialRealNumber, initialImaginaryNumber, power, escapeValue, colorMap)

    def initialize(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                  initialRealNumber, initialImaginaryNumber, power, escapeValue, colorMap = DEFAULT_COLOR_MAP):
        # Setup Included Indexes and the Real and Imaginary Number Spaces
        ZoomableComplexRange.initialize(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin,
                                       imaginaryNumberMax)

        # Calculate C Values and Initial Z Value
        cValues = numpy.multiply(numpy.complex(0,1), self._imaginaryNumberValues)
        cValues = numpy.add(cValues, self._realNumberValues)

        zValues = numpy.add(numpy.complex(initialRealNumber, initialImaginaryNumber), cValues)

        self._zValues = zValues
        self._cValues = cValues

        # Initialize Image Cache
        CachedImageRenderer.initialize(self, width, height, cValues.shape, colorMap)
        
        self._initialRealNumber = initialRealNumber
        self._initialImaginaryNumber = initialImaginaryNumber
        self._power = power
        self._escapeValue = escapeValue

    def reinitialize(self):
        self.initialize(self._width, self._height, self._minRealNumber, self._maxRealNumber, self._minImaginaryNumber,
                       self._maxImaginaryNumber, self._initialRealNumber, self._initialImaginaryNumber, self._power,
                       self._escapeValue, self._colorMap)

    def preheatRenderCache(self, maxIterations):
        print("Preheating Multibrot Render Cache")
        super().preheatRenderCache(maxIterations)

    def iterate(self):
        if len(self._zValues) <= 0:
            # Nothing left to calculate, so just store the last image in the cache
            finalImage = self._renderCache[len(self._renderCache) - 1]
            self._renderCache.update({ self._nextIterationIndex : finalImage })
            self._nextIterationIndex += 1
            return

        # Apply Multibrot Algorithm
        zValuesNew = multibrotAlgorithm(self._zValues, self._cValues, self._power)

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
        self._xIndexes, self._yIndexes, self._zValues, self._cValues = removeIndexes([ self._xIndexes, self._yIndexes, zValuesNew,
                                                                            self._cValues ], remainingIndexes)