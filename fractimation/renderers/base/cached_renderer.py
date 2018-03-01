from abc import ABC, abstractmethod

from .fractimation_renderer import FractimationRenderer

class CachedRenderer(FractimationRenderer, ABC):
    """Base class for Cached Fractal Renderers"""

    _renderCache = None

    def initialize(self):
        FractimationRenderer.initialize(self)

        self._renderCache = { }

    def preheatRenderCache(self, maxIterations):
        if maxIterations < len(self._renderCache):
            return

        print("Preheating Cache to {} iterations...".format(maxIterations))
        for iterationCounter in range(len(self._renderCache), maxIterations):
            print("Iteration {} processing...".format(iterationCounter))
            self.iterate()

        print("Completed preheating cache!")

    @abstractmethod
    def iterate(self):
        super().iterate()

    @abstractmethod
    def render(self, frameNumber, axes):
        super().render(frameNumber, axes)