# http://pi3.sites.sheffield.ac.uk/tutorials/week-1-fibonacci
# http://junilyd.github.io/blog/2014/08/13/fibonacci-mystery-pythonified/

import numpy

from .base.cached_patch_collection_renderer import CachedPatchCollectionRenderer
from ..helpers.render import build_square, build_patch_collection
from ..helpers.fractal_algorithm import get_fibonocci_number

X_VALUE_INDEX = 0
Y_VALUE_INDEX = 1
SIZE_SCALAR = 0.1
INITIAL_LOCATION = [0, 0]

class FibonacciSquare(CachedPatchCollectionRenderer):
    """Fractal Renderer for Fibonocci Squares"""

    _size_scalar = None
    _line_widths = None
    _next_square_location = None
    _next_move_mode = None

    def __init__(self, line_widths, size_scalar=SIZE_SCALAR):
        self.initialize(line_widths, size_scalar)

    def initialize(self, line_widths, size_scalar=SIZE_SCALAR):
        super().initialize()

        self._line_widths = line_widths
        self._size_scalar = size_scalar

        empty_patches = build_patch_collection([])
        self._render_cache.update({0 : empty_patches})

        self._next_iteration_index = 1
        self._next_square_location = numpy.array(INITIAL_LOCATION)
        self._next_move_mode = 1

    def preheat_render_cache(self, max_iterations):
        print("Preheating Fibonocci Square Render Cache")
        super().preheat_render_cache(max_iterations)

    def iterate(self):
        current_fib_number = get_fibonocci_number(self._next_iteration_index) * self._size_scalar
        square_location = self._next_square_location

        second_prev_fib_num = (get_fibonocci_number(self._next_iteration_index - 2) *
                               self._size_scalar)
        prev_fib_num = get_fibonocci_number(self._next_iteration_index - 1) * self._size_scalar
        if self._next_move_mode == 1:
            move_deviation = [-second_prev_fib_num, prev_fib_num]
        elif self._next_move_mode == 2:
            move_deviation = [-current_fib_number, -second_prev_fib_num]
        elif self._next_move_mode == 3:
            move_deviation = [0, -current_fib_number]
        elif self._next_move_mode == 4:
            move_deviation = [prev_fib_num, 0]

        self._next_square_location = square_location + move_deviation
        line_width = self._line_widths[self._next_iteration_index]
        new_square = build_square(self._next_square_location[X_VALUE_INDEX],
                                  self._next_square_location[Y_VALUE_INDEX],
                                  current_fib_number, line_width)
        patch_collection = build_patch_collection([new_square])
        self._render_cache.update({self._next_iteration_index : patch_collection})

        self._next_iteration_index += 1
        self._next_move_mode += 1
        if self._next_move_mode > 4:
            self._next_move_mode = 1
