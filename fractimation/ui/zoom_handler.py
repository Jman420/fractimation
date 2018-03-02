import matplotlib.widgets as widgets

LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 3

MATPLOTLIB_PAN_ZOOM_MODE = "pan/zoom"

def restart_playback(viewer):
    viewer.stop()
    viewer.get_render_manager().get_animation_axes().autoscale(True)
    viewer.get_animation_manager().render(0)
    viewer.play()

class ZoomHandler(object):
    """Class to handle Fractimation Zoom UI"""

    _renderer = None
    _viewer = None

    _x_start = None
    _y_start = None
    _x_end = None
    _y_end = None
    _zoom_ready = False
    _zoom_box = None
    _zoom_stack = None

    def __init__(self, renderer, viewer, min_zoom_width=10, min_zoom_height=10):
        self._renderer = renderer
        self._viewer = viewer

        animation_axes = self._viewer.get_render_manager().get_animation_axes()
        self._zoom_box = widgets.RectangleSelector(animation_axes, self.select_zoom_coords,
                                                   useblit=True, minspanx=min_zoom_width,
                                                   minspany=min_zoom_height,
                                                   button=[LEFT_MOUSE_BUTTON], interactive=True)

        figure = viewer.get_window_manager().get_figure()
        figure.canvas.mpl_connect('button_press_event', self.handle_mouse_button_press)
        figure.canvas.mpl_connect('button_release_event', self.handle_mouse_button_release)

    def select_zoom_coords(self, start_coords, end_coords):
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
        if not self._zoom_ready:
            return

        self._renderer.zoom_in(self._x_start, self._y_start, self._x_end, self._y_end)
        self._zoom_ready = False
        self._zoom_box.extents = (0, 0, 0, 0)

        restart_playback(self._viewer)

    def undo_current_zoom(self):
        if self._renderer.zoom_out():
            restart_playback(self._viewer)

    def handle_mouse_button_press(self, event_data):
        if event_data.dblclick:
            self.confirm_zoom_coords()

    def handle_mouse_button_release(self, event_data):
        if (self._viewer.get_window_manager().get_figure().canvas.toolbar.mode ==
                MATPLOTLIB_PAN_ZOOM_MODE):
            return

        if event_data.button == RIGHT_MOUSE_BUTTON:
            self.undo_current_zoom()
