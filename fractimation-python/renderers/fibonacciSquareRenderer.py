# http://pi3.sites.sheffield.ac.uk/tutorials/week-1-fibonacci

import numpy
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

X_VALUE_INDEX = 0
Y_VALUE_INDEX = 1
SIZE_SCALAR = 0.1

PHI = (1 + 5**0.5) / 2.0
def getFibonocciNumber(index):
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

    def __init__(self, lineWidths, sizeScalar=SIZE_SCALAR):
        self._squaresAddedToAxes = False
        self.initialize(lineWidths, sizeScalar)

    def initialize(self, lineWidths, sizeScalar=SIZE_SCALAR):
        self._lineWidths = lineWidths
        self._sizeScalar = sizeScalar
        self._squaresCache = { }
        self._nextIterationIndex = 0
        self._nextSquareLocation = [ 0, 0 ]

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
        scaledFibNum = getFibonocciNumber(self._nextIterationIndex + 1) * self._sizeScalar
        newSquare = buildSquare(self._nextSquareLocation[X_VALUE_INDEX], self._nextSquareLocation[Y_VALUE_INDEX],
                               scaledFibNum, lineWidth)
        patchCollection = buildPatchCollection([ newSquare ])
        self._squaresCache.update({ self._nextIterationIndex : patchCollection })

        scaledPrevFibNum = getFibonocciNumber(self._nextIterationIndex) * self._sizeScalar
        if self._nextIterationIndex % 2:
            self._nextSquareLocation[Y_VALUE_INDEX] += scaledFibNum
        elif self._nextIterationIndex % 3:
            self._nextSquareLocation[X_VALUE_INDEX] -= scaledFibNum
        elif self._nextIterationIndex % 4:
            self._nextSquareLocation[Y_VALUE_INDEX] -= scaledFibNum
        else:
            self._nextSquareLocation[X_VALUE_INDEX] += scaledFibNum

        self._nextIterationIndex += 1

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