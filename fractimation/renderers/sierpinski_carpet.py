# https://en.wikipedia.org/wiki/Sierpinski_carpet

import numpy

from .base.cached_patch_collection_renderer import CachedPatchCollectionRenderer
from ..helpers.render import build_rectangle, build_patch_collection

X_VALUE_INDEX = 0
Y_VALUE_INDEX = 1
WIDTH_INDEX = 2
HEIGHT_INDEX = 3
INITIAL_RECTS = [[0.01, 0.01, 0.98, 0.98]]

def calculate_subdivisions(rectangles):
    first_rect = rectangles[0]
    one_third_width = first_rect[WIDTH_INDEX] * (1 / 3)
    two_thirds_width = first_rect[WIDTH_INDEX] * (2 / 3)
    one_third_height = first_rect[HEIGHT_INDEX] * (1 / 3)
    two_thirds_height = first_rect[HEIGHT_INDEX] * (2 / 3)

    # Top Subdivisions
    top_right_subdivision = rectangles + [0, 0,
                                          -two_thirds_width, -two_thirds_height]
    top_middle_subdivision = rectangles + [one_third_width, 0,
                                           -two_thirds_width, -two_thirds_height]
    top_left_subdivision = rectangles + [two_thirds_width, 0,
                                         -two_thirds_width, -two_thirds_height]

    # Middle Subdivisions
    middle_right_subdivision = rectangles + [0, one_third_height,
                                             -two_thirds_height, -two_thirds_height]
    middle_left_subdivision = rectangles + [two_thirds_width, one_third_height,
                                            -two_thirds_height, -two_thirds_height]

    # Bottom Subdivisions
    bottom_left_subdivision = rectangles + [0, two_thirds_height,
                                            -two_thirds_height, -two_thirds_height]
    bottom_middle_subdivision = rectangles + [one_third_width, two_thirds_height,
                                              -two_thirds_height, -two_thirds_height]
    bottom_right_subdivision = rectangles + [two_thirds_width, two_thirds_height,
                                             -two_thirds_height, -two_thirds_height]

    all_subdivisions = numpy.concatenate((top_left_subdivision, top_middle_subdivision,
                                          top_right_subdivision,
                                          middle_left_subdivision, middle_right_subdivision,
                                          bottom_left_subdivision, bottom_middle_subdivision,
                                          bottom_right_subdivision))
    return all_subdivisions

class SierpinskiCarpet(CachedPatchCollectionRenderer):
    """Fractal Renderer for Sierpinski Carpet (aka Sierpinski Square)"""

    _eligible_rects = None
    _line_widths = None

    def __init__(self, line_widths, eligible_rects=None):
        self.initialize(line_widths, eligible_rects)

    # eligibleRects is an array of arrays of x, y, width and height describing the initial
    #   rectangles as percentages of screen space.
    def initialize(self, line_widths, eligible_rects=None):
        super().initialize()

        self._line_widths = line_widths

        if eligible_rects is None:
            eligible_rects = INITIAL_RECTS
        self._eligible_rects = numpy.array(eligible_rects)

        initial_patches = []
        for eligible_rect in eligible_rects:
            new_patch = build_rectangle(eligible_rect[X_VALUE_INDEX], eligible_rect[Y_VALUE_INDEX],
                                        eligible_rect[WIDTH_INDEX], eligible_rect[HEIGHT_INDEX],
                                        line_widths[0])
            initial_patches.append(new_patch)

        initial_patch_collection = build_patch_collection(initial_patches)
        self._render_cache.update({0 : initial_patch_collection})

        self._next_iteration_index = 1

    def preheat_render_cache(self, max_iterations):
        print("Preheating Sierpinski Carpet Render Cache")
        super().preheat_render_cache(max_iterations)

    def iterate(self):
        if (len(self._eligible_rects)) < 1:
            return

        new_rectangle_patches = []
        subdivisions = calculate_subdivisions(self._eligible_rects)
        line_width = self._line_widths[self._next_iteration_index]
        for new_rect in subdivisions:
            new_patch = build_rectangle(new_rect[X_VALUE_INDEX], new_rect[Y_VALUE_INDEX],
                                        new_rect[WIDTH_INDEX], new_rect[HEIGHT_INDEX], line_width)
            new_rectangle_patches.append(new_patch)

        iteration_patch_collection = build_patch_collection(new_rectangle_patches)
        self._render_cache.update({self._next_iteration_index : iteration_patch_collection})

        self._eligible_rects = subdivisions
        self._next_iteration_index += 1
