# Algorithm modified from : https://thesamovar.wordpress.com/2009/03/22/fast-fractals-with-python-and-numpy/
# Multibrot Fractal Definitions : 
#   C = realNumber + imaginaryNumber
#   Z = Z**power + C
#   Z0 = complex(initialRealNumber, initialImaginaryNumber) + C
# Multibrot Rendering Instructions :
#   - Map range of real and imaginary number values evenly to the image x and y pixel coordinates
#   - For each iteration 
#     * For each unexploded pixel in the image
#       @ Retrieve associated real and imaginary number values for pixel coordinates
#       @ Perform provided Multibrot equation variant
#       @ Set pixel value equal to number of iterations for Z to exceed the Escape Value
#     * Remove exploded pixel coordinates from calculation indexes

# Mandelbrot Parameters :
#realNumberMin, realNumberMax = -2.0, 0.5
#imaginaryNumberMin, imaginaryNumberMax = -1.25, 1.25
#constantRealNumber, constantImaginaryNumber = 0, 0
#power = 2
#escapeValue = 2.0

import numpy

from .base.cached_image_renderer import CachedImageRenderer
from .functionality.zoomable_complex_range import ZoomableComplexRange
from ..helpers.fractal_algorithm import multibrot_algorithm
from ..helpers.list_tools import update_indexes_with_value, remove_indexes

DEFAULT_COLOR_MAP = "viridis"

class Multibrot(CachedImageRenderer, ZoomableComplexRange):
    """Fractal Renderer for Multibrot Sets"""

    _initial_real_number = None
    _initial_imaginary_number = None
    _power = None
    _escape_value = None

    _z_values = None
    _c_values = None

    def __init__(self, width, height, real_number_min, real_number_max, imaginary_number_min, imaginary_number_max,
                initial_real_number, initial_imaginary_number, power, escape_value, color_map = DEFAULT_COLOR_MAP):
        CachedImageRenderer.__init__(self)
        ZoomableComplexRange.__init__(self)

        self.initialize(width, height, real_number_min, real_number_max, imaginary_number_min, imaginary_number_max,
                       initial_real_number, initial_imaginary_number, power, escape_value, color_map)

    def initialize(self, width, height, real_number_min, real_number_max, imaginary_number_min, imaginary_number_max,
                initial_real_number, initial_imaginary_number, power, escape_value, color_map = DEFAULT_COLOR_MAP):
        # Setup Included Indexes and the Real and Imaginary Number Spaces
        ZoomableComplexRange.initialize(self, width, height, real_number_min, real_number_max, imaginary_number_min,
                                        imaginary_number_max)

        # Calculate C Values and Initial Z Value
        c_values = numpy.multiply(numpy.complex(0,1), self._imaginary_number_values)
        c_values = numpy.add(c_values, self._real_number_values)

        z_values = numpy.add(numpy.complex(initial_real_number, initial_imaginary_number), c_values)

        self._z_values = z_values
        self._c_values = c_values

        # Initialize Image Cache
        CachedImageRenderer.initialize(self, width, height, c_values.shape, color_map)
        
        self._initial_real_number = initial_real_number
        self._initial_imaginary_number = initial_imaginary_number
        self._power = power
        self._escape_value = escape_value

    def reinitialize(self):
        self.initialize(self._width, self._height, self._min_real_number, self._max_real_number, self._min_imaginary_number,
                       self._max_imaginary_number, self._initial_real_number, self._initial_imaginary_number, self._power,
                       self._escape_value, self._color_map)

    def preheat_render_cache(self, max_iterations):
        print("Preheating Multibrot Render Cache")
        super().preheat_render_cache(max_iterations)

    def iterate(self):
        if len(self._z_values) <= 0:
            # Nothing left to calculate, so just store the last image in the cache
            final_image = self._render_cache[len(self._render_cache) - 1]
            self._render_cache.update({ self._nextIterationIndex : final_image })
            self._next_iteration_index += 1
            return

        # Apply Multibrot Algorithm
        z_values_new = multibrot_algorithm(self._z_values, self._c_values, self._power)

        # Update indexes which have exceeded the Escape Value
        exploded_indexes = numpy.abs(z_values_new) > self._escape_value
        self._image_array[self._x_indexes[exploded_indexes], self._y_indexes[exploded_indexes]] = self._next_iteration_index

        # Recolor Indexes which have not exceeded the Escape Value
        recolored_image = update_indexes_with_value(self._image_array, -1, self._next_iteration_index + 1)
        final_image = recolored_image.T

        # Update cache and prepare for next iteration
        self._render_cache.update({ self._next_iteration_index : final_image })
        self._next_iteration_index += 1

        # Remove Exploded Indexes since we don't need to calculate them anymore
        remaining_indexes = ~exploded_indexes
        self._x_indexes, self._y_indexes, self._z_values, self._c_values = remove_indexes([ self._x_indexes, self._y_indexes, z_values_new,
                                                                            self._c_values ], remaining_indexes)
