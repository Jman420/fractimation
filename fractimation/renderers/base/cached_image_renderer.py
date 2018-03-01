from abc import ABC, abstractmethod

import numpy

from .cached_renderer import CachedRenderer

class CachedImageRenderer(CachedRenderer, ABC):
    """Base class for Fractal Renderers using Image Arrays for rendering"""

    _width = None
    _height = None
    _image_array = None
    _image_canvas = None
    _color_map = None

    def initialize(self, width, height, image_array_shape, color_map, initial_image_array_value=-1):
        CachedRenderer.initialize(self)

        # Initialize Image Array
        image_array = numpy.zeros(image_array_shape, dtype=int)
        image_array = numpy.add(image_array, initial_image_array_value)

        self._width = width
        self._height = height
        self._image_array = image_array
        self._color_map = color_map

    @abstractmethod
    def iterate(self):
        super().iterate()

    def render(self, frame_num, axes):
        if frame_num not in self._render_cache:
            for frame_counter in range(self._next_iteration_index, frame_num + 1):
                self.iterate()
            
        final_image = self._render_cache[frame_num]
        if self._image_canvas is None:
            self._image_canvas = axes.imshow(final_image, cmap=self._color_map, origin="upper")
        else:
            self._image_canvas.set_data(final_image)
            self._image_canvas.autoscale()
