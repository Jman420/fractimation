from abc import ABC, abstractmethod

class FractimationRenderer(ABC, object):
    """Base Class for all Fractimation Renderers"""

    def initialize(self):
        pass

    @abstractmethod
    def iterate(self):
        pass

    @abstractmethod
    def render(self, frameNumber, axes):
        pass