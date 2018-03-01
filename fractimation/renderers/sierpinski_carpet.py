# https://en.wikipedia.org/wiki/Sierpinski_carpet

import numpy

from .base.cached_patch_collection_renderer import CachedPatchCollectionRenderer
from ..helpers.render import build_rectangle, build_patch_collection

X_VALUE_INDEX = 0
Y_VALUE_INDEX = 1
WIDTH_INDEX = 2
HEIGHT_INDEX = 3
INITIAL_RECTS = [ [ 0.01, 0.01, 0.98, 0.98 ] ]

def calculateSubdivisions(rectangles):
    firstRect = rectangles[0]
    oneThirdWidth = firstRect[WIDTH_INDEX] * (1 / 3)
    twoThirdsWidth = firstRect[WIDTH_INDEX] * (2 / 3)
    oneThirdHeight = firstRect[HEIGHT_INDEX] * (1 / 3)
    twoThirdsHeight = firstRect[HEIGHT_INDEX] * (2 / 3)

    # Top Subdivisions
    topRightSubdivision = rectangles + [ 0,
                                         0,
                                         -twoThirdsWidth, -twoThirdsHeight
                                       ]
    topMiddleSubdivision = rectangles + [ oneThirdWidth,
                                          0,
                                          -twoThirdsWidth, -twoThirdsHeight
                                        ]
    topLeftSubdivision = rectangles + [ twoThirdsWidth,
                                        0,
                                        -twoThirdsWidth, -twoThirdsHeight
                                      ]

    # Middle Subdivisions
    middleRightSubdivision = rectangles + [ 0,
                                            oneThirdHeight,
                                            -twoThirdsHeight, -twoThirdsHeight
                                          ]
    middleLeftSubdivision = rectangles + [ twoThirdsWidth,
                                           oneThirdHeight,
                                           -twoThirdsHeight, -twoThirdsHeight
                                         ]

    # Bottom Subdivisions
    bottomLeftSubdivision = rectangles + [ 0,
                                           twoThirdsHeight,
                                           -twoThirdsHeight, -twoThirdsHeight
                                         ]
    bottomMiddleSubdivision = rectangles + [ oneThirdWidth,
                                             twoThirdsHeight,
                                             -twoThirdsHeight, -twoThirdsHeight
                                           ]
    bottomRightSubdivision = rectangles + [ twoThirdsWidth,
                                            twoThirdsHeight,
                                            -twoThirdsHeight, -twoThirdsHeight
                                          ]

    allSubdivisions = numpy.concatenate((topLeftSubdivision, topMiddleSubdivision, topRightSubdivision,
                              middleLeftSubdivision, middleRightSubdivision,
                              bottomLeftSubdivision, bottomMiddleSubdivision, bottomRightSubdivision))
    return allSubdivisions

class SierpinskiCarpet(CachedPatchCollectionRenderer):
    """Fractal Renderer for Sierpinski Carpet (aka Sierpinski Square)"""

    _eligibleRects = None
    _lineWidths = None

    def __init__(self, lineWidths, eligibleRects=None):
        self.initialize(lineWidths, eligibleRects)

    # eligibleRects is an array of arrays of x, y, width and height describing the initial rectangles
    #   as percentages of screen space.
    def initialize(self, lineWidths, eligibleRects=None):
        super().initialize()

        self._lineWidths = lineWidths

        if eligibleRects == None:
            eligibleRects = INITIAL_RECTS
        self._eligibleRects = numpy.array(eligibleRects)

        initialPatches = [ ]
        for eligibleRect in eligibleRects:
            newPatch = build_rectangle(eligibleRect[X_VALUE_INDEX], eligibleRect[Y_VALUE_INDEX],
                                                   eligibleRect[WIDTH_INDEX], eligibleRect[HEIGHT_INDEX], lineWidths[0])
            initialPatches.append(newPatch)

        initialPatchCollection = build_patch_collection(initialPatches)
        self._render_cache.update({ 0 : initialPatchCollection })

        self._nextIterationIndex = 1

    def preheatRenderCache(self, maxIterations):
        print("Preheating Sierpinski Carpet Render Cache")
        super().preheatRenderCache(maxIterations)

    def iterate(self):
        if (len(self._eligibleRects)) < 1:
            return

        newRectanglePatches = [ ]
        subdivisions = calculateSubdivisions(self._eligibleRects)
        lineWidth = self._lineWidths[self._next_iteration_index]
        for newRect in subdivisions:
            newPatch = build_rectangle(newRect[X_VALUE_INDEX], newRect[Y_VALUE_INDEX],
                                                   newRect[WIDTH_INDEX], newRect[HEIGHT_INDEX], lineWidth)
            newRectanglePatches.append(newPatch)

        iterationPatchCollection = build_patch_collection(newRectanglePatches)
        self._render_cache.update({ self._next_iteration_index : iterationPatchCollection })

        self._eligibleRects = subdivisions
        self._next_iteration_index += 1