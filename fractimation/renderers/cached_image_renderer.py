import numpy

from .base.cached_renderer import CachedRenderer
from ..data_models.image_params import ImageParams
from ..helpers.list_tools import update_indexes_with_value, remove_indexes

_IMAGE_ORIGIN = "upper"

class CachedImageRenderer(CachedRenderer):
    """Base class for Fractal Renderers using Image Arrays for rendering"""

    _dimension_params = None
    _image_params = None
    
    _image_array = None
    _image_canvas = None

    def __init__(self, image_axes, fractal_iterable, dimension_params, image_params=None):
        super().__init__(image_axes, fractal_iterable)

        if image_params is None:
            image_params = ImageParams()

        image_array = numpy.zeros([dimension_params.width, dimension_params.height], dtype=int)
        image_array = numpy.add(image_array, image_params.initial_value)
        self._image_array = image_array

        self._image_canvas = image_axes.imshow(self._image_array, cmap=image_params.color_map)

        self._dimension_params = dimension_params
        self._image_params = image_params
        
    def render_to_canvas(self, frame_num, canvas):
        if frame_num not in self._render_cache:
            for frame_counter in range(self._next_frame_number, frame_num + 1):
                self.render_to_cache()

        final_image = self._render_cache[frame_num]
        self._image_canvas.set_data(final_image)
        self._image_canvas.autoscale()

    def render_to_cache(self):
        iteration_data = self._fractal_iterator.__next__()
        frame_num = self._next_frame_number

        if iteration_data is None:
            last_image = self._render_cache[len(self._render_cache) - 1]
            self._render_cache.update({frame_num : last_image})
        else:
            dimension_params = self._dimension_params
            exploded_indexes = iteration_data.exploded_indexes
            exploded_x_indexes = dimension_params.x_indexes[exploded_indexes]
            exploded_y_indexes = dimension_params.y_indexes[exploded_indexes]
            self._image_array[exploded_x_indexes, exploded_y_indexes] = frame_num

            final_image = self._image_array
            if self._image_params.recolor_image:
                final_image = update_indexes_with_value(final_image,
                                                        self._image_params.initial_value,
                                                        frame_num + 1)

            self._render_cache.update({frame_num : final_image.T})

            reducable_arrays = [dimension_params.x_indexes, dimension_params.y_indexes]
            remaining_indexes = iteration_data.remaining_indexes
            reduced_arrays = remove_indexes(reducable_arrays, remaining_indexes)
            dimension_params.x_indexes = reduced_arrays[0]
            dimension_params.y_indexes = reduced_arrays[1]

        self._next_frame_number += 1
