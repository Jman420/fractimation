from abc import ABC, abstractmethod

class FractimationRenderer(ABC, object):
    """Base Class for all Fractimation Renderers"""

    _render_axes = None
    _fractal_iterable = None

    def __init__(self, render_axes, fractal_iterable):
        self._render_axes = render_axes
        self._fractal_iterable = fractal_iterable

    @abstractmethod
    def render_to_canvas(self, frame_num, canvas):
        pass
