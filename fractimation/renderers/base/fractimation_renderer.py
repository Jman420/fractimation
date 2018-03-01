from abc import ABC, abstractmethod

class FractimationRenderer(ABC, object):
    """Base Class for all Fractimation Renderers"""

    _nextIterationIndex = None

    def initialize(self):
        self._nextIterationIndex = 0

    @abstractmethod
    def iterate(self):
        pass

    @abstractmethod
    def render(self, frameNumber, axes):
        pass