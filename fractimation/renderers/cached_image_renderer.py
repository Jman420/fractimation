import numpy

from .base.cached_renderer import CachedRenderer
from ..data_models.image_params import ImageParams
from ..helpers.list_tools import update_indexes_with_value, remove_indexes

_IMAGE_ORIGIN = "upper"

class CachedImageRenderer(CachedRenderer):

    _dimension_params = None
    _image_params = None
    
    _image_array = None
    _image_canvas = None

    def __init__(self, image_axes, fractal_iterable, dimension_params, image_params=None):
        super().__init__(image_axes)

        if image_params is None:
            image_params = ImageParams()

        self._dimension_params = dimension_params
        self._image_params = image_params

        temp_image = numpy.zeros([self._dimension_params.width, self._dimension_params.height],
                                  dtype=int)
        self._image_canvas = self._render_axes.imshow(temp_image.T, cmap=self._image_params.color_map)

        self.initialize(fractal_iterable)

    def initialize(self, fractal_iterable):
        super().initialize(fractal_iterable)

        image_array = numpy.zeros([self._dimension_params.width, self._dimension_params.height],
                                  dtype=int)
        image_array = numpy.add(image_array, self._image_params.initial_value)
        self._image_array = image_array

        initial_image = numpy.copy(self._image_array)
        rotated_image = initial_image.T
        self._render_cache.append(rotated_image)
        
    def render_to_canvas(self, frame_num, canvas):
        super().render_to_canvas(frame_num, canvas)

        frame_image = self._render_cache[frame_num]
        self._image_canvas.set_data(frame_image)
        self._image_canvas.autoscale()

    def render_to_cache(self):
        iteration_data = self._fractal_iterator.__next__()
        frame_num = len(self._render_cache)

        if iteration_data is None:
            last_image = self._render_cache[-1]
            self._render_cache.append(last_image)
        else:
            dimension_params = self._dimension_params
            exploded_indexes = iteration_data.exploded_indexes
            exploded_x_indexes = dimension_params.x_indexes[exploded_indexes]
            exploded_y_indexes = dimension_params.y_indexes[exploded_indexes]
            self._image_array[exploded_x_indexes, exploded_y_indexes] = frame_num

            if self._image_params.recolor_image:
                final_image = update_indexes_with_value(self._image_array,
                                                        self._image_params.initial_value,
                                                        frame_num + 1)
            else:
                final_image = numpy.copy(self._image_array)
            rotated_image = final_image.T
            self._render_cache.append(rotated_image)

            reducable_arrays = [dimension_params.x_indexes, dimension_params.y_indexes]
            remaining_indexes = iteration_data.remaining_indexes
            reduced_arrays = remove_indexes(reducable_arrays, remaining_indexes)
            dimension_params.x_indexes = reduced_arrays[0]
            dimension_params.y_indexes = reduced_arrays[1]
