# http://pi3.sites.sheffield.ac.uk/tutorials/week-1-fibonacci
# http://junilyd.github.io/blog/2014/08/13/fibonacci-mystery-pythonified/

import numpy
from matplotlib.patches import Wedge
from matplotlib.collections import PatchCollection

X_VALUE_INDEX = 0
Y_VALUE_INDEX = 1
THETA1_INDEX = 0
THETA2_INDEX = 1

SIZE_SCALAR = 0.1
INITIAL_LOCATION = [ 0, 0 ]
INITIAL_ANGLES = [ 270, 0 ]

PHI = (1 + 5**0.5) / 2.0
def getFibonocciNumber(index):
    if index < 2:
        return index
    return int(round((PHI**index - (1 - PHI)**index) / 5**0.5))

def buildWedge(x, y, radius, theta1, theta2, wedgeWidth):
    newPatch = Wedge([x, y], radius, theta1, theta2, wedgeWidth, fill=False)
    return newPatch

def buildPatchCollection(patches):
    patchCollection = PatchCollection(patches, True)
    patchCollection.set_visible(False)
    return patchCollection

class goldenSpiralRenderer(object):
    """Fractal Renderer for the Golden Spiral"""

    _wedgesCache = None
    _wedgesAddedToAxes = False
    _sizeScalar = _lineWidths = None
    _nextIterationIndex = _nextWedgeLocation = None
    _nextMoveMode = _nextWedgeAngles = None

    def __init__(self, lineWidths, sizeScalar=SIZE_SCALAR):
        self._squaresAddedToAxes = False
        self.initialize(lineWidths, sizeScalar)

    def initialize(self, lineWidths, sizeScalar=SIZE_SCALAR):
        self._lineWidths = lineWidths
        self._sizeScalar = sizeScalar
        self._wedgesCache = { }
        self._nextIterationIndex = 1
        self._nextWedgeLocation = numpy.array(INITIAL_LOCATION)
        self._nextWedgeAngles = numpy.array(INITIAL_ANGLES)
        self._nextMoveMode = 1

        emptyPatches = buildPatchCollection([ ])
        self._wedgesCache.update({ 0 : emptyPatches })

    def preheatCache(self, maxIterations):
        if maxIterations < len(self._wedgesCache):
            return

        print("Preheating Fibonocci Square Cache to {} iterations...".format(maxIterations))
        for iterationCounter in range(len(self._wedgesCache), maxIterations):
            print("Fibonocci Square iteration {} processing...".format(iterationCounter))
            self.iterate(iterationCounter, self._lineWidths[iterationCounter])

        self._squaresAddedToAxes = False
        print("Completed preheating Fibonocci Square cache!")

    def iterate(self, lineWidth):
        self._nextWedgeAngles += 90
        currentFibNumber = getFibonocciNumber(self._nextIterationIndex) * self._sizeScalar
        wedgeLocation = self._nextWedgeLocation

        secondPrevFibNum = getFibonocciNumber(self._nextIterationIndex - 2) * self._sizeScalar
        prevFibNum = getFibonocciNumber(self._nextIterationIndex - 1) * self._sizeScalar
        if self._nextMoveMode == 1:
            moveDeviation = [ -secondPrevFibNum, 0 ]
            self._nextWedgeLocation = wedgeLocation + moveDeviation
        elif self._nextMoveMode == 2:
            moveDeviation = [ 0, -secondPrevFibNum ]
            self._nextWedgeLocation = wedgeLocation + moveDeviation
        elif self._nextMoveMode == 3:
            moveDeviation = [ secondPrevFibNum, 0 ]
            self._nextWedgeLocation = wedgeLocation + moveDeviation
        elif self._nextMoveMode == 4:
            moveDeviation = [ 0, secondPrevFibNum ]
            self._nextWedgeLocation = wedgeLocation + moveDeviation

        newWedge = buildWedge(self._nextWedgeLocation[X_VALUE_INDEX], self._nextWedgeLocation[Y_VALUE_INDEX], currentFibNumber,
                              self._nextWedgeAngles[THETA1_INDEX], self._nextWedgeAngles[THETA2_INDEX], lineWidth)
        patchCollection = buildPatchCollection([ newWedge ])
        self._wedgesCache.update({ self._nextIterationIndex : patchCollection })

        self._nextIterationIndex += 1
        self._nextMoveMode += 1
        if self._nextMoveMode > 4:
            self._nextMoveMode = 1 

    def render(self, frameNumber, axes):
        if not self._wedgesAddedToAxes:
            for frameCounter in range(0, len(self._wedgesCache)):
                frameSquares = self._wedgesCache[frameCounter]
                axes.add_collection(frameSquares)
            self._squaresAddedToAxes = True
        
        if not frameNumber in self._wedgesCache:
            for frameCounter in range(self._nextIterationIndex, frameNumber + 1):
                self.iterate(self._lineWidths[frameCounter])

                frameSquares = self._wedgesCache[frameCounter]
                axes.add_collection(frameSquares)

        for frameCounter in range(0, len(self._wedgesCache)):
            frameSquares = self._wedgesCache[frameCounter]
            frameSquares.set_visible(frameCounter <= frameNumber)