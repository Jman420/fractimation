from abc import ABC, abstractmethod

from .cachedRenderer import CachedRenderer

class CachedPatchCollectionRenderer(CachedRenderer, ABC):
    """Base class for Fratal Renderers using Matpotlib PatchCollections for rendering"""

    _cacheAddedToAxes = False

    def initialize(self):
        super().initialize()

        self._cacheAddedToAxes = False

    @abstractmethod
    def iterate(self):
        super().iterate()

    def render(self, frameNumber, axes):
        if not self._cacheAddedToAxes:
            for frameCounter in range(0, len(self._renderCache)):
                framePatches = self._renderCache[frameCounter]
                axes.add_collection(framePatches)
            self._cacheAddedToAxes = True
        
        if not frameNumber in self._renderCache:
            for frameCounter in range(self._nextIterationIndex, frameNumber + 1):
                self.iterate()

                framePatches = self._renderCache[frameCounter]
                axes.add_collection(framePatches)

        for frameCounter in range(0, len(self._renderCache)):
            framePatches = self._renderCache[frameCounter]
            framePatches.set_visible(frameCounter <= frameNumber)