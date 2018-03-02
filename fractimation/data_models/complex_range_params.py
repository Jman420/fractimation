class ComplexRangeParams(object):
    """description of class"""

    min_real_number = None
    max_real_number = None
    min_imaginary_number = None
    max_imaginary_number = None

    def __init__(self, min_real_number, max_real_number, min_imaginary_number,
                 max_imaginary_number):
        self.min_real_number = min_real_number
        self.max_real_number = max_real_number
        self.min_imaginary_number = min_imaginary_number
        self.max_imaginary_number = max_imaginary_number
