class ComplexRange(object):

    real_number_values = None
    imaginary_number_values = None

    def __init__(self, real_number_values, imaginary_number_values):
        self.real_number_values = real_number_values
        self.imaginary_number_values = imaginary_number_values

    def get_real_number_values(self):
        return self.real_number_values

    def get_imaginary_number_values(self):
        return self.imaginary_number_values
