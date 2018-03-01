import numpy

from matplotlib.patches import Polygon
from matplotlib.patches import Rectangle
from matplotlib.patches import Wedge
from matplotlib.collections import PatchCollection

def build_triangle(vertices, lineWidth):
    newPatch = Polygon(vertices, fill=False, lineWidth=lineWidth)
    return newPatch

def build_rectangle(x, y, width, height, linewidth):
    newPatch = Rectangle((x, y), width, height, fill=False, linewidth=linewidth)
    return newPatch

def build_square(x, y, dimension, linewidth):
    newPatch = build_rectangle(x, y, dimension, dimension, linewidth)
    return newPatch

def build_wedge(x, y, radius, theta1, theta2, wedgeWidth):
    newPatch = Wedge([x, y], radius, theta1, theta2, wedgeWidth, fill=False)
    return newPatch

def build_patch_collection(patches, visible=False):
    patchCollection = PatchCollection(patches, True)
    patchCollection.set_visible(visible)
    return patchCollection
