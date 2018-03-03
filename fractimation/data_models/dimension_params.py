import numpy

class DimensionParams(object):
    """description of class"""

    width = None
    height = None
    x_indexes = None
    y_indexes = None

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.x_indexes, self.y_indexes = numpy.mgrid[0:width, 0:height]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_x_indexes(self):
        return self.x_indexes

    def get_y_indexes(self):
        return self.y_indexes
