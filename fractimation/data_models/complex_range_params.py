"""
Fractimation specific Complex Range Parameter Class

Public Classes :
  * ComplexRangeParams - Represents the parameters associated with a range of complex numbers
"""

import numpy

class ComplexRangeParams(object):
    """
    Parameters for creating a range of complex numbers

    Public Attributes :
      * min_real_number - Minimum value of the range of real numbers
      * max_real_number - Maximum value of the range of real numbers
      * min_imaginary_number - Minimum value of the range of imaginary numbers
      * max_imaginary_number - Maximum value of the range of imaginary numbers
      * spacing_func - A function accepting 3 parameters (min_value, max_value, size) which returns
          an array of numbers of the specified size
    """

    min_real_number = None
    max_real_number = None
    min_imaginary_number = None
    max_imaginary_number = None
    spacing_func = None

    def __init__(self, min_real_number, max_real_number, min_imaginary_number,
                 max_imaginary_number, spacing_func=numpy.linspace):
        """
        Constructor

        Parameters :
          * min_real_number - Minimum value of the range of real numbers
          * max_real_number - Maximum value of the range of real numbers
          * min_imaginary_number - Minimum value of the range of imaginary numbers
          * max_imaginary_number - Maximum value of the range of imaginary numbers
          * spacing_func - A function accepting 3 parameters (min_value, max_value, size) which
              returns an array of numbers of the specified size
        """
        self.min_real_number = min_real_number
        self.max_real_number = max_real_number
        self.min_imaginary_number = min_imaginary_number
        self.max_imaginary_number = max_imaginary_number
        self.spacing_func = spacing_func
