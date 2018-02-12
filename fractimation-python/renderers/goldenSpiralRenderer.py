# https://numerica.pt/2017/09/14/fibonacci-spiral-in-python/
# http://junilyd.github.io/blog/2014/08/13/fibonacci-mystery-pythonified/

import numpy

class goldenSpiralRenderer(object):
    """Fractal Renderer for the Golden Spiral"""

    _width = _height = None
    _goldenArcs = None

    def __init__(self, width, height):
        self.initialize(width, height)

    def initialize(self, width, height):
        return

    def render(self, frameNumber, axes):
        return