import numpy
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

class sierpinskiTriangleRenderer(object):
    """Fractal Renderer for Sierpinski Triangle"""

    _width = _height = None
    _trianglesCache = None
    _trianglesAddedToAxes = False

    def __init__(self, width, height, maxFrames):
        self.initialize(width, height, maxFrames)

    def initialize(self, width, height, maxFrames):
        self._width = width
        self._height = height
        self._trianglesCache = { }
        self._trianglesAddedToAxes = False

        lineWidths = numpy.linspace(1.0, 0.1, maxFrames)
        eligibleRectangles = [ rectangleDimensions(0, 0, 1, 1) ]
        for frameCounter in range(0, maxFrames):
            newEligibleRects = [ ]
            newTrianglePatches = [ ]

            for eligibleRect in eligibleRectangles:
                quarterWidth = eligibleRect._width * 0.25
                halfWidth = eligibleRect._width * 0.5
                threeQuarterWidth = eligibleRect._width * 0.75
                halfHeight = eligibleRect._height * 0.5

                trianglePoints = [
                                    [ eligibleRect._x, eligibleRect._y ],
                                    [ eligibleRect._x + halfWidth, eligibleRect._y + eligibleRect._height ],
                                    [ eligibleRect._x + eligibleRect._width, eligibleRect._y ]
                                 ]
                newPatch = Polygon(trianglePoints, fill=False, lineWidth=lineWidths[frameCounter])
                newTrianglePatches.append(newPatch)

                topSubdivision = rectangleDimensions(eligibleRect._x + quarterWidth,
                                                     eligibleRect._y + halfHeight,
                                                     halfWidth, halfHeight)
                leftSubdivision = rectangleDimensions(eligibleRect._x,
                                                      eligibleRect._y,
                                                      halfWidth, halfHeight)
                rightSubdivision = rectangleDimensions(eligibleRect._x + halfWidth,
                                                       eligibleRect._y,
                                                       halfWidth, halfHeight)
                newEligibleRects.extend([ topSubdivision, leftSubdivision, rightSubdivision ])

            eligibleRectangles = list(newEligibleRects)
            iterationPatchCollection = PatchCollection(newTrianglePatches, True)
            iterationPatchCollection.set_visible(False)
            self._trianglesCache.update({ frameCounter : iterationPatchCollection })

    def render(self, frameNumber, axes):
        if not self._trianglesAddedToAxes:
            for frameCounter in range(0, len(self._trianglesCache)):
                frameTriangles = self._trianglesCache[frameCounter]
                axes.add_collection(frameTriangles)
            self._trianglesAddedToAxes = True

        for frameCounter in range(0, len(self._trianglesCache)):
            frameTriangles = self._trianglesCache[frameCounter]
            frameTriangles.set_visible(frameCounter <= frameNumber)

class rectangleDimensions(object):
    _x = _y = None
    _width = _height = None

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height