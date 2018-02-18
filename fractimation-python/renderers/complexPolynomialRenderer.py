import numpy

from .base.cachedImageRenderer import CachedImageRenderer
from helpers.fractalAlgorithmHelper import polynomialIterator1D

class ComplexPolynomialRenderer(CachedImageRenderer):
    """Fractal Renderer for Generic Complex Polynomial Equations"""

    def __init__(self, width, height, minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber,
                 coefficientArray, escapeValue, colorMap = "viridis"):
        self.initialize(width, height, minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber,
                        coefficientArray, escapeValue, colorMap)

    def initialize(self, width, height, minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber,
                   coefficientArray, escapeValue, colorMap = "viridis"):
        super().initialize()

