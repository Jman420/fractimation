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

    real_number = None
    imaginary_number = None
    escape_value = None

    def __init__(self, real_number, imaginary_number, escape_value):
        """
        Constructor

        Parameters :
            * real_number - A real number value used by the formula; usually used as an initial
                value during initialization or as a constant value within the formula
            * imaginary_number - An imaginary number value used by the formula; usually used as an
                initial value during initialization or as a constant value within the formula
            * escape_value - A threshold value used to determine when to stop evaluating a pixel's
                associated complex values
        """

        self.real_number = real_number
        self.imaginary_number = imaginary_number
        self.escape_value = escape_value
