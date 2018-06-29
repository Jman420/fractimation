import numpy

from .base.fractal_formula import FractalFormulaIterable, FractalFormulaIterator, ROWS_INDEX, COLUMNS_INDEX
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

        # use numpy.where() to get remaining indexes
        formula_params = cls._formula_params

        # condition check for early exit (no indexes to calculate)
        if len(cls._remaining_indexes[ROWS_INDEX]) < 1:
            return None

        # get remaining z & c values
        remaining_z_values = cls._z_values[cls._remaining_indexes]
        remaining_c_values = cls._c_values[cls._remaining_indexes]

        # evaluate polynomial
        new_z_values = evaluate_polynomial_1d(formula_params.coefficient_array,
                                              remaining_z_values,
                                              remaining_c_values)

        # update remaining index z values
        cls._z_values[cls._remaining_indexes] = new_z_values

        # calculate new exploded indexes
        exploded_new_indexes = numpy.where(numpy.abs(new_z_values) > formula_params.escape_value)
        exploded_rows = cls._remaining_indexes[ROWS_INDEX][exploded_new_indexes]
        exploded_cols = cls._remaining_indexes[COLUMNS_INDEX][exploded_new_indexes]
        exploded_indexes = (exploded_rows, exploded_cols)

        # calculate new remaining indexes
        remaining_rows = numpy.delete(cls._remaining_indexes[ROWS_INDEX], exploded_new_indexes)
        remaining_cols = numpy.delete(cls._remaining_indexes[COLUMNS_INDEX], exploded_new_indexes)
        cls._remaining_indexes = (remaining_rows, remaining_cols)

        # return z values and exploded indexes
        cls._next_iteration += 1
        return ComplexPolynomialIterationData(cls._z_values, exploded_indexes, cls._remaining_indexes)

    def set_z_values(self, new_z_values):
        self._z_values = new_z_values
        self._remaining_indexes = numpy.where(numpy.abs(self._z_values) < self._formula_params.ecape_value)

    def set_c_values(self, new_c_values):
        self._c_values = new_c_values
