# https://en.wikipedia.org/wiki/Sierpinski_triangle

import numpy

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

LAST_VERTEX_INDEX = 2
FIRST_VERTEX_INDEX = 0
X_VALUE_INDEX = 0
INITIAL_ELIGIBLE_VERTICES = [ 
                                [ 0, 0 ],
                                [ 0.5, 1 ],
                                [ 1, 0 ]
                            ]

def calculateSubdivisions(vertices):
    firstTriangle = vertices[0]
    largeSubdivision = (firstTriangle[LAST_VERTEX_INDEX, X_VALUE_INDEX] - firstTriangle[FIRST_VERTEX_INDEX, X_VALUE_INDEX]) / 2
    smallSubdivision = largeSubdivision / 2

    leftSubdivisionMod = [
                            [ 0, 0 ],
                            [ -smallSubdivision, -largeSubdivision ],
                            [ -largeSubdivision, 0 ]
                         ]
    topSubdivisionMod = [
                            [ smallSubdivision, largeSubdivision ],
                            [ 0, 0 ],
                            [ -smallSubdivision, largeSubdivision ]
                        ]
    rightSubdivisionMod = [
                            [ largeSubdivision, 0 ],
                            [ smallSubdivision, -largeSubdivision ],
                            [ 0, 0 ]
                          ]

    leftSubdivision = vertices + leftSubdivisionMod
    topSubdivision = vertices + topSubdivisionMod
    rightSubdivision = vertices + rightSubdivisionMod

    return numpy.concatenate((leftSubdivision, topSubdivision, rightSubdivision))

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
    _trianglesAddedToAxes = False
    _lineWidths = None
    _currentFrameNumber =  None

    def __init__(self, lineWidths, eligibleRects=None):
        self.initialize(lineWidths, eligibleRects)

    # eligibleVertices is an array of three vertices that describe the points of a triangle as percentages of screen space.
    #    These vertices must be defined from left to right; ie. [ [ left vertex ], [ top vertex ], [ right vertex ] ]
    def initialize(self, lineWidths, eligibleVertices=None):
        self._trianglesCache = { }
        self._trianglesAddedToAxes = False
        self._currentFrameNumber = 1
        self._lineWidths = lineWidths

        if eligibleVertices == None:
            eligibleVertices = INITIAL_ELIGIBLE_VERTICES
        self._eligibleVertices = numpy.array([ eligibleVertices ])

        initialPatches = [ ]
        for eligibleTriangle in self._eligibleVertices:
            newPatch = buildTriangle(eligibleTriangle, lineWidth=lineWidths[0])
            initialPatches.append(newPatch)

        initialPatchCollection = buildPatchCollection(initialPatches)
        self._trianglesCache.update({ 0 : initialPatchCollection })

    def preheatCache(self, maxIterations):
        if maxIterations < len(self._trianglesCache):
            return

        print("Preheating Sierpinski Triangle Cache to {} iterations...".format(maxIterations))
        for iterationCounter in range(len(self._trianglesCache), maxIterations):
            print("Sierpinski Triangle iteration {} processing...".format(iterationCounter))
            self.iterate(iterationCounter, self._lineWidths[iterationCounter])

        self._cachePreheated = True
        print("Completed preheating Sierpinski Triangle cache!")

    def iterate(self, iterationIndex, lineWidth):
        if len(self._eligibleVertices) < 1:
            return
        
        newTrianglePatches = [ ]
        newSubdivisions = calculateSubdivisions(self._eligibleVertices)
        for triangleVertices in newSubdivisions:
            newPatch = buildTriangle(triangleVertices, lineWidth)
            newTrianglePatches.append(newPatch)

        iterationPatchCollection = buildPatchCollection(newTrianglePatches)
        self._trianglesCache.update({ iterationIndex : iterationPatchCollection })

        self._eligibleVertices = newSubdivisions
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