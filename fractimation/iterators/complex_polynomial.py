import numpy

from .base.fractal_formula import FractalFormulaIterable, FractalFormulaIterator

from ..helpers.fractal_algorithm import evaluate_polynomial_1d
from ..helpers.list_tools import remove_indexes

class ComplexPolynomialIterable(FractalFormulaIterable):
    
    def __iter__(cls):
        return ComplexPolynomialIterator(cls)

class ComplexPolynomialIterator(FractalFormulaIterator):

    def __next__(cls):
        max_iterations = cls._formula_iterable.get_max_iterations()
        if len(cls._z_values) < 1 or (max_iterations is not None and 
                                      cls._next_iteration >= max_iterations):
            raise StopIteration

        formula_params = cls._formula_iterable.get_formula_params()
        z_values_new = evaluate_polynomial_1d(formula_params.coefficient_array, cls._z_values,
                                              cls._c_values)

        remaining_indexes = numpy.abs(z_values_new) > formula_params.escape_value

        reduced_arrays = remove_indexes([z_values_new, cls._c_values], remaining_indexes)
        cls._z_values, cls._c_values = reduced_arrays
        cls._next_iteration += 1

        return [z_values_new, remaining_indexes]
