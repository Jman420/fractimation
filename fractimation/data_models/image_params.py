DEFAULT_COLOR_MAP = "viridis"

class ImageParams(object):
    """description of class"""

    width = None
    height = None
    color_map = None

    def __init__(self, width, height, color_map=DEFAULT_COLOR_MAP):
        self.width = width
        self.height = height
        self.color_map = color_map
