import matplotlib.widgets as widgets

class zoomHandler(object):
    """Class to handle Fractimation UI Events"""
    RIGHT_MOUSE_BUTTON = 3

    _renderer = _viewer = None
    _zoomBox = _zoomStack = None

    def __init__(self, renderer, viewer, minZoomWidth=50, minZoomHeight=50):
        self._renderer = renderer
        self._viewer = viewer
        self._zoomBox = widgets.RectangleSelector(self._viewer._animationAxes, self.confirmZoomCoords,
                                                 useblit=True, minspanx=minZoomWidth, minspany=minZoomHeight,
                                                 button=[1])
        viewer._figure.canvas.mpl_connect('button_press_event', self.undoPreviousZoom)

    def confirmZoomCoords(self, startCoords, endCoords):
        startX = int(max(startCoords.xdata, 0))
        startY = int(max(startCoords.ydata, 0))
        endX = int(max(endCoords.xdata, 0))
        endY = int(max(endCoords.ydata, 0))

        self._renderer.zoomIn(startX, startY, endX, endY)
        self._viewer.stop()
        self._viewer.render(0)
        self._viewer.play()

    def undoPreviousZoom(self, eventData):
        if eventData.button == self.RIGHT_MOUSE_BUTTON:
            if self._renderer.zoomOut():
                self._viewer.stop()
                self._viewer.render(0)
                self._viewer.play()