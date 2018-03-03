from ..data_models.complex_range import ComplexRange

def generate_complex_range(complex_range_params, dimension_params):
    spacing_func = complex_range_params.spacing_func
    
    real_range = spacing_func(complex_range_params.min_real_number,
                              complex_range_params.max_real_number,
                              dimension_params.width)[dimension_params.x_indexes]
    imaginary_range = spacing_func(complex_range_params.min_imaginary_number,
                                   complex_range_params.max_imaginary_number,
                                   dimension_params.height)[dimension_params.y_indexes]

    return ComplexRange(real_range, imaginary_range)
