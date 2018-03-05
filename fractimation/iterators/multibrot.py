import numpy

from .complex_polynomial import ComplexPolynomialIterable
from ..data_models.formula_params import FormulaParams
from ..data_models.complex_range_params import ComplexRangeParams

_MANDELBROT_POWER = 2
_FRACTAL_NAME = "Multibrot"

class Multibrot(ComplexPolynomialIterable):

    def __init__(self, c_values_range_params, dimension_params, escape_value,
                 power=_MANDELBROT_POWER, z_values_range_params=None, max_iterations=None):
        if z_values_range_params is None:
            z_values_range_params = ComplexRangeParams(0, 0, 0, 0)

        coefficient_array = numpy.zeros(power + 1, dtype=int)
        coefficient_array[0] = 1
        coefficient_array[-1] = 1

        formula_params = FormulaParams(coefficient_array, escape_value)

        super().__init__(z_values_range_params, c_values_range_params, dimension_params,
                         formula_params, max_iterations)

    def get_fractal_name(self):
        return _FRACTAL_NAME
