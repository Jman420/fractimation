"""
Functions related to Fractal Algorithms

Public Methods :
  * get_fibonocci_number - Returns the Fibonnoci Number for the requested index
  * multibrot_algorithm - Performs a single interation of the Multibrot Formula
  * newton_method_algorithm - Performs a single iteration of the Newton Method Formula
  * evaluate_polynomial_1d - Performs a single iteration of a Polynomial Formula
"""

import numpy

_PHI = (1 + 5**0.5) / 2.0

def get_fibonocci_number(index):
    """
    Returns the Fibonocci Number for the requested index

    Parameters :
      * index - Index of the requested Fibonocci Number
          (indexes 2 and below will simply return the requested index value)
    """
    if index < 2:
        return index

    return int(round((_PHI**index - (1 - _PHI)**index) / 5**0.5))

def multibrot_algorithm(z_values, c_values, power):
    """
    Perform an iteration of the Multibrot Polynomial Formula (z = z^power + c) and return the
    resulting values

    Parameters :
      * z_values - Input z values for the Polynomial Formula
      * c_values - Input c values for the Polynomial Formula
      * power - Exponential power to use in the Polynomial Formula
    """
    z_values_new = numpy.copy(z_values)
    exponent_value = numpy.copy(z_values)
    for exponent_counter in range(0, power - 1):
        z_values_new = numpy.multiply(exponent_value, z_values_new)

    z_values_new = numpy.add(z_values_new, c_values)
    return z_values_new

def newton_method_algorithm(coefficient_array, coefficient_array_derivative, z_values, c_values):
    """
    Perform an iteration of the Newton Method Algorithm (z = z - (f(z) / f_deriv(z))) and return
    the difference in iteration values and the resulting values

    Parameters :
      * coefficient_array - An array describing a Polynomial Formula in exponential order
          (ie. [ 1, 2, 3 ] = c + 2z + 3z**2 ; [ 4, 0, 1, 0, 5 ] = 4c + z**2 + 5z**4)
      * coefficient_array_derivative - An array describing the Derivative Polynomial Formula
          of coefficient_array in exponential order
          (ie. [ 1, 2, 3 ] = c + 2z + 3z**2 ; [ 4, 0, 1, 0, 5 ] = 4c + z**2 + 5z**4)
      * z_values - Input z values for the Polynomial Formula
      * c_values - Input c values for the Polynomial Formula
    """
    coefficient_func_values = evaluate_polynomial_1d(coefficient_array, z_values, c_values)
    coefficient_deriv_func_values = evaluate_polynomial_1d(coefficient_array_derivative,
                                                           z_values, c_values)
    func_values = numpy.divide(coefficient_func_values, coefficient_deriv_func_values)

    z_values_new = numpy.add(z_values, -func_values)
    iteration_diff = numpy.add(z_values, -z_values_new)

    return [iteration_diff, z_values_new]

def evaluate_polynomial_1d(coefficient_array, z_values, c_values):
    """
    Perform an iteration of the Polynomial Formula provided and return the resulting values

    Parameters :
      * coefficient_array - An array describing a Polynomial Formula in exponential order
          (ie. [ 1, 2, 3 ] = c + 2z + 3z**2 ; [ 4, 0, 1, 0, 5 ] = 4c + z**2 + 5z**4)
      * z_values - Input z values for the Polynomial Formula
      * c_values - Input c values for the Polynomial Formula
    """
    # Calculate Polynomial Constant Expression
    constant_coefficient = coefficient_array[0]
    constant_values = c_values * constant_coefficient

    # Calculate Polynomial Exponential Expressions
    exponent_accumulator = numpy.ones(z_values.shape, dtype=z_values.dtype)
    exponent_values = numpy.empty(z_values.shape, dtype=z_values.dtype)
    z_values_new = numpy.zeros(z_values.shape, dtype=z_values.dtype)
    for exponent_counter in range(1, len(coefficient_array)):
        exponent_accumulator = numpy.multiply(exponent_accumulator, z_values)
        exponent_coefficient = coefficient_array[exponent_counter]

        exponent_values = numpy.multiply(exponent_accumulator, exponent_coefficient)
        z_values_new = numpy.add(z_values_new, exponent_values)

    # Add Constant and Exponential Expressions
    z_values_new = z_values_new + constant_values

    return z_values_new
