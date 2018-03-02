"""
Functions related to Matplotlib Rendering

Public Methods :
  * build_triangle - Returns a Matplotlib Triangle Patch
  * build_rectangle - Returns a Matplotlib Rectangle Patch
  * build_square - Returns a Matplotlib Square Patch
  * build_wedge - Returns a Matplotlib Wedge Patch
  * build_patch_collection - Returns a Matplotlib Patch Collection
"""

from matplotlib.patches import Polygon
from matplotlib.patches import Rectangle
from matplotlib.patches import Wedge
from matplotlib.collections import PatchCollection

def build_triangle(vertices, line_width, fill=False):
    """
    Returns a Matplotlib Triangle Patch from the provided vertices

    Parameters :
      * vertices - An array of 3 arrays of 2 float values indicating the vertices of the triangle
          Float values describe screen percentages (ie. [ 0.25, 0.5 ] is a vertex at 25% of the
          width and 50% of the height)
      * line_width - The line width of the edges
      * fill (optional) - Whether or not to fill the triangle
    """
    new_patch = Polygon(vertices, fill=fill, lineWidth=line_width)
    return new_patch

def build_rectangle(x_coord, y_coord, width, height, line_width, fill=False):
    """
    Returns a Matplotlib Rectangle Patch from the provided parameters

    Parameters :
      * x_coord - The x coordinate for the top left corner of the rectangle in screen percentage
      * y_coord - The y coordinate for the top left corner of the rectangle in screen percentage
      * width - The width of the rectangle
      * height - The height of the rectangle
      * line_width - The line width of the edges
      * fill (optional) - Whether or not to fill the rectangle
    """
    new_patch = Rectangle((x_coord, y_coord), width, height, fill=fill, linewidth=line_width)
    return new_patch

def build_square(x_coord, y_coord, dimension, line_width, fill=False):
    """
    Returns a Matplotlib Rectangle Patch in the shape of a Square

    Parameters :
      * x_coord - The x coordinate for the top left corner of the rectangle in screen percentage
      * y_coord - The y coordinate for the top left corner of the rectangle in screen percentage
      * dimension - The dimension of the square
      * line_width - The line width of the edges
      * fill (optional) - Whether or not to fill the square
    """
    new_patch = build_rectangle(x_coord, y_coord, dimension, dimension, line_width, fill)
    return new_patch

def build_wedge(x_coord, y_coord, radius, theta1, theta2, wedge_width, fill=False):
    """
    Returns a Matplotlib Wedge Patch from the provided parameters

    Parameters :
      * x_coord - The x coordinate for the top left corner of the rectangle in screen percentage
      * y_coord - The y coordinate for the top left corner of the rectangle in screen percentage
      * radius - The radius of the wedge
      * theta1 - The angle of the wedge at the start point
      * theta2 - The angle of the wedge at the end point
      * fill (optional) - Whether or not to fill the wedge
    """
    new_patch = Wedge([x_coord, y_coord], radius, theta1, theta2, wedge_width, fill=fill)
    return new_patch

def build_patch_collection(patches, visible=False):
    """
    Returns a Matplotlib Patch Collection

    Parameters :
      * patches - Array of patches to include in the Patch Collection
      * visible (optional) - Whether or not the Patch Collection is visible
    """
    patch_collection = PatchCollection(patches, True)
    patch_collection.set_visible(visible)
    return patch_collection
