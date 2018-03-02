"""
Fractimation specific Image Parameters Class

Public Constants :
  * DEFAULT_COLOR_MAP - Default color map used if none is specified

Public Classes :
  * ImageParams - Represents the parameters associated with a Fractimation Image
"""

DEFAULT_COLOR_MAP = "viridis"

class ImageParams(object):
    """
    Parameters for initializing a Fractimation Image

    Public Attributes :
      * width - The width of the image
      * heigh - The height of the image
      * color_map - A color map to be applied to the image
    """

    width = None
    height = None
    color_map = None

    def __init__(self, width, height, color_map=DEFAULT_COLOR_MAP):
        """
        Constructor

        Parameters :
          * width - The width of the image
          * heigh - The height of the image
          * color_map - A color map to be applied to the image
        """
        self.width = width
        self.height = height
        self.color_map = color_map
