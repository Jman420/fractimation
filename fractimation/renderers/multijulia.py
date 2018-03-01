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

from .base.cached_image_renderer import CachedImageRenderer
from .functionality.zoomable_complex_range import ZoomableComplexRange
from ..helpers.fractal_algorithm import multibrot_algorithm
from ..helpers.list_tools import update_indexes_with_value, remove_indexes

DEFAULT_COLOR_MAP = "viridis"

class Multijulia(CachedImageRenderer, ZoomableComplexRange):
    """Fractal Renderer for Multi-Julia Sets"""

    _constantRealNumber = _constantImaginaryNumber = None
    _power = _escapeValue = None

    _zValues = _cValue = None

    def __init__(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax, 
                 constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap = DEFAULT_COLOR_MAP):
        CachedImageRenderer.__init__(self)
        ZoomableComplexRange.__init__(self)

        self.initialize(width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                       constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap)

    def initialize(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                  constantRealNumber, constantImaginaryNumber, power, escapeValue, colorMap = DEFAULT_COLOR_MAP):
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
        self._power = power
        self._escapeValue = escapeValue

    def reinitialize(self):
        self.initialize(self._width, self._height, self._minRealNumber, self._maxRealNumber, self._minImaginaryNumber,
                       self._maxImaginaryNumber, self._constantRealNumber, self._constantImaginaryNumber, self._power,
                       self._escapeValue, self._colorMap)

    def preheatRenderCache(self, maxIterations):
        print("Preheating Multi-Julia Render Cache")
        super().preheatRenderCache(maxIterations)

    def iterate(self):
        if len(self._zValues) <= 0:
            # Nothing left to calculate, so just store the last image in the cache
            finalImage = self._render_cache[len(self._render_cache) - 1]
            self._render_cache.update({ self._nextIterationIndex : finalImage })
            self._next_iteration_index += 1
            return

        # Apply Multibrot Algorithm (Julia Set is a different initialization of Multibrot Algorithm)
        zValuesNew = multibrot_algorithm(self._zValues, self._cValue, self._power)

        # Update indexes which have exceeded the Escape Value
        explodedIndexes = numpy.abs(zValuesNew) > self._escapeValue
        self._imageArray[self._xIndexes[explodedIndexes], self._yIndexes[explodedIndexes]] = self._next_iteration_index

        # Recolor Indexes which have not exceeded the Escape Value
        recoloredImage = update_indexes_with_value(self._imageArray, -1, self._next_iteration_index + 1)
        finalImage = recoloredImage.T

        # Update cache and prepare for next iteration
        self._render_cache.update({ self._next_iteration_index : finalImage })
        self._next_iteration_index += 1

        # Remove Exploded Indexes since we don't need to calculate them anymore
        remainingIndexes = ~explodedIndexes
        self._xIndexes, self._yIndexes, self._zValues = remove_indexes([ self._xIndexes, self._yIndexes,
                                                                                             zValuesNew ], remainingIndexes)