from abc import ABC, abstractclassmethod
from collections.abc import Iterable, Iterator

import numpy

class FractalFormulaIterable(Iterable, ABC):
    """description of class"""

    _max_iterations = None
    _z_values_range = None
    _c_values_range = None
    _formula_params = None

    def __init__(self, z_values_range, c_values_range, formula_params, max_iterations=None):
        self._max_iterations = max_iterations
        self._z_values_range = z_values_range
        self._c_values_range = c_values_range
        self._formula_params = formula_params

    def get_max_iterations(self):
        return self._max_iterations

    def get_z_values_range(self):
        return self._z_values_range

    def get_c_values_range(self):
        return self._c_values_range

    def get_formula_params(self):
        return self._formula_params

    @abstractclassmethod
    def __iter__(cls):
        return super().__iter__()

class FractalFormulaIterator(Iterator, ABC):
    """description of class"""

    _next_iteration = None
    _formula_iterable = None
    _z_values = None
    _c_values = None

    def __init__(self, formula_iterable):
        c_values_range = formula_iterable.get_c_values_range()
        c_values = numpy.multiply(numpy.complex(0, 1), c_values_range.imaginary_number_values)
        c_values = numpy.add(c_values, c_values_range.real_number_values)

        z_values_range = formula_iterable.get_z_values_range()
        z_values = numpy.multiply(numpy.complex(0, 1), z_values_range.imaginary_number_values)
        z_values = numpy.add(z_values, z_values_range.real_number_values)

        self._current_iteration = 0
        self._formula_iterable = formula_iterable
        self._z_values = z_values
        self._c_values = c_values

    def get_z_values(self):
        return self._z_values

    def get_c_values(self):
        return self._c_values

    @abstractclassmethod
    def __next__(cls):
        return super().__next__()
