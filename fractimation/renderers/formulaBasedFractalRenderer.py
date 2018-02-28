from .base.cachedImageRenderer import CachedImageRenderer

class formulaBasedFractalRenderer(CachedImageRenderer):
    """description of class"""

    _fractalAlgorithmFunc = None
    _recolorImage = False
    _reducibleArrays = None

    def __init__(self, width, height, imageArrayShape, colorMap, fractalAlgorithmFunc, reducibleArrays, recolorImage=True, initialImageArrayValue=-1):
        self.initialize(width, height, imageArrayShape, colorMap, fractalAlgorithmFunc, reducibleArrays, recolorImage, initialImageArrayValue)

    def initialize(self, width, height, imageArrayShape, colorMap, fractalAlgorithmFunc, reducibleArrays, recolorImage=True, initialImageArrayValue=-1):
        super().initialize(width, height, imageArrayShape, colorMap, initialImageArrayValue)

        self._fractalAlgorithmFunc = fractalAlgorithmFunc
        self._recolorImage = recolorImage
        self._reducibleArrays = reducibleArrays

    def iterate(self):
        super().iterate()

        if len(self._zValues) <= 0:
            # Nothing left to calculate, so just store the last image in the cache
            finalImage = self._renderCache[len(self._renderCache) - 1]
            self._renderCache.update({ self._nextIterationIndex : finalImage })
            self._nextIterationIndex += 1
            return