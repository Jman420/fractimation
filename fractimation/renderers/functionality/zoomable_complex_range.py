from abc import ABC, abstractmethod
import numpy

class ZoomableComplexRange(ABC):
    """Base Class for Zoomable Complex Polynomial Fractal Equation Renderers"""

    _x_indexes = None
    _y_indexes = None
    _min_real_number = None
    _max_real_number = None
    _min_imaginary_number = None
    _max_imaginary_number = None
    _real_number_values = None
    _imaginary_number_values = None

    _zoom_cache = None

    def __init__(self):
        self._zoom_cache = []

    def initialize(self, width, height, min_real_number, max_real_number, min_imaginary_number,
                   max_imaginary_number, spacing_func=numpy.linspace):
        x_indexes, y_indexes = numpy.mgrid[0:width, 0:height]

        real_number_values = spacing_func(min_real_number, max_real_number, width)[x_indexes]
        imaginary_number_values = spacing_func(min_imaginary_number, max_imaginary_number,
                                               height)[y_indexes]

        self._x_indexes = x_indexes
        self._y_indexes = y_indexes
        self._min_real_number = min_real_number
        self._max_real_number = max_real_number
        self._min_imaginary_number = min_imaginary_number
        self._max_imaginary_number = max_imaginary_number
        self._real_number_values = real_number_values
        self._imaginary_number_values = imaginary_number_values

    def zoom_in(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        prev_zoom = ZoomCacheItem(self._min_real_number, self._max_real_number,
                                  self._min_imaginary_number, self._max_imaginary_number)

        min_real_number = self._real_number_values[top_left_x][top_left_y]
        max_real_number = self._real_number_values[bottom_right_x][bottom_right_y]
        min_imaginary_number = self._imaginary_number_values[top_left_x][top_left_y]
        max_imaginary_number = self._imaginary_number_values[bottom_right_x][bottom_right_y]
        print("ZoomIn Parameters (minReal, maxReal) -> (minImaginary, maxImaginary) : ({}, {})" +
              " -> ({}, {})".format(min_real_number, max_real_number, min_imaginary_number,
                                    max_imaginary_number))

        self._min_real_number = min_real_number
        self._max_real_number = max_real_number
        self._min_imaginary_number = min_imaginary_number
        self._max_imaginary_number = max_imaginary_number

        self.reinitialize()
        self._zoom_cache.append(prev_zoom)

    def zoom_out(self):
        if len(self._zoom_cache) < 1:
            return False

        prev_zoom = self._zoom_cache.pop()
        print("ZoomOut Parameters (minReal, maxReal) -> (minImaginary, maxImaginary) : ({}, {})" +
              " -> ({}, {})".format(prev_zoom.min_real_number, prev_zoom.max_real_number,
                                    prev_zoom.min_imaginary_number, prev_zoom.max_imaginary_number))

        self._min_real_number = prev_zoom.min_real_number
        self._max_real_number = prev_zoom.max_real_number
        self._min_imaginary_number = prev_zoom.min_imaginary_number
        self._max_imaginary_number = prev_zoom.max_imaginary_number

        self.reinitialize()
        return True

    @abstractmethod
    def reinitialize(self):
        pass

class ZoomCacheItem(object):
    min_real_number = None
    max_real_number = None
    min_imaginary_number = None
    max_imaginary_number = None

    def __init__(self, min_real_number, max_real_number, min_imaginary_number,
                 max_imaginary_number):
        self.min_real_number = min_real_number
        self.max_real_number = max_real_number
        self.min_imaginary_number = min_imaginary_number
        self.max_imaginary_number = max_imaginary_number
