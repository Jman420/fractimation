from abc import ABC, abstractmethod

from .fractimation_renderer import FractimationRenderer

_POPULATING_RENDER_CACHE_CAPTION = "Populating render cache to frame {}!"

class CachedRenderer(FractimationRenderer, ABC):
    """Base class for Cached Fractal Renderers"""

    _fractal_iterator = None
    _render_cache = None
    _populate_cache_caption = None

    def __init__(self, render_axes):
        super().__init__(render_axes)

        self._render_cache = list()
        self._populate_cache_caption = render_axes.text(0.5, 0.5,
                                                        _POPULATING_RENDER_CACHE_CAPTION.format(0),
                                                        horizontalalignment='center',
                                                        verticalalignment='center',
                                                        fontsize=18,
                                                        transform=render_axes.transAxes,
                                                        visible=False)

    def initialize(self, fractal_iterable):
        super().initialize(fractal_iterable)

        self._fractal_iterator = self._fractal_iterable.__iter__()
        self._render_cache.clear()

    def populate_render_cache(self, max_iterations):
        if max_iterations <= len(self._render_cache):
            return

        figure = self._render_axes.get_figure()
        self._populate_cache_caption.set_text(_POPULATING_RENDER_CACHE_CAPTION.format(max_iterations))
        self._populate_cache_caption.set_visible(True)
        figure.canvas.draw()

        fractal_name = self._fractal_iterable.get_fractal_name()
        print("Populating {} Render Cache to {} iterations...".format(fractal_name, max_iterations))
        for iteration_counter in range(len(self._render_cache), max_iterations):
            print("Iteration {} processing...".format(iteration_counter))
            self.render_to_cache()

        print("Completed populating {} Render Cache!".format(fractal_name))
        self._populate_cache_caption.set_visible(False)
        figure.canvas.draw()

    @abstractmethod
    def render_to_canvas(self, frame_num, canvas):
        super().render_to_canvas(frame_num, canvas)

        if frame_num >= len(self._render_cache):
            for frame_counter in range(len(self._render_cache), frame_num + 1):
                self.render_to_cache()
        
    @abstractmethod
    def render_to_cache(self):
        pass
