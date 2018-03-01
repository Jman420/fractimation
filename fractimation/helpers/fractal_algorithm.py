import numpy

PHI = (1 + 5**0.5) / 2.0
def get_fibonocci_number(index):
    if index < 2:
        return index

    return int(round((PHI**index - (1 - PHI)**index) / 5**0.5))

def multibrot_algorithm(z_values, c_values, power):
    # Calculate exponent piece of Multibrot Equation
    z_values_new = numpy.copy(z_values)
    exponent_value = numpy.copy(z_values)
    for exponentCounter in range(0, power - 1):
        z_values_new = numpy.multiply(exponent_value, z_values_new)

    # Add C piece of Multibrot Equation
    z_values_new = numpy.add(z_values_new, c_values)
    return z_values_new

def newton_method_algorithm(coefficient_array, coefficient_array_derivative, z_values, c_values):
    coefficient_func_values = evaluate_polynomial_1d(coefficient_array, z_values, c_values)
    coefficient_deriv_func_values = evaluate_polynomial_1d(coefficient_array_derivative, z_values, c_values)
    func_values = numpy.divide(coefficient_func_values, coefficient_deriv_func_values)

    z_values_new = numpy.add(z_values, -func_values)
    iteration_diff = numpy.add(z_values, -z_values_new)

    return iteration_diff, z_values_new

# polynomialExpressionArray is an array in the format of increasing order; 
#   ie. [ 1, 2, 3 ] = c + 2z + 3z**2 ; [ 4, 0, 1, 0, 5 ] = 4c + z**2 + 5z**4
def evaluate_polynomial_1d(coefficient_array, z_values, c_values):
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
