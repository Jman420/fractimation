import numpy

from ...data_models.complex_range_params import ComplexRangeParams

class ZoomableComplexRange():
    """Base Class for Zoomable Complex Polynomial Fractal Equation Renderers"""

    _renderer = None
    _zoom_cache = None

    def __init__(self):
        self._zoom_cache = []

    def initialize(self, renderer):
        self._renderer = renderer

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

        fractal_iterable.initialize(new_z_values_range_params, new_c_values_range_params,
                                    fractal_iterable.get_dimension_params(),
                                    fractal_iterable.get_formula_params(),
                                    fractal_iterable.get_max_iterations())
        self._renderer.initialize(fractal_iterable)
        self._zoom_cache.append(prev_zoom)

    def zoom_out(self):
        if len(self._zoom_cache) < 1:
            return False

        prev_zoom = self._zoom_cache.pop()
        fractal_iterable = self._renderer.get_fractal_iterable()
        fractal_iterable.initialize(prev_zoom.z_values_range_params,
                                    prev_zoom.c_values_range_params,
                                    fractal_iterable.get_dimension_params(),
                                    fractal_iterable.get_formula_params(),
                                    fractal_iterable.get_max_iterations())
        self._renderer.initialize(fractal_iterable)
        return True

class ZoomCacheItem(object):
    c_values_range_params = None
    z_values_range_params = None

    def __init__(self, z_values_range_params, c_values_range_params):
        self.z_values_range_params = z_values_range_params
        self.c_values_range_params = c_values_range_params
