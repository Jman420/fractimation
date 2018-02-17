# http://pi3.sites.sheffield.ac.uk/tutorials/week-1-fibonacci
# http://junilyd.github.io/blog/2014/08/13/fibonacci-mystery-pythonified/

import numpy

from renderers.fractimationRenderer import FractimationRenderer
import renderers.renderHelper as renderHelper

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

class goldenSpiralRenderer(FractimationRenderer):
    """Fractal Renderer for the Golden Spiral"""

    _wedgesAddedToAxes = False
    _sizeScalar = _lineWidths = None
    _nextWedgeLocation = None
    _nextMoveMode = _nextWedgeAngles = None

    def __init__(self, lineWidths, sizeScalar=SIZE_SCALAR):
        self._wedgesAddedToAxes = False
        self.initialize(lineWidths, sizeScalar)

    def initialize(self, lineWidths, sizeScalar=SIZE_SCALAR):
        self._lineWidths = lineWidths
        self._sizeScalar = sizeScalar
        
        self._nextWedgeLocation = numpy.array(INITIAL_LOCATION)
        self._nextWedgeAngles = numpy.array(INITIAL_ANGLES)
        self._nextMoveMode = 1

        self._renderCache = { }
        emptyPatches = renderHelper.buildPatchCollection([ ])
        self._renderCache.update({ 0 : emptyPatches })

        self._nextIterationIndex = 1

    def preheatRenderCache(self, maxIterations):
        print("Preheating Golden Spiral Render Cache")
        super().preheatRenderCache(maxIterations)

    def iterate(self):
        self._nextWedgeAngles += 90
        currentFibNumber = getFibonocciNumber(self._nextIterationIndex) * self._sizeScalar
        wedgeLocation = self._nextWedgeLocation

        secondPrevFibNum = getFibonocciNumber(self._nextIterationIndex - 2) * self._sizeScalar
        prevFibNum = getFibonocciNumber(self._nextIterationIndex - 1) * self._sizeScalar
        if self._nextMoveMode == 1:
            moveDeviation = [ -secondPrevFibNum, 0 ]
        elif self._nextMoveMode == 2:
            moveDeviation = [ 0, -secondPrevFibNum ]
        elif self._nextMoveMode == 3:
            moveDeviation = [ secondPrevFibNum, 0 ]
        elif self._nextMoveMode == 4:
            moveDeviation = [ 0, secondPrevFibNum ]

        self._nextWedgeLocation = wedgeLocation + moveDeviation
        lineWidth = self._lineWidths[self._nextIterationIndex]
        newWedge = renderHelper.buildWedge(self._nextWedgeLocation[X_VALUE_INDEX], self._nextWedgeLocation[Y_VALUE_INDEX], currentFibNumber,
                              self._nextWedgeAngles[THETA1_INDEX], self._nextWedgeAngles[THETA2_INDEX], lineWidth)
        patchCollection = renderHelper.buildPatchCollection([ newWedge ])
        self._renderCache.update({ self._nextIterationIndex : patchCollection })

        self._nextIterationIndex += 1
        self._nextMoveMode += 1
        if self._nextMoveMode > 4:
            self._nextMoveMode = 1 

    def render(self, frameNumber, axes):
        if not self._wedgesAddedToAxes:
            existingWedges = axes.get_children()
            for frameCounter in range(0, len(self._renderCache)):
                frameWedges = self._renderCache[frameCounter]
                if frameWedges not in existingWedges:
                    axes.add_collection(frameWedges)

            self._wedgesAddedToAxes = True
        
        if not frameNumber in self._renderCache:
            for frameCounter in range(self._nextIterationIndex, frameNumber + 1):
                self.iterate()

                frameWedges = self._renderCache[frameCounter]
                axes.add_collection(frameWedges)

        for frameCounter in range(0, len(self._renderCache)):
            frameWedges = self._renderCache[frameCounter]
            frameWedges.set_visible(frameCounter <= frameNumber)