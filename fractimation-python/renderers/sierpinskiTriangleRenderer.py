# https://en.wikipedia.org/wiki/Sierpinski_triangle

import numpy

from renderers.fractimationRenderer import FractimationRenderer
import renderers.renderHelper as renderHelper

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

class SierpinskiTriangleRenderer(FractimationRenderer):
    """Fractal Renderer for Sierpinski Triangle"""

    _eligibleVertices = None
    _trianglesAddedToAxes = False
    _lineWidths = None
    _nextIterationIndex =  None

    def __init__(self, lineWidths, eligibleRects=None):
        self.initialize(lineWidths, eligibleRects)

    # eligibleVertices is an array of three vertices that describe the points of a triangle as percentages of screen space.
    #    These vertices must be defined from left to right; ie. [ [ left vertex ], [ top vertex ], [ right vertex ] ]
    def initialize(self, lineWidths, eligibleVertices=None):
        self._lineWidths = lineWidths
        self._renderCache = { }

        if eligibleVertices == None:
            eligibleVertices = INITIAL_ELIGIBLE_VERTICES
        self._eligibleVertices = numpy.array([ eligibleVertices ])

        initialPatches = [ ]
        for eligibleTriangle in self._eligibleVertices:
            newPatch = renderHelper.buildTriangle(eligibleTriangle, lineWidth=lineWidths[0])
            initialPatches.append(newPatch)

        initialPatchCollection = renderHelper.buildPatchCollection(initialPatches)
        self._renderCache.update({ 0 : initialPatchCollection })

        self._trianglesAddedToAxes = False
        self._nextIterationIndex = 1

    def preheatRenderCache(self, maxIterations):
        print("Preheating Sierpinski Triangle Render Cache")
        super().preheatRenderCache(maxIterations)

    def iterate(self):
        if len(self._eligibleVertices) < 1:
            return
        
        newTrianglePatches = [ ]
        newSubdivisions = calculateSubdivisions(self._eligibleVertices)
        lineWidth = self._lineWidths[self._nextIterationIndex]
        for triangleVertices in newSubdivisions:
            newPatch = renderHelper.buildTriangle(triangleVertices, lineWidth)
            newTrianglePatches.append(newPatch)

        iterationPatchCollection = renderHelper.buildPatchCollection(newTrianglePatches)
        self._renderCache.update({ self._nextIterationIndex : iterationPatchCollection })

        self._eligibleVertices = newSubdivisions
        self._nextIterationIndex += 1

    def render(self, frameNumber, axes):
        if not self._trianglesAddedToAxes:
            for frameCounter in range(0, len(self._renderCache)):
                frameTriangles = self._renderCache[frameCounter]
                axes.add_collection(frameTriangles)
            self._trianglesAddedToAxes = True
        
        if not frameNumber in self._renderCache:
            for frameCounter in range(self._nextIterationIndex, frameNumber + 1):
                self.iterate()

                frameTriangles = self._renderCache[frameCounter]
                axes.add_collection(frameTriangles)

        for frameCounter in range(0, len(self._renderCache)):
            frameTriangles = self._renderCache[frameCounter]
            frameTriangles.set_visible(frameCounter <= frameNumber)