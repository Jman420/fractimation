import numpy

from complex_polynomial import ComplexPolynomialIterable
from ..data_models.formula_params import FormulaParams
from ..data_models.complex_range import ComplexRange

_MANDELBROT_POWER = 2
_DEFAULT_Z_VALUES_RANGE = ComplexRange(0, 0)

class Multibrot(ComplexPolynomialIterable):
    """description of class"""

    def __init__(self, c_values_range, escape_value, z_values_range=_DEFAULT_Z_VALUES_RANGE, power=_MANDELBROT_POWER, max_iterations=None):
        coefficientArray = numpy.zeros(power, dtype=int)
        coefficientArray[0] = 1
        coefficientArray[-1] = 1

        formula_params = FormulaParams(coefficient_array, escape_value)

        super().__init__(z_values_range, c_values_range, formula_params, max_iterations)
