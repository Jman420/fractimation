# https://stackoverflow.com/questions/17393592/how-do-i-speed-up-fractal-generation-with-numpy-arrays
# https://austingwalters.com/newtons-method-and-fractals/

import numpy

from .base.cachedImageRenderer import CachedImageRenderer
from helpers.fractalAlgorithmHelper import polynomialIterator1D

class newtonFractalRenderer(CachedImageRenderer):
    """Fractal Renderer for Newton Fractals"""
    
    