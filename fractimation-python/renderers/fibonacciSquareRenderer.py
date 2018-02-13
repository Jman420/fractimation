# http://pi3.sites.sheffield.ac.uk/tutorials/week-1-fibonacci
# http://junilyd.github.io/blog/2014/08/13/fibonacci-mystery-pythonified/

import numpy
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

X_VALUE_INDEX = 0
Y_VALUE_INDEX = 1
SIZE_SCALAR = 0.1
INITIAL_LOCATION = [ 0, 0 ]

PHI = (1 + 5**0.5) / 2.0
def getFibonocciNumber(index):
    if index < 2:
        return index
    return int(round((PHI**index - (1 - PHI)**index) / 5**0.5))

def buildSquare(x, y, dimension, linewidth):
    newPatch = Rectangle((x, y), dimension, dimension, fill=False, linewidth=linewidth)
    return newPatch

def buildPatchCollection(patches):
    patchCollection = PatchCollection(patches, True)
    patchCollection.set_visible(False)
    return patchCollection

class fibonacciSquareRenderer(object):
    """Fractal Renderer for Fibonocci Squares"""

    _squaresCache = None
    _squaresAddedToAxes = False
    _sizeScalar = _lineWidths = None
    _nextIterationIndex = _nextSquareLocation = None
    _nextMoveMode = None

    def __init__(self, lineWidths, sizeScalar=SIZE_SCALAR):
        self._squaresAddedToAxes = False
        self.initialize(lineWidths, sizeScalar)

    def initialize(self, lineWidths, sizeScalar=SIZE_SCALAR):
        self._lineWidths = lineWidths
        self._sizeScalar = sizeScalar
        self._squaresCache = { }
        self._nextIterationIndex = 1
        self._nextSquareLocation = numpy.array(INITIAL_LOCATION)
        self._nextMoveMode = 1

        emptyPatches = buildPatchCollection([ ])
        self._squaresCache.update({ 0 : emptyPatches })

    def preheatCache(self, maxIterations):
        if maxIterations < len(self._squaresCache):
            return

        print("Preheating Fibonocci Square Cache to {} iterations...".format(maxIterations))
        for iterationCounter in range(len(self._squaresCache), maxIterations):
            print("Fibonocci Square iteration {} processing...".format(iterationCounter))
            self.iterate(iterationCounter, self._lineWidths[iterationCounter])

        self._squaresAddedToAxes = False
        print("Completed preheating Fibonocci Square cache!")

    def iterate(self, lineWidth):
        currentFibNumber = getFibonocciNumber(self._nextIterationIndex) * self._sizeScalar
        squareLocation = self._nextSquareLocation

        secondPrevFibNum = getFibonocciNumber(self._nextIterationIndex - 2) * self._sizeScalar
        prevFibNum = getFibonocciNumber(self._nextIterationIndex - 1) * self._sizeScalar
        if self._nextMoveMode == 1:
            moveDeviation = [ -secondPrevFibNum, prevFibNum ]
            self._nextSquareLocation = squareLocation + moveDeviation
        elif self._nextMoveMode == 2:
            moveDeviation = [ -currentFibNumber, -secondPrevFibNum ]
            self._nextSquareLocation = squareLocation + moveDeviation
        elif self._nextMoveMode == 3:
            moveDeviation = [ 0, -currentFibNumber ]
            self._nextSquareLocation = squareLocation + moveDeviation
        elif self._nextMoveMode == 4:
            moveDeviation = [ prevFibNum, 0 ]
            self._nextSquareLocation = squareLocation + moveDeviation

        newSquare = buildSquare(self._nextSquareLocation[X_VALUE_INDEX], self._nextSquareLocation[Y_VALUE_INDEX], currentFibNumber, lineWidth)
        patchCollection = buildPatchCollection([ newSquare ])
        self._squaresCache.update({ self._nextIterationIndex : patchCollection })

        self._nextIterationIndex += 1
        self._nextMoveMode += 1
        if self._nextMoveMode > 4:
            self._nextMoveMode = 1 

    def render(self, frameNumber, axes):
        if not self._squaresAddedToAxes:
            for frameCounter in range(0, len(self._squaresCache)):
                frameSquares = self._squaresCache[frameCounter]
                axes.add_collection(frameSquares)
            self._squaresAddedToAxes = True
        
        if not frameNumber in self._squaresCache:
            for frameCounter in range(self._nextIterationIndex, frameNumber + 1):
                self.iterate(self._lineWidths[frameCounter])

                frameSquares = self._squaresCache[frameCounter]
                axes.add_collection(frameSquares)

        for frameCounter in range(0, len(self._squaresCache)):
            frameSquares = self._squaresCache[frameCounter]
            frameSquares.set_visible(frameCounter <= frameNumber)