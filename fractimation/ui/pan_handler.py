class PanHandler(object):

    _pannable_backend = None
    _viewer = None

    def __init__(self, pannable_backend, viewer):
        self._pannable_backend = pannable_backend
        self._viewer = viewer

        input_handler = self._viewer.get_input_manager()
        input_handler.add_key_press_handler(self._handle_key_press)
        
    def _handle_key_press(self, event_data):
        pass
