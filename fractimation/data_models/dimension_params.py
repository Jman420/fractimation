import numpy

class DimensionParams(object):

    width = None
    height = None
    x_indexes = None
    y_indexes = None

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.initialize()

    def initialize(self):
        x_indexes_grid, y_indexes_grid = numpy.mgrid[0:self.width, 0:self.height]

        self.x_indexes = x_indexes_grid
        self.y_indexes = y_indexes_grid

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_x_indexes(self):
        return self.x_indexes

    def get_y_indexes(self):
        return self.y_indexes
