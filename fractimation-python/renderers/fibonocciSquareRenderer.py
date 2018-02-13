# http://pi3.sites.sheffield.ac.uk/tutorials/week-1-fibonacci

PHI = (1 + 5**0.5) / 2.0
def getFibonocciNumber(index):
    return int(round((PHI**index - (1 - PHI)**index) / 5**0.5))

class fibonocciSquareRenderer(object):
    """Fractal Renderer for Fibonocci Squares"""

    _squareCache = None
