from abc import ABC, abstractmethod

class FractimationRenderer(ABC):
    """Base class for Fractal Renderers"""

    _renderCache = None
    _nextIterationIndex = None

    def initialize(self):
        self._renderCache = { }
        self._nextIterationIndex = 0

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
        pass