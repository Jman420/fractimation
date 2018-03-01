# https://stackoverflow.com/questions/17393592/how-do-i-speed-up-fractal-generation-with-numpy-arrays
# https://austingwalters.com/newtons-method-and-fractals/

import numpy
import numpy.polynomial.polynomial as numpynomial

from .complex_polynomial import ComplexPolynomial
from ..helpers.fractal_algorithm import newton_method_algorithm
from ..helpers.list_tools import remove_indexes

class NewtonFractal(ComplexPolynomial):
    """Fractal Renderer for Newton Method Fractals"""
    
    _coefficient_array_deriv = None

    def __init__(self, width, height, real_number_min, real_number_max, imaginary_number_min, imaginary_number_max,
                initial_real_number, initial_imaginary_number, power, escape_value, color_map = 'viridis'):
        ComplexPolynomial.__init__(self, width, height, real_number_min, real_number_max, imaginary_number_min,
                                  imaginary_number_max, initial_real_number, initial_imaginary_number, power,
                                  escape_value, color_map)

        self.initialize(width, height, real_number_min, real_number_max, imaginary_number_min, imaginary_number_max,
                        initial_real_number, initial_imaginary_number, power, escape_value, color_map)
    
    def initialize(self, width, height, real_number_min, real_number_max, imaginary_number_min, imaginary_number_max,
                   initial_real_number, initial_imaginary_number, power, escape_value, color_map = 'viridis'):
        super().initialize(width, height, real_number_min, real_number_max, imaginary_number_min, imaginary_number_max,
                           initial_real_number, initial_imaginary_number, power, escape_value, color_map)

        self._coefficient_array_deriv = numpynomial.polyder(self._coefficient_array)

    def preheat_render_cache(self, max_iterations):
        print("Preheating Newton Fractal Render Cache")
        super().preheat_render_cache(max_iterations)

    def iterate(self):
        if len(self._z_values) <= 0:
            # Nothing left to calculate, so just store the last image in the cache
            final_image = self._render_cache[len(self._render_cache) - 1]
            self._render_cache.update({ self._next_iteration_index : final_image })
            self._next_iteration_index += 1
            return
        
        # Perform Newton Method
        iteration_diff, z_values_new = newton_method_algorithm(self._coefficient_array, 
                                                               self._coefficient_array_deriv,
                                                               self._z_values,
                                                               self._c_value)

        # Update indexes which have exceeded the Escape Value
        exploded_indexes = numpy.abs(iteration_diff) < self._escape_value
        self._image_array[self._x_indexes[exploded_indexes], self._y_indexes[exploded_indexes]] = self._next_iteration_index

        # Update cache and prepare for next iteration
        final_image = numpy.copy(self._image_array.T)
        self._render_cache.update({ self._next_iteration_index : final_image })
        self._next_iteration_index += 1

        # Remove Exploded Indexes since we don't need to calculate them anymore
        remaining_indexes = ~exploded_indexes
        self._x_indexes, self._y_indexes, self._z_values = remove_indexes([ self._x_indexes, self._y_indexes, z_values_new ],
                                                                          remaining_indexes)
