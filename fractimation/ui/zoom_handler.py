"""
Fractimation specific Zoom Functionality Class

Public Classes :
  * ZoomHandler - Class to manage the Zoom Functionality for the Fractimation App
"""

import matplotlib.widgets as widgets

from ..helpers.playback import restart_playback

_LEFT_MOUSE_BUTTON = 1
_RIGHT_MOUSE_BUTTON = 3

_MATPLOTLIB_PAN_ZOOM_MODE = "pan/zoom"

class ZoomHandler(object):
    """
    Zoom Functionality handler for Fractimation

    Public Methods :
      * select_zoom_coords - Sets the zoom coordinates and indicates that zoom is ready
      * confirm_zoom_coords - Passes the zoom coordinates to the renderer and resets the Zoom UI
      * undo_current_zoom - Returns to the previous zoom coordinates

    Private Methods :
      * _handle_mouse_button_press - Method to handle mouse button down events; attached to
          Matplotlib button_press_event
      * _handle_mouse_button_release - Method to handle mouse button release events; attached to
          Matplotlib button_release_event
    """

    _zoomable_backend = None
    _viewer = None

    _x_start = None
    _y_start = None
    _x_end = None
    _y_end = None
    _zoom_ready = False
    _zoom_box = None

    def __init__(self, zoomable_backend, viewer, min_zoom_width=10, min_zoom_height=10):
        """
        Constructor

        Parameters :
          * renderer - The fractal renderer associated with the Zoom Functionality
          * viewer - The PlotPlayer instance used for playback
          * min_zoom_width (optional) - Minimum zoom box width
          * min_zoom_height (optional) - Minimum zoom box height
        """
        self._zoomable_backend = zoomable_backend
        self._viewer = viewer

        animation_axes = self._viewer.get_render_manager().get_animation_axes()
        self._zoom_box = widgets.RectangleSelector(animation_axes, self.select_zoom_coords,
                                                   useblit=True, minspanx=min_zoom_width,
                                                   minspany=min_zoom_height,
                                                   button=[_LEFT_MOUSE_BUTTON], interactive=True)

        figure = viewer.get_window_manager().get_figure()
        figure.canvas.mpl_connect('button_press_event', self._handle_mouse_button_press)
        figure.canvas.mpl_connect('button_release_event', self._handle_mouse_button_release)

    def select_zoom_coords(self, start_coords, end_coords):
        """
        Store the Start and End Coordinates for later confirmation

        Parameters :
          * start_coords - Matplotlib Rectangle Selector event data object
          * end_coords - Matplotlib Rectangle Selector event data object
        """
        x_start = int(max(start_coords.xdata, 0))
        y_start = int(max(start_coords.ydata, 0))
        x_end = int(max(end_coords.xdata, 0))
        y_end = int(max(end_coords.ydata, 0))

        self._x_start = x_start
        self._y_start = y_start
        self._x_end = x_end
        self._y_end = y_end
        self._zoom_ready = True

    def confirm_zoom_coords(self):
        """
        Perform the Zoom to the stored Start and End Coordinates
        """
        if not self._zoom_ready:
            return

        self._zoomable_backend.zoom_in(self._x_start, self._y_start, self._x_end, self._y_end)
        self._zoom_ready = False
        self._zoom_box.extents = (0, 0, 0, 0)

        restart_playback(self._viewer)

    def undo_current_zoom(self):
        """
        Return to the previous Zoom Coordinates
        """
        if self._zoomable_backend.zoom_out():
            restart_playback(self._viewer)

    def _handle_mouse_button_press(self, event_data):
        """
        Handles the Mouse Button Press event
        """
        if event_data.dblclick:
            self.confirm_zoom_coords()

    def _handle_mouse_button_release(self, event_data):
        """
        Handles the Mouse Button Release event
        """
        if (self._viewer.get_window_manager().get_figure().canvas.toolbar.mode ==
                _MATPLOTLIB_PAN_ZOOM_MODE):
            return

        if event_data.button == _RIGHT_MOUSE_BUTTON:
            self.undo_current_zoom()
