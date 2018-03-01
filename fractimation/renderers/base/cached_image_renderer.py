from abc import ABC, abstractmethod

import numpy

from .cached_renderer import CachedRenderer

class CachedImageRenderer(CachedRenderer, ABC):
    """Base class for Fractal Renderers using Image Arrays for rendering"""

    _width = _height = None
    _imageArray = None
    _imageCanvas = _colorMap = None

    def initialize(self, width, height, imageArrayShape, colorMap, initialImageArrayValue=-1):
        CachedRenderer.initialize(self)

        # Initialize Image Array
        imageArray = numpy.zeros(imageArrayShape, dtype=int)
        imageArray = numpy.add(imageArray, initialImageArrayValue)

        self._width = width
        self._height = height
        self._imageArray = imageArray
        self._colorMap = colorMap

    @abstractmethod
    def iterate(self):
        super().iterate()

    def render(self, frameNumber, axes):
        if frameNumber not in self._renderCache:
            for frameCounter in range(self._nextIterationIndex, frameNumber + 1):
                self.iterate()
            
        finalImage = self._renderCache[frameNumber]
        if self._imageCanvas == None:
            self._imageCanvas = axes.imshow(finalImage, cmap=self._colorMap, origin="upper")
        else:
            self._imageCanvas.set_data(finalImage)
            self._imageCanvas.autoscale()