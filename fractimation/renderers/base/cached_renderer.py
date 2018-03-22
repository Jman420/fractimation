from abc import ABC, abstractmethod

from .fractimation_renderer import FractimationRenderer
from ...app_events.cache_events import CacheEvents

_POPULATING_RENDER_CACHE_CAPTION = "Populating render cache to frame {}!"

class CachedRenderer(FractimationRenderer, ABC):

    events = None

    _fractal_iterator = None
    _render_cache = None

    def __init__(self):
        self._render_cache = list()
        self.events = CacheEvents()

    def initialize(self, fractal_iterable):
        super().initialize(fractal_iterable)

        self._fractal_iterator = self._fractal_iterable.__iter__()
        self._render_cache.clear()

    def populate_render_cache(self, max_iterations):
        if max_iterations <= len(self._render_cache):
            return

        fractal_name = self._fractal_iterable.get_fractal_name()
        print("Populating {} Render Cache to {} iterations...".format(fractal_name, max_iterations))
        self.events.on_start_populating_cache(_POPULATING_RENDER_CACHE_CAPTION.format(max_iterations))
        
        for iteration_counter in range(len(self._render_cache), max_iterations):
            print("Iteration {} processing...".format(iteration_counter))
            self.render_to_cache()

        print("Completed populating {} Render Cache!".format(fractal_name))
        self.events.on_complete_populating_cache()

    def render(self, frame_num):
        super().render(frame_num)

        if frame_num >= len(self._render_cache):
            for frame_counter in range(len(self._render_cache), frame_num + 1):
                self.render_to_cache()

        frame = self._render_cache[frame_num]
        return frame

    def get_render_cache(self):
        return self._render_cache
        
    @abstractmethod
    def render_to_cache(self):
        pass
