# https://en.wikipedia.org/wiki/Sierpinski_carpet

import numpy

from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

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

def buildRectangle(dimensions, linewidth):
    newPatch = Rectangle((dimensions[X_VALUE_INDEX], dimensions[Y_VALUE_INDEX]), dimensions[WIDTH_INDEX],
                        dimensions[HEIGHT_INDEX], fill=False, linewidth=linewidth)
    return newPatch

def buildPatchCollection(patches):
    patchCollection = PatchCollection(patches, True)
    patchCollection.set_visible(False)
    return patchCollection

class sierpinskiCarpetRenderer(object):
    """Fractal Renderer for Sierpinski Carpet (aka Sierpinski Square)"""

    _eligibleRects = _rectanglesCache = None
    _rectanglesAddedToAxes = False
    _lineWidths = None
    _nextIterationIndex =  None

    def __init__(self, lineWidths, eligibleRects=None):
        self.initialize(lineWidths, eligibleRects)

    # eligibleRects is an array of arrays of x, y, width and height describing the initial rectangles
    #   as percentages of screen space.
    def initialize(self, lineWidths, eligibleRects=None):
        self._rectanglesCache = { }
        self._rectanglesAddedToAxes = False
        self._nextIterationIndex = 1
        self._lineWidths = lineWidths

        if eligibleRects == None:
            eligibleRects = INITIAL_RECTS
        self._eligibleRects = numpy.array(eligibleRects)

        initialPatches = [ ]
        for eligibleRect in eligibleRects:
            newPatch = buildRectangle(eligibleRect, lineWidths[0])
            initialPatches.append(newPatch)

        initialPatchCollection = buildPatchCollection(initialPatches)
        self._rectanglesCache.update({ 0 : initialPatchCollection })

    def preheatCache(self, maxIterations):
        if maxIterations < len(self._rectanglesCache):
            return

        print("Preheating Sierpinski Carpet Cache to {} iterations...".format(maxIterations))
        for iterationCounter in range(len(self._rectanglesCache), maxIterations):
            print("Sierpinski Carpet iteration {} processing...".format(iterationCounter))
            self.iterate(self._lineWidths[iterationCounter])

        print("Completed preheating Sierpinski Carpet cache!")

    def iterate(self, lineWidth):
        if (len(self._eligibleRects)) < 1:
            return

        newRectanglePatches = [ ]
        subdivisions = calculateSubdivisions(self._eligibleRects)
        for newRect in subdivisions:
            newPatch = buildRectangle(newRect, lineWidth)
            newRectanglePatches.append(newPatch)

        iterationPatchCollection = buildPatchCollection(newRectanglePatches)
        self._rectanglesCache.update({ self._nextIterationIndex : iterationPatchCollection })

        self._eligibleRects = subdivisions
        self._nextIterationIndex += 1

    def render(self, frameNumber, axes):
        if not self._rectanglesAddedToAxes:
            for frameCounter in range(0, len(self._rectanglesCache)):
                frameRectangles = self._rectanglesCache[frameCounter]
                axes.add_collection(frameRectangles)
            self._rectanglesAddedToAxes = True
        
        if not frameNumber in self._rectanglesCache:
            for frameCounter in range(self._nextIterationIndex, frameNumber + 1):
                self.iterate(self._lineWidths[frameCounter])

                frameRectangles = self._rectanglesCache[frameCounter]
                axes.add_collection(frameRectangles)

        for frameCounter in range(0, len(self._rectanglesCache)):
            frameRectangles = self._rectanglesCache[frameCounter]
            frameRectangles.set_visible(frameCounter <= frameNumber)