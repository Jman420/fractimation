from .base.fractimation_functionality import FractimationFunctionality
from ..data_models.complex_range_params import ComplexRangeParams

def _reinitialize_renderer(renderer, fractal_iterable, z_values_range_params,
                           c_values_range_params):
    dimension_params = fractal_iterable.get_dimension_params()
    dimension_params.initialize()
    fractal_iterable.initialize(z_values_range_params, c_values_range_params, dimension_params,
                                fractal_iterable.get_formula_params(),
                                fractal_iterable.get_max_iterations())
    renderer.initialize(fractal_iterable)

class PannableComplexRange(FractimationFunctionality):

    def pan(self, real_range_diff, imaginary_range_diff):
        fractal_iterable = self._renderer.get_fractal_iterable()

        z_values_range_params = fractal_iterable.get_z_values_range_params()
        z_values_min_real_num = z_values_range_params.min_real_number
        z_values_max_real_num = z_values_range_params.max_real_number
        if z_values_min_real_num != z_values_max_real_num:
            z_values_min_real_num += real_range_diff
            z_values_max_real_num += real_range_diff

        z_values_min_imaginary_num = z_values_range_params.min_imaginary_number
        z_values_max_imaginary_num = z_values_range_params.max_imaginary_number
        if z_values_min_imaginary_num != z_values_max_imaginary_num:
            z_values_min_imaginary_num += imaginary_range_diff
            z_values_max_imaginary_num += imaginary_range_diff

        c_values_range_params = fractal_iterable.get_c_values_range_params()
        c_values_min_real_num = c_values_range_params.min_real_number
        c_values_max_real_num = c_values_range_params.max_real_number
        if c_values_min_real_num != c_values_max_real_num:
            c_values_min_real_num += real_range_diff
            c_values_max_real_num += real_range_diff

        c_values_min_imaginary_num = c_values_range_params.min_imaginary_number
        c_values_max_imaginary_num = c_values_range_params.max_imaginary_number
        if c_values_min_imaginary_num != c_values_max_imaginary_num:
            c_values_min_imaginary_num += imaginary_range_diff
            c_values_max_imaginary_num += imaginary_range_diff

        z_values_range_params_new = ComplexRangeParams(z_values_min_real_num,
                                                       z_values_max_real_num,
                                                       z_values_min_imaginary_num,
                                                       z_values_max_imaginary_num,
                                                       z_values_range_params.spacing_func)

        c_values_range_params_new = ComplexRangeParams(c_values_min_real_num,
                                                       c_values_max_real_num,
                                                       c_values_min_imaginary_num,
                                                       c_values_max_imaginary_num,
                                                       c_values_range_params.spacing_func)

        _reinitialize_renderer(self._renderer, fractal_iterable, z_values_range_params_new,
                               c_values_range_params_new)
