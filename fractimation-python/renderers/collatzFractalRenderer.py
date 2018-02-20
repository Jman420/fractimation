# http://www.njohnston.ca/2009/06/the-collatz-conjecture-as-a-fractal/
# https://github.com/sebhz/fractals/blob/master/mandelbrot/python/fractal.py#L27
# https://en.wikipedia.org/wiki/Collatz_conjecture
# https://glowingpython.blogspot.com/2011/06/collatz-conjecture.html

from .base.cachedImageRenderer import CachedImageRenderer
from .functionality.zoomableComplexRange import ZoomableComplexRange

class CollatzFractalRenderer(CachedImageRenderer, ZoomableComplexRange):
    """Fractal Renderer for Collatz Conjecture Fractals"""
    
    def __init__(self, width, height):
        super().__init__()