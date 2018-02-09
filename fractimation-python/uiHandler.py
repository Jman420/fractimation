class uiHandler(object):
    """Class to handle Fractimation UI Events"""
    LEFT_MOUSE_BUTTON = 1
    RIGHT_MOUSE_BUTTON = 3

    _renderer = _viewer = None
    _mouseButtonDown = False
    _startX = _startY = None
    _minRealNumber = _minImaginaryNumber = None

    def __init__(self, renderer, viewer):
        self._renderer = renderer
        self._viewer = viewer

    def imageMouseButtonPress(self, eventData):
        print(eventData)
        
        if self._mouseButtonDown and eventData.dblclick:
            self._renderer.confirmZoomCoords(False)
            self._viewer.renderImage(self._renderer._currentFrameNumber - 1)

        elif eventData.button == self.LEFT_MOUSE_BUTTON:
            self._renderer.setStartZoomCoords(eventData.x, eventData.y)
            self._mouseButtonDown = True
            self._viewer.renderImage(self._renderer._currentFrameNumber - 1)

    def imageMouseButtonRelease(self, eventData):
        print(eventData)

        if eventData.button == self.LEFT_MOUSE_BUTTON:
            self._mouseButtonDown = False

    def imageMouseMotion(self, eventData):
        print(eventData)

        if (self._mouseButtonDown):
            self._renderer.setEndZoomCoords(eventData.x, eventData.y)
            self._viewer.renderImage(self._renderer._currentFrameNumber - 1)