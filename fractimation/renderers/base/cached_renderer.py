from abc import ABC, abstractmethod

from .fractimation_renderer import FractimationRenderer

class CachedRenderer(FractimationRenderer, ABC):
    """Base class for Cached Fractal Renderers"""

    _fractal_iterator = None
    _render_cache = None

    def __init__(self, render_axes):
        super().__init__(render_axes)

        self._render_cache = list()

    def initialize(self, fractal_iterable):
        super().initialize(fractal_iterable)

        self._fractal_iterator = self._fractal_iterable.__iter__()
        self._render_cache.clear()

    def preheat_render_cache(self, max_iterations):
        if max_iterations <= len(self._render_cache):
            return

        fractal_name = self._fractal_iterable.get_fractal_name()
        print("Preheating {} Render Cache to {} iterations...".format(fractal_name, max_iterations))
        for iteration_counter in range(len(self._render_cache), max_iterations):
            print("Iteration {} processing...".format(iteration_counter))
            self.render_to_cache()

        print("Completed preheating {} Render Cache!".format(fractal_name))

    @abstractmethod
    def render_to_canvas(self, frame_num, canvas):
        super().render_to_canvas(frame_num, canvas)

    @abstractmethod
    def render_to_cache(self):
        pass
