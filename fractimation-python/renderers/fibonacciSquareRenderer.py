# http://pi3.sites.sheffield.ac.uk/tutorials/week-1-fibonacci
# http://junilyd.github.io/blog/2014/08/13/fibonacci-mystery-pythonified/

import numpy

from .base.cachedPatchCollectionRenderer import CachedPatchCollectionRenderer
import helpers.renderHelper as renderHelper
import helpers.fractalAlgorithmHelper as fractalAlgHelper

X_VALUE_INDEX = 0
Y_VALUE_INDEX = 1
SIZE_SCALAR = 0.1
INITIAL_LOCATION = [ 0, 0 ]

class FibonacciSquareRenderer(CachedPatchCollectionRenderer):
    """Fractal Renderer for Fibonocci Squares"""
    
    _sizeScalar = _lineWidths = None
    _nextSquareLocation = None
    _nextMoveMode = None

    def __init__(self, lineWidths, sizeScalar=SIZE_SCALAR):
        self.initialize(lineWidths, sizeScalar)

    def initialize(self, lineWidths, sizeScalar=SIZE_SCALAR):
        super().initialize()

        self._lineWidths = lineWidths
        self._sizeScalar = sizeScalar
        
        emptyPatches = renderHelper.buildPatchCollection([ ])
        self._renderCache.update({ 0 : emptyPatches })

        self._nextIterationIndex = 1
        self._nextSquareLocation = numpy.array(INITIAL_LOCATION)
        self._nextMoveMode = 1

    def preheatRenderCache(self, maxIterations):
        print("Preheating Fibonocci Square Render Cache")
        super().preheatRenderCache(maxIterations)

    def iterate(self):
        currentFibNumber = fractalAlgHelper.getFibonocciNumber(self._nextIterationIndex) * self._sizeScalar
        squareLocation = self._nextSquareLocation

        secondPrevFibNum = fractalAlgHelper.getFibonocciNumber(self._nextIterationIndex - 2) * self._sizeScalar
        prevFibNum = fractalAlgHelper.getFibonocciNumber(self._nextIterationIndex - 1) * self._sizeScalar
        if self._nextMoveMode == 1:
            moveDeviation = [ -secondPrevFibNum, prevFibNum ]
        elif self._nextMoveMode == 2:
            moveDeviation = [ -currentFibNumber, -secondPrevFibNum ]
        elif self._nextMoveMode == 3:
            moveDeviation = [ 0, -currentFibNumber ]
        elif self._nextMoveMode == 4:
            moveDeviation = [ prevFibNum, 0 ]

        self._nextSquareLocation = squareLocation + moveDeviation
        lineWidth = self._lineWidths[self._nextIterationIndex]
        newSquare = renderHelper.buildSquare(self._nextSquareLocation[X_VALUE_INDEX], self._nextSquareLocation[Y_VALUE_INDEX], currentFibNumber, lineWidth)
        patchCollection = renderHelper.buildPatchCollection([ newSquare ])
        self._renderCache.update({ self._nextIterationIndex : patchCollection })

        self._nextIterationIndex += 1
        self._nextMoveMode += 1
        if self._nextMoveMode > 4:
            self._nextMoveMode = 1