from abc import ABC, abstractmethod

from .fractimation_renderer import FractimationRenderer

class CachedRenderer(FractimationRenderer, ABC):
    """Base class for Cached Fractal Renderers"""

    _render_cache = None

    def initialize(self):
        FractimationRenderer.initialize(self)

        self._render_cache = { }

    def preheat_render_cache(self, max_iterations):
        if max_iterations < len(self._render_cache):
            return

        print("Preheating Cache to {} iterations...".format(max_iterations))
        for iteration_counter in range(len(self._render_cache), max_iterations):
            print("Iteration {} processing...".format(iteration_counter))
            self.iterate()

        print("Completed preheating cache!")

    @abstractmethod
    def iterate(self):
        super().iterate()

    @abstractmethod
    def render(self, frame_num, axes):
        super().render(frame_num, axes)
