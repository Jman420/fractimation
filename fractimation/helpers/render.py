from matplotlib.patches import Polygon
from matplotlib.patches import Rectangle
from matplotlib.patches import Wedge
from matplotlib.collections import PatchCollection

def build_triangle(vertices, line_width):
    new_patch = Polygon(vertices, fill=False, lineWidth=line_width)
    return new_patch

def build_rectangle(x, y, width, height, line_width):
    new_patch = Rectangle((x, y), width, height, fill=False, linewidth=line_width)
    return new_patch

def build_square(x, y, dimension, line_width):
    new_patch = build_rectangle(x, y, dimension, dimension, line_width)
    return new_patch

def build_wedge(x, y, radius, theta1, theta2, wedge_width):
    new_patch = Wedge([x, y], radius, theta1, theta2, wedge_width, fill=False)
    return new_patch

def build_patch_collection(patches, visible=False):
    patch_collection = PatchCollection(patches, True)
    patch_collection.set_visible(visible)
    return patch_collection
