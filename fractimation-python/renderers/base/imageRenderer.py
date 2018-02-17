from abc import ABC

from .fractimationRenderer import FractimationRenderer

class ImageRenderer(FractimationRenderer, ABC):
    """Base class for Fractal Renderers using Image Arrays for rendering"""

    _imageCanvas = None
    
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