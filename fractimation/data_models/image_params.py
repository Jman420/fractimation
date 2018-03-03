"""
Fractimation specific Image Parameters Class

Public Classes :
  * ImageParams - Represents the parameters associated with a Fractimation Image
"""

_DEFAULT_COLOR_MAP = "viridis"
_DEFAULT_IMAGE_ARRAY_VALUE = -1

class ImageParams(object):
    """
    Parameters for initializing a Fractimation Image

    Public Attributes :
      * width - The width of the image
      * heigh - The height of the image
      * color_map - A color map to be applied to the image
    """

    color_map = None
    initial_value = None
    recolor_image = None

    def __init__(self, color_map=_DEFAULT_COLOR_MAP, initial_value=_DEFAULT_IMAGE_ARRAY_VALUE,
                 recolor_image=False):
        """
        Constructor

        Parameters :
          * width - The width of the image
          * heigh - The height of the image
          * color_map - A color map to be applied to the image
        """
        self.color_map = color_map
        self.initial_value = initial_value
        self.recolor_image = recolor_image

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_color_map(self):
        return self.color_map

    def get_initial_value(self):
        return self.initial_value

    def get_recolor_image(self):
        return self.recolor_image
