# http://www.njohnston.ca/2009/06/the-collatz-conjecture-as-a-fractal/
# https://github.com/sebhz/fractals/blob/master/mandelbrot/python/fractal.py#L27
# https://en.wikipedia.org/wiki/Collatz_conjecture
# https://glowingpython.blogspot.com/2011/06/collatz-conjecture.html

import numpy

from .base.cachedImageRenderer import CachedImageRenderer
from .functionality.zoomableComplexRange import ZoomableComplexRange

# z = (2 + 7z - (2 + 5z) * cos(pi * z)) / 4
def collatzConjecture(zValues):
    twoPlusFiveZ = numpy.add(numpy.multiply(zValues, 5), 2)
    cosPiZ = numpy.cos(numpy.multiply(zValues, numpy.pi))
    
    sevenZ = numpy.multiply(zValues, 7)
    cosProduct = numpy.multiply(twoPlusFiveZ, cosPiZ)

    twoPlusSevenZ = numpy.add(sevenZ, 2)

    leftParenVal = numpy.subtract(twoPlusSevenZ, cosProduct)
    zValuesNew = numpy.divide(leftParenVal, 4)

    return zValuesNew

class CollatzFractalRenderer(CachedImageRenderer, ZoomableComplexRange):
    """Fractal Renderer for Collatz Conjecture Fractals"""
    
    _escapeValue = None
    _zValues = _cValue = None

    def __init__(self, width, height, realNumberMin, realNumberMax, imaginaryNumberMin, imaginaryNumberMax,
                 escapeValue, colorMap = "viridis"):
        super().__init__()
        