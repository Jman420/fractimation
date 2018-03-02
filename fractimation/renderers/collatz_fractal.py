# http://www.njohnston.ca/2009/06/the-collatz-conjecture-as-a-fractal/
# https://github.com/sebhz/fractals/blob/master/mandelbrot/python/fractal.py#L27
# https://en.wikipedia.org/wiki/Collatz_conjecture
# https://glowingpython.blogspot.com/2011/06/collatz-conjecture.html

import numpy

from .base.cached_image_renderer import CachedImageRenderer
from .functionality.zoomable_complex_range import ZoomableComplexRange

# z = (2 + 7z - (2 + 5z) * cos(pi * z)) / 4
def collatz_conjecture_algorithm(z_values, c_values):
    two_plus_five_z = numpy.add(numpy.multiply(z_values, 5), 2)
    cos_pi_z = numpy.cos(numpy.multiply(z_values, numpy.pi))

    seven_z = numpy.multiply(z_values, 7)
    cos_product = numpy.multiply(two_plus_five_z, cos_pi_z)

    two_plus_seven_z = numpy.add(seven_z, 2)

    left_paren_val = numpy.subtract(two_plus_seven_z, cos_product)
    z_values_new = numpy.divide(left_paren_val, 4)

    return z_values_new

class CollatzFractal(CachedImageRenderer, ZoomableComplexRange):
    """Fractal Renderer for Collatz Conjecture Fractals"""

    _escape_value = None
    _z_values = None
    _c_value = None

    def __init__(self, width, height, real_number_min, real_number_max, imaginary_number_min,
                 imaginary_number_max, escape_value, color_map="viridis"):
        super().__init__()

    def initialize(self, width, height, image_array_shape, color_map,
                   initial_image_array_value=-1):
        return super().initialize(width, height, image_array_shape, color_map,
                                  initial_image_array_value)

    def reinitialize(self):
        return super().reinitialize()

    def iterate(self):
        return super().iterate()

    def preheat_render_cache(self, max_iterations):
        print("Preheating Collatz Fractal Render Cache")
        super().preheat_render_cache(max_iterations)
