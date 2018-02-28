import matplotlib.widgets as widgets

LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 3

def restartPlayback(viewer):
    viewer.stop()
    viewer.get_render_manager().get_animation_axes().autoscale(True)
    viewer.get_animation_manager().render(0)
    viewer.play()

class ZoomHandler(object):
    """Class to handle Fractimation Zoom UI"""
    
    _renderer = _viewer = None

    _startX = _startY = None
    _endX = _endY = None
    _zoomReady = False
    _zoomBox = _zoomStack = None

    def __init__(self, renderer, viewer, minZoomWidth=10, minZoomHeight=10):
        self._renderer = renderer
        self._viewer = viewer

        self._zoomBox = widgets.RectangleSelector(self._viewer.get_render_manager().get_animation_axes(), self.selectZoomCoords,
                                                  useblit=True, minspanx=minZoomWidth, minspany=minZoomHeight,
                                                  button=[ LEFT_MOUSE_BUTTON ], interactive=True)

        figure = viewer.get_window_manager().get_figure()
        figure.canvas.mpl_connect('button_press_event', self.handleMouseButtonPress)
        figure.canvas.mpl_connect('button_release_event', self.handleMouseButtonRelease)

    def selectZoomCoords(self, startCoords, endCoords):
        startX = int(max(startCoords.xdata, 0))
        startY = int(max(startCoords.ydata, 0))
        endX = int(max(endCoords.xdata, 0))
        endY = int(max(endCoords.ydata, 0))

        self._startX, self._startY = startX, startY
        self._endX, self._endY = endX, endY
        self._zoomReady = True

    def confirmZoomCoords(self):
        if not self._zoomReady:
            return

        self._renderer.zoomIn(self._startX, self._startY, self._endX, self._endY)
        self._zoomReady = False
        self._zoomBox.extents = (0, 0, 0, 0)

        restartPlayback(self._viewer)

    def undoCurrentZoom(self):
        if self._renderer.zoomOut():
            restartPlayback(self._viewer)

    def handleMouseButtonPress(self, eventData):
        if eventData.dblclick:
            self.confirmZoomCoords()

    def handleMouseButtonRelease(self, eventData):
        if self._viewer.get_window_manager().get_figure().canvas.toolbar.mode == "pan/zoom":
            return

        if eventData.button == RIGHT_MOUSE_BUTTON:
            self.undoCurrentZoom()