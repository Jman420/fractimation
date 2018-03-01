from .base.cached_image_renderer import CachedImageRenderer

class formulaBasedFractal(CachedImageRenderer):
    """description of class"""

    _fractal_algorithm_func = None
    _reducible_arrays = None
    _recolor_image = False

    def __init__(self, width, height, image_array_shape, color_map, fractal_algorithm_func, reducible_arrays, recolor_image=True, initial_image_array_value=-1):
        self.initialize(width, height, image_array_shape, color_map, fractal_algorithm_func, reducible_arrays, recolor_image, initial_image_array_value)

    def initialize(self, width, height, image_array_shape, color_map, fractal_algorithm_func, reducible_arrays, recolor_image=True, initial_image_array_value=-1):
        super().initialize(width, height, image_array_shape, color_map, initial_image_array_value)

        self._fractal_algorithm_func = fractal_algorithm_func
        self._reducible_arrays = reducible_arrays
        self._recolor_image = recolor_image

    def iterate(self):
        super().iterate()

        if len(self._z_values) <= 0:
            # Nothing left to calculate, so just store the last image in the cache
            final_image = self._render_cache[len(self._render_cache) - 1]
            self._render_cache.update({ self._next_iteration_index : final_image })
            self._next_iteration_index += 1
            return
