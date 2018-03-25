import numpy

from .base.fractal_formula import FractalFormulaIterable, FractalFormulaIterator

from ..data_models.complex_polynomial_iteration_data import ComplexPolynomialIterationData

from ..helpers.fractal_algorithm import evaluate_polynomial_1d
from ..helpers.list_tools import remove_indexes

_FRACTAL_NAME = "Generic Complex Polynomial"

class ComplexPolynomialIterable(FractalFormulaIterable):

    def get_fractal_name(self):
        return _FRACTAL_NAME

    def __iter__(cls):
        return ComplexPolynomialIterator(cls._z_values_range, cls._c_values_range,
                                         cls._formula_params, cls._max_iterations)

class ComplexPolynomialIterator(FractalFormulaIterator):

    _formula_params = None

    def __init__(self, z_values_range, c_values_range, formula_params, max_iterations = None):
        super().__init__(z_values_range, c_values_range, max_iterations)

        self._formula_params = formula_params

    def __next__(cls):
        super().__next__()

        if len(cls._z_values) < 1:
            return None

        formula_params = cls._formula_params
        z_values_new = evaluate_polynomial_1d(formula_params.coefficient_array,
                                              cls._z_values,
                                              cls._c_values)

        exploded_indexes = numpy.abs(z_values_new) > formula_params.escape_value
        remaining_indexes = ~exploded_indexes
        reduced_arrays = remove_indexes([z_values_new, cls._c_values], remaining_indexes)
        cls._z_values = reduced_arrays[0]
        cls._c_values = reduced_arrays[1]
        
        cls._next_iteration += 1
        return ComplexPolynomialIterationData(z_values_new, exploded_indexes, remaining_indexes)
