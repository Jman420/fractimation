import numpy

from .complex_polynomial import ComplexPolynomialIterable
from ..data_models.formula_params import FormulaParams
from ..data_models.complex_range import ComplexRange

_MANDELBROT_POWER = 2

class Multibrot(ComplexPolynomialIterable):
    """description of class"""

    def __init__(self, c_values_range, escape_value, power=_MANDELBROT_POWER, z_values_range=None,
                 max_iterations=None):
        if z_values_range is None:
            range_shape = [len(c_values_range.real_number_values),
                           len(c_values_range.real_number_values[0])]
            real_zeros = numpy.zeros(range_shape, int)
            imaginary_zeros = numpy.zeros(range_shape, int)

            z_values_range = ComplexRange(real_zeros, imaginary_zeros)

        coefficient_array = numpy.zeros(power + 1, dtype=int)
        coefficient_array[0] = 1
        coefficient_array[-1] = 1

        formula_params = FormulaParams(coefficient_array, escape_value)

        super().__init__(z_values_range, c_values_range, formula_params, max_iterations)
