from abc import ABC, abstractclassmethod
from collections.abc import Iterable, Iterator

import numpy

from ...helpers.formula_tools import generate_complex_range

class FractalFormulaIterable(Iterable, ABC):
    
    _max_iterations = None
    _z_values_range_params = None
    _c_values_range_params = None
    _dimension_params = None
    _formula_params = None

    _z_values_range = None
    _c_values_range = None

    def __init__(self, z_values_range_params, c_values_range_params, dimension_params,
                 formula_params, max_iterations=None):
        self.initialize(z_values_range_params, c_values_range_params, dimension_params,
                        formula_params, max_iterations)

    def initialize(self, z_values_range_params, c_values_range_params, dimension_params,
                   formula_params, max_iterations=None):
        self._z_values_range = generate_complex_range(z_values_range_params, dimension_params)
        self._c_values_range = generate_complex_range(c_values_range_params, dimension_params)

        self._z_values_range_params = z_values_range_params
        self._c_values_range_params = c_values_range_params
        self._dimension_params = dimension_params
        self._formula_params = formula_params
        self._max_iterations = max_iterations

    def get_max_iterations(self):
        return self._max_iterations

    def get_z_values_range_params(self):
        return self._z_values_range_params

    def get_z_values_range(self):
        return self._z_values_range

    def get_c_values_range_params(self):
        return self._c_values_range_params

    def get_c_values_range(self):
        return self._c_values_range

    def get_dimension_params(self):
        return self._dimension_params

    def get_formula_params(self):
        return self._formula_params

    @abstractclassmethod
    def __iter__(cls):
        return super().__iter__()

class FractalFormulaIterator(Iterator, ABC):
    
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

        self._next_iteration = 0
        self._formula_iterable = formula_iterable
        self._z_values = z_values
        self._c_values = c_values

    def get_z_values(self):
        return self._z_values

    def get_c_values(self):
        return self._c_values

    def __next__(cls):
        max_iterations = cls._formula_iterable.get_max_iterations()
        if max_iterations is not None and cls._next_iteration >= max_iterations:
            raise StopIteration
