import numpy

from .base.cached_image_renderer import CachedImageRenderer
from .functionality.zoomable_complex_range import ZoomableComplexRange
from ..helpers.fractal_algorithm import evaluate_polynomial_1d
from ..helpers.list_tools import update_indexes_with_value, remove_indexes

class ComplexPolynomial(CachedImageRenderer, ZoomableComplexRange):
    """Fractal Renderer for Generic Complex Polynomial Equations"""

    _constant_real_number = None
    _constant_imaginary_number = None
    _coefficient_array = None
    _escape_value = None

    _z_values = None
    _c_value = None

    def __init__(self, width, height, real_number_min, real_number_max, imaginary_number_min,
                 imaginary_number_max, coefficient_array, constant_real_number,
                 constant_imaginary_number, escape_value, color_map="viridis"):
        CachedImageRenderer.__init__(self)
        ZoomableComplexRange.__init__(self)

        self.initialize(width, height, real_number_min, real_number_max, imaginary_number_min,
                        imaginary_number_max, coefficient_array, constant_real_number,
                        constant_imaginary_number, escape_value, color_map)

    def initialize(self, width, height, real_number_min, real_number_max, imaginary_number_min,
                   imaginary_number_max, coefficient_array, constant_real_number,
                   constant_imaginary_number, escape_value, color_map="viridis"):
        # Setup Included Indexes and the Real and Imaginary Number Spaces
        ZoomableComplexRange.initialize(self, width, height, real_number_min, real_number_max,
                                        imaginary_number_min, imaginary_number_max)

        # Calculate C Value and Initial Z Values
        c_value = numpy.complex(constant_real_number, constant_imaginary_number)

        z_values = numpy.multiply(numpy.complex(0, 1), self._imaginary_number_values)
        z_values = numpy.add(z_values, self._real_number_values)

        self._z_values = z_values
        self._c_value = c_value

        # Initialize Image Cache
        CachedImageRenderer.initialize(self, width, height, z_values.shape, color_map)

        self._constant_real_number = constant_real_number
        self._constant_imaginary_number = constant_imaginary_number
        self._coefficient_array = coefficient_array
        self._escape_value = escape_value

    def reinitialize(self):
        self.initialize(self._width, self._height, self._min_real_number, self._max_real_number,
                        self._min_imaginary_number, self._max_imaginary_number,
                        self._coefficient_array, self._constant_real_number,
                        self._constant_imaginary_number, self._escape_value, self._color_map)

    def preheat_render_cache(self, max_iterations):
        print("Preheating Generic Complex Polynomial Render Cache")
        super().preheat_render_cache(max_iterations)

    def iterate(self):
        if len(self._z_values) <= 0:
            # Nothing left to calculate, so just store the last image in the cache
            final_image = self._render_cache[len(self._render_cache) - 1]
            self._render_cache.update({self._next_iteration_index : final_image})
            self._next_iteration_index += 1
            return

        # Evaluate Polynomial
        z_values_new = evaluate_polynomial_1d(self._coefficient_array, self._z_values,
                                              self._c_value)

        # Update indexes which have exceeded the Escape Value
        exploded_indexes = numpy.abs(z_values_new) > self._escape_value
        x_indexes = self._x_indexes[exploded_indexes]
        y_indexes = self._y_indexes[exploded_indexes]
        self._image_array[x_indexes, y_indexes] = self._next_iteration_index

        # Recolor Indexes which have not exceeded the Escape Value
        recolored_image = update_indexes_with_value(self._image_array, -1,
                                                    self._next_iteration_index + 1)
        final_image = recolored_image.T

        # Update cache and prepare for next iteration
        self._render_cache.update({self._next_iteration_index : final_image})
        self._next_iteration_index += 1

        # Remove Exploded Indexes since we don't need to calculate them anymore
        remaining_indexes = ~exploded_indexes
        reducable_arrays = [self._x_indexes, self._y_indexes, z_values_new]
        self._x_indexes, self._y_indexes, self._z_values = remove_indexes(reducable_arrays,
                                                                          remaining_indexes)
