import numpy

from matplotlib.patches import Polygon
from matplotlib.patches import Rectangle
from matplotlib.patches import Wedge
from matplotlib.collections import PatchCollection

def buildTriangle(vertices, lineWidth):
    newPatch = Polygon(vertices, fill=False, lineWidth=lineWidth)
    return newPatch

def buildRectangle(x, y, width, height, linewidth):
    newPatch = Rectangle((x, y), width, height, fill=False, linewidth=linewidth)
    return newPatch

def buildSquare(x, y, dimension, linewidth):
    newPatch = buildRectangle(x, y, dimension, dimension, linewidth)
    return newPatch

def buildWedge(x, y, radius, theta1, theta2, wedgeWidth):
    newPatch = Wedge([x, y], radius, theta1, theta2, wedgeWidth, fill=False)
    return newPatch

def buildPatchCollection(patches, visible=False):
    patchCollection = PatchCollection(patches, True)
    patchCollection.set_visible(visible)
    return patchCollection

def recolorUnexplodedIndexes(image, initialValue, recoloredValue):
    recoloredImage = numpy.copy(image)
    recoloredImage[recoloredImage == initialValue] = recoloredValue
    return recoloredImage