# https://stackoverflow.com/questions/17393592/how-do-i-speed-up-fractal-generation-with-numpy-arrays
# https://austingwalters.com/newtons-method-and-fractals/

import numpy
import numpy.polynomial.polynomial as numpynomial

from .complexPolynomialRenderer import ComplexPolynomialRenderer
from helpers.fractalAlgorithmHelper import evaluatePolynomial1D
from helpers.renderHelper import recolorUnexplodedIndexes
from helpers.fractalAlgorithmHelper import removeIndexes

class NewtonFractalRenderer(ComplexPolynomialRenderer):
    """Fractal Renderer for Newton Method Fractals"""
    
    _coefficientArrayDeriv = None

    def __init__(self, width, height, minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber,
                coefficientArray, constantRealNumber, constantImaginaryNumber, escapeValue, colorMap = 'viridis'):
        super().__init__(width, height, minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber,
                coefficientArray, constantRealNumber, constantImaginaryNumber, escapeValue, colorMap)

        self._coefficientArrayDeriv = numpynomial.polyder(self._coefficientArray)
    
    def initialize(self, width, height, minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber,
                  coefficientArray, constantRealNumber, constantImaginaryNumber, escapeValue, colorMap = 'viridis'):
        super().initialize(width, height, minRealNumber, maxRealNumber, minImaginaryNumber, maxImaginaryNumber,
                           coefficientArray, constantRealNumber, constantImaginaryNumber, escapeValue, colorMap)

        self._coefficientArrayDeriv = numpynomial.polyder(self._coefficientArray)

    def preheatRenderCache(self, maxIterations):
        print("Preheating Newton Fractal Render Cache")
        super().preheatRenderCache(maxIterations)

    def iterate(self):
        if len(self._zValues) <= 0:
            # Nothing left to calculate, so just store the last image in the cache
            finalImage = self._renderCache[len(self._renderCache) - 1]
            self._renderCache.update({ self._nextIterationIndex : finalImage })
            self._nextIterationIndex += 1
            return
        
        # Perform Newton Method
        coefficientFuncValues = evaluatePolynomial1D(self._coefficientArray, self._zValues, self._cValue)
        coefficientDerivFuncValues = evaluatePolynomial1D(self._coefficientArrayDeriv, self._zValues, self._cValue)
        funcValues = numpy.divide(coefficientFuncValues, coefficientDerivFuncValues)
        zValuesNew = numpy.add(self._zValues, -funcValues)
        iterationDiff = numpy.add(self._zValues, -zValuesNew)

        # Update indexes which have exceeded the Escape Value
        explodedIndexes = numpy.abs(iterationDiff) < self._escapeValue
        self._imageArray[self._xIndexes[explodedIndexes], self._yIndexes[explodedIndexes]] = self._nextIterationIndex

        # Update cache and prepare for next iteration
        finalImage = numpy.copy(self._imageArray.T)
        self._renderCache.update({ self._nextIterationIndex : finalImage })
        self._nextIterationIndex += 1

        # Remove Exploded Indexes since we don't need to calculate them anymore
        remainingIndexes = ~explodedIndexes
        self._xIndexes, self._yIndexes, self._zValues = removeIndexes([ self._xIndexes, self._yIndexes, zValuesNew ],
                                                                     remainingIndexes)