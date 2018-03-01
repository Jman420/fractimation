from abc import ABC, abstractmethod

class FractimationRenderer(ABC, object):
    """Base Class for all Fractimation Renderers"""

    _next_iteration_index = None

    def initialize(self):
        self._next_iteration_index = 0

    @abstractmethod
    def iterate(self):
        pass

    @abstractmethod
    def render(self, frame_num, axes):
        pass
