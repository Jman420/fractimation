import numpy

from .base.fractal_formula import FractalFormulaIterable, FractalFormulaIterator

from ..helpers.fractal_algorithm import evaluate_polynomial_1d
from ..helpers.list_tools import remove_indexes

_FRACTAL_NAME = "Generic Complex Polynomial"

class ComplexPolynomialIterable(FractalFormulaIterable):

    def get_fractal_name(self):
        return _FRACTAL_NAME

    def __iter__(cls):
        return ComplexPolynomialIterator(cls)

class ComplexPolynomialIterator(FractalFormulaIterator):

    def __next__(cls):
        super().__next__()

        if len(cls._z_values) < 1:
            return None

        formula_params = cls._formula_iterable.get_formula_params()
        z_values_new = evaluate_polynomial_1d(formula_params.coefficient_array,
                                              cls._z_values,
                                              cls._c_values)

        exploded_indexes = numpy.abs(z_values_new) > formula_params.escape_value

        remaining_indexes = ~exploded_indexes
        reduced_arrays = remove_indexes([z_values_new, cls._c_values], remaining_indexes)
        cls._z_values, cls._c_values = reduced_arrays
        
        cls._next_iteration += 1
        return ComplexPolynomialIterationData(z_values_new, exploded_indexes, remaining_indexes)

class ComplexPolynomialIterationData(object):

    z_values = None
    exploded_indexes = None
    remaining_indexes = None

    def __init__(self, z_values, exploded_indexes, remaining_indexes):
        self.z_values = z_values
        self.exploded_indexes = exploded_indexes
        self.remaining_indexes = remaining_indexes

    def get_z_values(self):
        return self.z_values

    def get_exploded_indexes(self):
        return self.exploded_indexes

    def get_remaining_indexes(self):
        return self.remaining_indexes
