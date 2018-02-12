from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

class sierpinskiCarpetRenderer(object):
    """Fractal Renderer for Sierpinski Carpet (aka Sierpinski Square)"""

    _eligibleRects = _rectanglesCache = None
    _cachePreheated = _rectanglesAddedToAxes = False
    _lineWidths = None
    _currentFrameNumber =  None

    def __init__(self, lineWidths, eligibleRects=None):
        self.initialize(lineWidths, eligibleRects)

    def initialize(self, lineWidths, eligibleRects=None):
        self._rectanglesCache = { }
        self._rectanglesAddedToAxes = False
        self._cachePreheated = False
        self._currentFrameNumber = 1
        self._lineWidths = lineWidths

        if eligibleRects == None:
            eligibleRects = [ rectangleDimensions(0, 0, 1, 1) ]
        self._eligibleRects = eligibleRects

        initialPatches = [ ]
        for eligibleRect in eligibleRects:
            newPatch = self.buildRectangle(eligibleRect, lineWidths[0])
            initialPatches.append(newPatch)

        initialPatchCollection = self.buildPatchCollection(initialPatches)
        self._rectanglesCache.update({ 0 : initialPatchCollection })

    def preheatCache(self, maxIterations):
        if self._cachePreheated:
            return

        for iterationCounter in range(1, maxIterations):
            self.iterate(iterationCounter, lineWidths[iterationCounter])

        self._cachePreheated = True

    def calculateSubdivisions(self, rectangle):
        subdivisions = [ ]
        thirdWidth = rectangle._width / 3
        thirdHeight = rectangle._height / 3
        twoThirdHeight = rectangle._height * (2 / 3)

        for subdivisionCounter in range(0, 3):
            subdivisionRect = rectangleDimensions(rectangle._x + subdivisionCounter * thirdWidth,
                                                  rectangle._y,
                                                  thirdHeight, thirdHeight)
            subdivisions.append(subdivisionRect)

        for subdivisionCounter in [0, 2]:
            subdivisionRect = rectangleDimensions(rectangle._x + subdivisionCounter * thirdWidth,
                                                  rectangle._y + thirdHeight,
                                                  thirdHeight, thirdHeight)
            subdivisions.append(subdivisionRect)

        for subdivisionCounter in range(0, 3):
            subdivisionRect = rectangleDimensions(rectangle._x + subdivisionCounter * thirdWidth,
                                                  rectangle._y + twoThirdHeight,
                                                  thirdHeight, thirdHeight)
            subdivisions.append(subdivisionRect)

        return subdivisions

    def iterate(self, iterationIndex, lineWidth):
        newEligibleRects = [ ]
        newRectanglePatches = [ ]

        for eligibleRect in self._eligibleRects:
            subdivisions = self.calculateSubdivisions(eligibleRect)

            for newRect in subdivisions:
                newPatch = self.buildRectangle(newRect, lineWidth)
                newRectanglePatches.append(newPatch)

            newEligibleRects.extend(subdivisions)

        iterationPatchCollection = self.buildPatchCollection(newRectanglePatches)
        self._rectanglesCache.update({ iterationIndex : iterationPatchCollection })

        self._eligibleRects = newEligibleRects
        self._currentFrameNumber = iterationIndex + 1

    def render(self, frameNumber, axes):
        if not self._rectanglesAddedToAxes:
            for frameCounter in range(0, len(self._rectanglesCache)):
                frameRectangles = self._rectanglesCache[frameCounter]
                axes.add_collection(frameRectangles)
            self._rectanglesAddedToAxes = True
        
        if not frameNumber in self._rectanglesCache:
            for frameCounter in range(self._currentFrameNumber, frameNumber + 1):
                self.iterate(frameCounter, self._lineWidths[frameCounter])

                frameRectangles = self._rectanglesCache[frameCounter]
                axes.add_collection(frameRectangles)

        for frameCounter in range(0, len(self._rectanglesCache)):
            frameRectangles = self._rectanglesCache[frameCounter]
            frameRectangles.set_visible(frameCounter <= frameNumber)

    def buildRectangle(self, dimensions, linewidth):
        newPatch = Rectangle((dimensions._x, dimensions._y), dimensions._width, dimensions._height, fill=False, linewidth=linewidth)
        return newPatch

    def buildPatchCollection(self, patches):
        patchCollection = PatchCollection(patches, True)
        patchCollection.set_visible(False)
        return patchCollection

class rectangleDimensions(object):
    _x = _y = None
    _width = _height = None

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
