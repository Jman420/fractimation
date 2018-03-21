from abc import ABC, abstractmethod

class FractimationRenderer(ABC, object):
    """Base Class for all Fractimation Renderers"""

    _fractal_iterable = None

    def initialize(self, fractal_iterable):
        self._fractal_iterable = fractal_iterable

    def get_fractal_iterable(self):
        return self._fractal_iterable

    @abstractmethod
    def render(self, frame_num):
        pass
