# http://pi3.sites.sheffield.ac.uk/tutorials/week-1-fibonacci
# http://junilyd.github.io/blog/2014/08/13/fibonacci-mystery-pythonified/

import numpy

from renderers.fractimationRenderer import FractimationRenderer
import renderers.renderHelper as renderHelper

X_VALUE_INDEX = 0
Y_VALUE_INDEX = 1
SIZE_SCALAR = 0.1
INITIAL_LOCATION = [ 0, 0 ]

PHI = (1 + 5**0.5) / 2.0
def getFibonocciNumber(index):
    if index < 2:
        return index
    return int(round((PHI**index - (1 - PHI)**index) / 5**0.5))

class FibonacciSquareRenderer(FractimationRenderer):
    """Fractal Renderer for Fibonocci Squares"""
    
    _squaresAddedToAxes = False
    _sizeScalar = _lineWidths = None
    _nextSquareLocation = None
    _nextMoveMode = None

    def __init__(self, lineWidths, sizeScalar=SIZE_SCALAR):
        self._squaresAddedToAxes = False
        self.initialize(lineWidths, sizeScalar)

    def initialize(self, lineWidths, sizeScalar=SIZE_SCALAR):
        self._lineWidths = lineWidths
        self._sizeScalar = sizeScalar
        self._nextSquareLocation = numpy.array(INITIAL_LOCATION)
        self._nextMoveMode = 1

        self._renderCache = { }
        emptyPatches = renderHelper.buildPatchCollection([ ])
        self._renderCache.update({ 0 : emptyPatches })

        self._nextIterationIndex = 1

    def preheatRenderCache(self, maxIterations):
        print("Preheating Fibonocci Square Render Cache")
        super().preheatRenderCache(maxIterations)

    def iterate(self):
        currentFibNumber = getFibonocciNumber(self._nextIterationIndex) * self._sizeScalar
        squareLocation = self._nextSquareLocation

        secondPrevFibNum = getFibonocciNumber(self._nextIterationIndex - 2) * self._sizeScalar
        prevFibNum = getFibonocciNumber(self._nextIterationIndex - 1) * self._sizeScalar
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

    def render(self, frameNumber, axes):
        if not self._squaresAddedToAxes:
            for frameCounter in range(0, len(self._renderCache)):
                frameSquares = self._renderCache[frameCounter]
                axes.add_collection(frameSquares)
            self._squaresAddedToAxes = True
        
        if not frameNumber in self._renderCache:
            for frameCounter in range(self._nextIterationIndex, frameNumber + 1):
                self.iterate()

                frameSquares = self._renderCache[frameCounter]
                axes.add_collection(frameSquares)

        for frameCounter in range(0, len(self._renderCache)):
            frameSquares = self._renderCache[frameCounter]
            frameSquares.set_visible(frameCounter <= frameNumber)