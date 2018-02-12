# https://en.wikipedia.org/wiki/Sierpinski_triangle

import numpy

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

def calculateSubdivisions(vertices):
    firstTriangle = vertices[0]
    largeSubdivision = (firstTriangle[2,0] - firstTriangle[0,0]) / 2
    smallSubdivision = largeSubdivision / 2

    leftSubdivision = vertices + [
                                    [ 0, 0 ],
                                    [ -smallSubdivision, -largeSubdivision ],
                                    [ -largeSubdivision, 0 ]
                                 ]
    topSubdivision = vertices + [
                                    [ smallSubdivision, largeSubdivision ],
                                    [ 0, 0 ],
                                    [ -smallSubdivision, largeSubdivision ]
                                ]
    rightSubdivision = vertices + [
                                    [ largeSubdivision, 0 ],
                                    [ smallSubdivision, -largeSubdivision ],
                                    [ 0, 0 ]
                                  ]

    allSubdivisions = numpy.concatenate((leftSubdivision, topSubdivision, rightSubdivision))
    return allSubdivisions

def buildTriangle(vertices, lineWidth):
    newPatch = Polygon(vertices, fill=False, lineWidth=lineWidth)
    return newPatch

def buildPatchCollection(patches):
    patchCollection = PatchCollection(patches, True)
    patchCollection.set_visible(False)
    return patchCollection

class sierpinskiTriangleRenderer(object):
    """Fractal Renderer for Sierpinski Triangle"""

    _eligibleVertices = _trianglesCache = None
    _cachePreheated = _trianglesAddedToAxes = False
    _lineWidths = None
    _currentFrameNumber =  None

    def __init__(self, lineWidths, eligibleRects=None):
        self.initialize(lineWidths, eligibleRects)

    # eligibleVertices is an array of three vertices that describe the points of a triangle.
    #    These vertices must be defined from left to right; ie. [ [ left vertex ], [ top vertex ], [ right vertex ] ]
    def initialize(self, lineWidths, eligibleVertices=None):
        self._trianglesCache = { }
        self._trianglesAddedToAxes = False
        self._cachePreheated = False
        self._currentFrameNumber = 1
        self._lineWidths = lineWidths

        if eligibleVertices == None:
            eligibleVertices = [ 
                                 [ 0, 0 ],
                                 [ 0.5, 1 ],
                                 [ 1, 0 ]
                               ]
        self._eligibleVertices = numpy.array([ eligibleVertices ])

        initialPatches = [ ]
        for eligibleTriangle in self._eligibleVertices:
            newPatch = buildTriangle(eligibleTriangle, lineWidth=lineWidths[0])
            initialPatches.append(newPatch)

        initialPatchCollection = buildPatchCollection(initialPatches)
        self._trianglesCache.update({ 0 : initialPatchCollection })

    def preheatCache(self, maxIterations):
        if self._cachePreheated:
            return

        print("Preheating Sierpinski Triangle Cache to {} iterations...".format(maxIterations))
        for iterationCounter in range(1, maxIterations):
            print("Sierpinski Triangle iteration {} processing...".format(iterationCounter))
            self.iterate(iterationCounter, self._lineWidths[iterationCounter])

        self._cachePreheated = True
        print("Completed preheating Sierpinski Triangle cache!")

    def iterate(self, iterationIndex, lineWidth):
        if len(self._eligibleVertices) < 1:
            return
        
        newTrianglePatches = [ ]

        subdivisions = calculateSubdivisions(self._eligibleVertices)
        for triangleVertices in subdivisions:
            newPatch = buildTriangle(triangleVertices, lineWidth)
            newTrianglePatches.append(newPatch)

        iterationPatchCollection = buildPatchCollection(newTrianglePatches)
        self._trianglesCache.update({ iterationIndex : iterationPatchCollection })

        self._eligibleVertices = subdivisions
        self._currentFrameNumber = iterationIndex + 1

    def render(self, frameNumber, axes):
        if not self._trianglesAddedToAxes:
            for frameCounter in range(0, len(self._trianglesCache)):
                frameTriangles = self._trianglesCache[frameCounter]
                axes.add_collection(frameTriangles)
            self._trianglesAddedToAxes = True
        
        if not frameNumber in self._trianglesCache:
            for frameCounter in range(self._currentFrameNumber, frameNumber + 1):
                self.iterate(frameCounter, self._lineWidths[frameCounter])

                frameTriangles = self._trianglesCache[frameCounter]
                axes.add_collection(frameTriangles)

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