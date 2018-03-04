from abc import ABC, abstractmethod

from .fractimation_renderer import FractimationRenderer

class CachedRenderer(FractimationRenderer, ABC):
    """Base class for Cached Fractal Renderers"""

    _fractal_iterator = None
    _render_cache = None

    def __init__(self, render_axes, fractal_iterable):
        super().__init__(render_axes, fractal_iterable)

        self._fractal_iterator = self._fractal_iterable.__iter__()
        self._render_cache = []

    def preheat_render_cache(self, max_iterations):
        if max_iterations <= len(self._render_cache):
            return

        print("Preheating Cache to {} iterations...".format(max_iterations))
        for iteration_counter in range(len(self._render_cache), max_iterations):
            print("Iteration {} processing...".format(iteration_counter))
            self.render_to_cache()

        print("Completed preheating cache!")

    @abstractmethod
    def render_to_canvas(self, frame_num, canvas):
        super().render(frame_num, canvas)

    @abstractmethod
    def render_to_cache(self):
        pass
