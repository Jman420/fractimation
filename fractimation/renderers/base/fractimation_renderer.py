from abc import ABC, abstractmethod

class FractimationRenderer(ABC, object):
    """Base Class for all Fractimation Renderers"""

    _render_axes = None
    _fractal_iterable = None

    def __init__(self, render_axes):
        self._render_axes = render_axes

    def initialize(self, fractal_iterable):
        self._fractal_iterable = fractal_iterable

    def get_render_axes(self):
        return self._render_axes

    def get_fractal_iterable(self):
        return self._fractal_iterable

    @abstractmethod
    def render_to_canvas(self, frame_num, canvas):
        pass
