# http://pi3.sites.sheffield.ac.uk/tutorials/week-1-fibonacci
# http://junilyd.github.io/blog/2014/08/13/fibonacci-mystery-pythonified/

import numpy

from .base.cached_patch_collection_renderer import CachedPatchCollectionRenderer
from ..helpers.render import build_wedge, build_patch_collection
from ..helpers.fractal_algorithm import get_fibonocci_number

X_VALUE_INDEX = 0
Y_VALUE_INDEX = 1
THETA1_INDEX = 0
THETA2_INDEX = 1

SIZE_SCALAR = 0.1
INITIAL_LOCATION = [ 0, 0 ]
INITIAL_ANGLES = [ 270, 0 ]

class GoldenSpiral(CachedPatchCollectionRenderer):
    """Fractal Renderer for the Golden Spiral"""

    _sizeScalar = None
    _lineWidths = None
    _nextWedgeLocation = None
    _nextMoveMode = None
    _nextWedgeAngles = None

    def __init__(self, lineWidths, sizeScalar=SIZE_SCALAR):
        self._wedgesAddedToAxes = False
        self.initialize(lineWidths, sizeScalar)

    def initialize(self, lineWidths, sizeScalar=SIZE_SCALAR):
        super().initialize()

        self._lineWidths = lineWidths
        self._sizeScalar = sizeScalar
        
        self._nextWedgeLocation = numpy.array(INITIAL_LOCATION)
        self._nextWedgeAngles = numpy.array(INITIAL_ANGLES)
        self._nextMoveMode = 1

        emptyPatches = build_patch_collection([ ])
        self._render_cache.update({ 0 : emptyPatches })

        self._nextIterationIndex = 1

    def preheatRenderCache(self, maxIterations):
        print("Preheating Golden Spiral Render Cache")
        super().preheatRenderCache(maxIterations)

    def iterate(self):
        self._nextWedgeAngles += 90
        currentFibNumber = get_fibonocci_number(self._next_iteration_index) * self._sizeScalar
        wedgeLocation = self._nextWedgeLocation

        secondPrevFibNum = get_fibonocci_number(self._next_iteration_index - 2) * self._sizeScalar
        prevFibNum = get_fibonocci_number(self._next_iteration_index - 1) * self._sizeScalar
        if self._nextMoveMode == 1:
            moveDeviation = [ -secondPrevFibNum, 0 ]
        elif self._nextMoveMode == 2:
            moveDeviation = [ 0, -secondPrevFibNum ]
        elif self._nextMoveMode == 3:
            moveDeviation = [ secondPrevFibNum, 0 ]
        elif self._nextMoveMode == 4:
            moveDeviation = [ 0, secondPrevFibNum ]

        self._nextWedgeLocation = wedgeLocation + moveDeviation
        lineWidth = self._lineWidths[self._next_iteration_index]
        newWedge = build_wedge(self._nextWedgeLocation[X_VALUE_INDEX], self._nextWedgeLocation[Y_VALUE_INDEX], currentFibNumber,
                              self._nextWedgeAngles[THETA1_INDEX], self._nextWedgeAngles[THETA2_INDEX], lineWidth)
        patchCollection = build_patch_collection([ newWedge ])
        self._render_cache.update({ self._next_iteration_index : patchCollection })

        self._next_iteration_index += 1
        self._nextMoveMode += 1
        if self._nextMoveMode > 4:
            self._nextMoveMode = 1
