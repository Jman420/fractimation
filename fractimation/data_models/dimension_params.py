class DimensionParams(object):
    """description of class"""

    width = None
    height = None

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height
