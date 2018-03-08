import numpy
from numpy.polynomial.polynomial import polyder

from .base.fractal_formula import FractalFormulaIterable, FractalFormulaIterator
from ..data_models.formula_params import FormulaParams
from ..data_models.complex_range_params import ComplexRangeParams
from ..data_models.complex_polynomial_iteration_data import ComplexPolynomialIterationData
from ..helpers.fractal_algorithm import newton_method_algorithm
from ..helpers.list_tools import remove_indexes

_FRACTAL_NAME = "Newton Method"

class NewtonMethod(FractalFormulaIterable):

    _coefficient_array_deriv = None

    def __init__(self, z_values_range_params, c_values_range_params, dimension_params,
                 formula_params, max_iterations = None):
        super().__init__(z_values_range_params, c_values_range_params, dimension_params,
                         formula_params, max_iterations)

        self._coefficient_array_deriv = polyder(self._formula_params.coefficient_array)

    def __iter__(cls):
        return NewtonMethodIterator(cls._z_values_range, cls._c_values_range, cls._formula_params,
                                    cls._coefficient_array_deriv, cls._max_iterations)

    def get_fractal_name(self):
        return _FRACTAL_NAME

class NewtonMethodIterator(FractalFormulaIterator):

    _formula_params = None
    _coefficient_array_deriv = None

    def __init__(self, z_values_range, c_values_range, formula_params, coefficient_array_deriv,
                 max_iterations = None):
        super().__init__(z_values_range, c_values_range, max_iterations)

        self._formula_params = formula_params
        self._coefficient_array_deriv = coefficient_array_deriv

    def __next__(cls):
        super().__next__()

        if len(cls._z_values) < 1:
            return None

        formula_params = cls._formula_params
        coefficient_array_deriv = cls._coefficient_array_deriv
        newton_method_result = newton_method_algorithm(formula_params.coefficient_array,
                                                       coefficient_array_deriv, cls._z_values,
                                                       cls._c_values)
        iteration_diff = newton_method_result[0]
        z_values_new = newton_method_result[1]

        exploded_indexes = numpy.abs(iteration_diff) < formula_params.escape_value
        remaining_indexes = ~exploded_indexes
        reduced_arrays = remove_indexes([z_values_new, cls._c_values], remaining_indexes)
        cls._z_values, cls._c_values = reduced_arrays
        
        cls._next_iteration += 1
        return ComplexPolynomialIterationData(iteration_diff, exploded_indexes, remaining_indexes)
