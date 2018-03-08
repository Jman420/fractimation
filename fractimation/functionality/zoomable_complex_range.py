import numpy

from .base.fractimation_functionality import FractimationFunctionality
from ..data_models.complex_range_params import ComplexRangeParams
from ..data_models.dimension_params import DimensionParams

def _reinitialize_renderer(renderer, fractal_iterable, z_values_range_params,
                           c_values_range_params):
    dimension_params = fractal_iterable.get_dimension_params()
    dimension_params.initialize()
    fractal_iterable.initialize(z_values_range_params, c_values_range_params, dimension_params,
                                fractal_iterable.get_formula_params(),
                                fractal_iterable.get_max_iterations())
    renderer.initialize(fractal_iterable)

class ZoomableComplexRange(FractimationFunctionality):

    _zoom_cache = None

    def __init__(self, renderer):
        super().__init__(renderer)

        self._zoom_cache = []

    def zoom_in(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        fractal_iterable = self._renderer.get_fractal_iterable()

        prev_zoom = ZoomCacheItem(fractal_iterable.get_z_values_range_params(),
                                  fractal_iterable.get_c_values_range_params())

        z_values_range = fractal_iterable.get_z_values_range()
        z_min_real_num = z_values_range.real_number_values[top_left_x][top_left_y]
        z_max_real_num = z_values_range.real_number_values[bottom_right_x][bottom_right_y]
        z_min_imaginary_num = z_values_range.imaginary_number_values[top_left_x][top_left_y]
        z_max_imaginary_num = z_values_range.imaginary_number_values[bottom_right_x][bottom_right_y]

        c_values_range = fractal_iterable.get_c_values_range()
        c_min_real_num = c_values_range.real_number_values[top_left_x][top_left_y]
        c_max_real_num = c_values_range.real_number_values[bottom_right_x][bottom_right_y]
        c_min_imaginary_num = c_values_range.imaginary_number_values[top_left_x][top_left_y]
        c_max_imaginary_num = c_values_range.imaginary_number_values[bottom_right_x][bottom_right_y]

        z_values_range_params = fractal_iterable.get_z_values_range_params()
        new_z_values_range_params = ComplexRangeParams(z_min_real_num, z_max_real_num,
                                                       z_min_imaginary_num, z_max_imaginary_num,
                                                       z_values_range_params.spacing_func)

        c_values_range_params = fractal_iterable.get_c_values_range_params()
        new_c_values_range_params = ComplexRangeParams(c_min_real_num, c_max_real_num,
                                                       c_min_imaginary_num, c_max_imaginary_num,
                                                       c_values_range_params.spacing_func)

        _reinitialize_renderer(self._renderer, fractal_iterable, new_z_values_range_params,
                               new_c_values_range_params)
        self._zoom_cache.append(prev_zoom)

    def zoom_out(self):
        if len(self._zoom_cache) < 1:
            return False

        prev_zoom = self._zoom_cache.pop()
        fractal_iterable = self._renderer.get_fractal_iterable()
        _reinitialize_renderer(self._renderer, fractal_iterable, prev_zoom.z_values_range_params,
                               prev_zoom.c_values_range_params)
        return True

class ZoomCacheItem(object):
    c_values_range_params = None
    z_values_range_params = None

    def __init__(self, z_values_range_params, c_values_range_params):
        self.z_values_range_params = z_values_range_params
        self.c_values_range_params = c_values_range_params
