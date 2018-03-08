from ..helpers.playback import restart_playback, repopulate_render_cache

_PAN_TOGGLE_BUTTON = '`'
_SHIFT_LEFT_BUTTON = 'left'
_SHIFT_RIGHT_BUTTON = 'right'
_SHIFT_DOWN_BUTTON = 'down'
_SHIFT_UP_BUTTON = 'up'

_DEFAULT_PAN_SIZE = 0.05

def _handle_pan_keys(key, pannable_backend, pan_size):
    handled = True

    real_number_pan_size = 0
    imaginary_number_pan_size = 0
    if key == _SHIFT_LEFT_BUTTON:
        real_number_pan_size = -pan_size
    elif key == _SHIFT_RIGHT_BUTTON:
        real_number_pan_size = pan_size
    elif key == _SHIFT_UP_BUTTON:
        imaginary_number_pan_size = -pan_size
    elif key == _SHIFT_DOWN_BUTTON:
        imaginary_number_pan_size = pan_size
    else:
        handled = False

    if handled:
        pannable_backend.pan_range(real_number_pan_size, imaginary_number_pan_size)

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
            renderer = self._pannable_backend.get_renderer()
            animation_handler = self._viewer.get_animation_manager()
            current_frame_num = animation_handler.get_frame_number()

            renderer.populate_render_cache(current_frame_num + 1)
            animation_handler.render(current_frame_num)

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
