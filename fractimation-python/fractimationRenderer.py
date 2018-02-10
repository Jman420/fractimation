import matplotlib.patches as patches

class fractimationRenderer(object):
    """Base Class for Fractal Renderers"""

    _renderStartZoomCaption = _renderEndZoomCaption = False
    _renderZoomBox = False
    _startZoomX = _startZoomY = None
    _endZoomX = _endZoomY = None
    _cache = None
    _initialized = False

    def setStartZoomCoords(self, x, y):
        self._startZoomX = x
        self._startZoomY = y
        self._renderStartZoomCaption = True
        self._renderZoomBox = (self._startZoomX and self._startZoomY and self._endZoomX and self._endZoomY)

    def setEndZoomCoords(self, x, y):
        self._endZoomX = x
        self._endZoomY = y
        self._renderEndZoomCaption = True
        self._renderZoomBox = (self._startZoomX and self._startZoomY and self._endZoomX and self._endZoomY)

    def getMinZoomCoords(self):
        xCoord = min(self._startZoomX, self._endZoomX)
        yCoord = min(self._startZoomY, self._endZoomY)
        return [ int(xCoord), int(yCoord) ]

    def getMaxZoomCoords(self):
        xCoord = max(self._startZoomX, self._endZoomX)
        yCoord = max(self._startZoomY, self._endZoomY)
        return [ int(xCoord), int(yCoord) ]

    def confirmZoomCoords(confirm):
        if not confirm:
            self._startZoomX = self._startZoomY = None
            self._endZoomX = self._endZoomY = None
            self._renderStartZoomCaption = False
            self._renderEndZoomCaption = False
            self._renderZoomBox = false

    def render(self, frameNumber, axes):
        if self._renderZoomBox:
            zoomBoxWidth = abs(self._startZoomX - self._endZoomX)
            zoomBoxHeight = abs(self._startZoomY - self._endZoomY)
            zoomBox = patches.Rectangle(min(self._startZoomX, self._endZoomX), min(self._startZoomY, self._endZoomY),
                                       zoomBoxWidth, zoomBoxHeight, fill=False)
            axes.add_patch(zoomBox)