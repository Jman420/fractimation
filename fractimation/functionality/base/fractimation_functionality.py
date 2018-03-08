class FractimationFunctionality(object):

    _renderer = None

    def __init__(self, renderer):
        self._renderer = renderer

    def get_renderer(self):
        return self._renderer