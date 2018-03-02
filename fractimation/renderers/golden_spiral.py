# http://pi3.sites.sheffield.ac.uk/tutorials/week-1-fibonacci
# http://junilyd.github.io/blog/2014/08/13/fibonacci-mystery-pythonified/

import numpy

from .base.cached_patch_collection_renderer import CachedPatchCollectionRenderer
from ..helpers.render import build_wedge, build_patch_collection
from ..helpers.fractal_algorithm import get_fibonocci_number

X_VALUE_INDEX = 0
Y_VALUE_INDEX = 1
THETA1_INDEX = 0
THETA2_INDEX = 1

SIZE_SCALAR = 0.1
INITIAL_LOCATION = [0, 0]
INITIAL_ANGLES = [270, 0]

class GoldenSpiral(CachedPatchCollectionRenderer):
    """Fractal Renderer for the Golden Spiral"""

    _size_scalar = None
    _line_widths = None
    _next_wedge_location = None
    _next_move_mode = None
    _next_wedge_angles = None

    def __init__(self, line_widths, size_scalar=SIZE_SCALAR):
        self.initialize(line_widths, size_scalar)

    def initialize(self, line_widths, size_scalar=SIZE_SCALAR):
        super().initialize()

        self._line_widths = line_widths
        self._size_scalar = size_scalar

        self._next_wedge_location = numpy.array(INITIAL_LOCATION)
        self._next_wedge_angles = numpy.array(INITIAL_ANGLES)
        self._next_move_mode = 1

        empty_patches = build_patch_collection([])
        self._render_cache.update({0 : empty_patches})

        self._next_iteration_index = 1

    def preheat_render_cache(self, max_iterations):
        print("Preheating Golden Spiral Render Cache")
        super().preheat_render_cache(max_iterations)

    def iterate(self):
        self._next_wedge_angles += 90
        current_fib_number = get_fibonocci_number(self._next_iteration_index) * self._size_scalar
        wedge_location = self._next_wedge_location

        second_prev_fib_num = (get_fibonocci_number(self._next_iteration_index - 2) *
                               self._size_scalar)
        if self._next_move_mode == 1:
            move_deviation = [-second_prev_fib_num, 0]
        elif self._next_move_mode == 2:
            move_deviation = [0, -second_prev_fib_num]
        elif self._next_move_mode == 3:
            move_deviation = [second_prev_fib_num, 0]
        elif self._next_move_mode == 4:
            move_deviation = [0, second_prev_fib_num]

        self._next_wedge_location = wedge_location + move_deviation
        line_width = self._line_widths[self._next_iteration_index]
        new_wedge = build_wedge(self._next_wedge_location[X_VALUE_INDEX],
                                self._next_wedge_location[Y_VALUE_INDEX], current_fib_number,
                                self._next_wedge_angles[THETA1_INDEX],
                                self._next_wedge_angles[THETA2_INDEX], line_width)
        patch_collection = build_patch_collection([new_wedge])
        self._render_cache.update({self._next_iteration_index : patch_collection})

        self._next_iteration_index += 1
        self._next_move_mode += 1
        if self._next_move_mode > 4:
            self._next_move_mode = 1
