_PAN_TOGGLE_BUTTON = "shift"
_SHIFT_LEFT_BUTTON = 'left'
_SHIFT_RIGHT_BUTTON = 'right'
_SHIFT_DOWN_BUTTON = 'down'
_SHIFT_UP_BUTTON = 'up'

_DEFAULT_PAN_SIZE = 0.5

def _handle_pan_keys(key, pannable_backend, pan_size):
    handled = True

    if key == _SHIFT_LEFT_BUTTON:
        pannable_backend.pan_range(-pan_size, 0)
    elif key == _SHIFT_RIGHT_BUTTON:
        pannable_backend.pan_range(pan_size, 0)
    elif key == _SHIFT_UP_BUTTON:
        pannable_backend.pan_range(0, pan_size)
    elif key == _SHIFT_DOWN_BUTTON:
        pannable_backend.pan_range(0, -pan_size)
    else:
        handled = False

    return handled

class PanHandler(object):

    _pannable_backend = None
    _viewer = None
    _pan_toggle_pressed = False
    _pan_size = None

    def __init__(self, pannable_backend, viewer, pan_size=_DEFAULT_PAN_SIZE):
        self._pannable_backend = pannable_backend
        self._viewer = viewer
        self._pan_size = pan_size
        self._pan_toggle_pressed = False

        input_handler = self._viewer.get_input_manager()
        input_handler.add_key_press_handler(self._handle_key_press)
        input_handler.add_key_release_handler(self._handle_key_release)
        
    def _handle_key_press(self, event_data):
        key = event_data.key

        if self._pan_toggle_pressed and _handle_pan_keys(key, self._pannable_backend,
                                                         self._pan_size):
            return True
        elif key == _PAN_TOGGLE_BUTTON:
            self._pan_toggle_pressed = True
            return True

        return False

    def _handle_key_release(self, event_data):
        if not self._pan_toggle_pressed:
            return

        key = event_data.key
        if key == _PAN_TOGGLE_BUTTON:
            self._pan_toggle_pressed = False
