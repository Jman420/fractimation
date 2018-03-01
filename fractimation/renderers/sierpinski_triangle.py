# https://en.wikipedia.org/wiki/Sierpinski_triangle

import numpy

from .base.cached_patch_collection_renderer import CachedPatchCollectionRenderer
from ..helpers.render import build_triangle, build_patch_collection

LAST_VERTEX_INDEX = 2
FIRST_VERTEX_INDEX = 0
X_VALUE_INDEX = 0
INITIAL_ELIGIBLE_VERTICES = [ 
                                [ 0, 0 ],
                                [ 0.5, 1 ],
                                [ 1, 0 ]
                            ]

def calculate_subdivisions(vertices):
    first_triangle = vertices[0]
    large_subdivision = (first_triangle[LAST_VERTEX_INDEX, X_VALUE_INDEX] - first_triangle[FIRST_VERTEX_INDEX, X_VALUE_INDEX]) / 2
    small_subdivision = large_subdivision / 2

    left_subdivision_mod = [
                            [ 0, 0 ],
                            [ -small_subdivision, -large_subdivision ],
                            [ -large_subdivision, 0 ]
                         ]
    top_subdivision_mod = [
                            [ small_subdivision, large_subdivision ],
                            [ 0, 0 ],
                            [ -small_subdivision, large_subdivision ]
                        ]
    right_subdivision_mod = [
                            [ large_subdivision, 0 ],
                            [ small_subdivision, -large_subdivision ],
                            [ 0, 0 ]
                          ]

    left_subdivision = vertices + left_subdivision_mod
    top_subdivision = vertices + top_subdivision_mod
    right_subdivision = vertices + right_subdivision_mod

    return numpy.concatenate((left_subdivision, top_subdivision, right_subdivision))

class SierpinskiTriangle(CachedPatchCollectionRenderer):
    """Fractal Renderer for Sierpinski Triangle"""

    _eligible_vertices = None
    _line_widths = None

    def __init__(self, line_widths, eligible_rects=None):
        self.initialize(line_widths, eligible_rects)

    # eligibleVertices is an array of three vertices that describe the points of a triangle as percentages of screen space.
    #    These vertices must be defined from left to right; ie. [ [ left vertex ], [ top vertex ], [ right vertex ] ]
    def initialize(self, line_widths, eligible_vertices=None):
        super().initialize()

        self._line_widths = line_widths
        
        if eligible_vertices == None:
            eligible_vertices = INITIAL_ELIGIBLE_VERTICES
        self._eligible_vertices = numpy.array([ eligible_vertices ])

        initial_patches = [ ]
        for eligible_triangle in self._eligible_vertices:
            new_patch = build_triangle(eligible_triangle, lineWidth=line_widths[0])
            initial_patches.append(new_patch)

        self._render_cache = { }
        initial_patch_collection = build_patch_collection(initial_patches)
        self._render_cache.update({ 0 : initial_patch_collection })

        self._cache_added_to_axes = False
        self._next_iteration_index = 1

    def preheat_render_cache(self, max_iterations):
        print("Preheating Sierpinski Triangle Render Cache")
        super().preheat_render_cache(max_iterations)

    def iterate(self):
        if len(self._eligible_vertices) < 1:
            return
        
        new_triangle_patches = [ ]
        new_subdivisions = calculate_subdivisions(self._eligible_vertices)
        line_width = self._line_widths[self._next_iteration_index]
        for triangleVertices in new_subdivisions:
            new_patch = build_triangle(triangleVertices, line_width)
            new_triangle_patches.append(new_patch)

        iteration_patch_collection = build_patch_collection(new_triangle_patches)
        self._render_cache.update({ self._next_iteration_index : iteration_patch_collection })

        self._eligible_vertices = new_subdivisions
        self._next_iteration_index += 1
