"""
Fractimation specific Fractal Formula Parameter Class

Public Classes :
  * FormulaParams - Represents the parameters associated with a Fractal Formula
"""

class FormulaParams(object):
    """
    Parameters for initializing and executing a Fractal Formula

    Public Attributes :
      * real_number - A real number value used by the formula; usually used as an initial value
          during initialization or as a constant value within the formula
      * imaginary_number - An imaginary number value used by the formula; usually used as an
          initial value during initialization or as a constant value within the formula
      * escape_value - A threshold value used to determine when to stop evaluating a pixel's
          associated complex values
    """

    coefficient_array = Non
    escape_value = None

    def __init__(self, coefficient_array, escape_value):
        """
        Constructor

        Parameters :
            * escape_value - A threshold value used to determine when to stop evaluating a pixel's
                associated complex values
        """

        self.coefficient_array = coefficient_array
        self.escape_value = escape_value

    def get_coefficient_array(self):
        return self.coefficient_array

    def get_escape_value(self):
        return self.escape_value
