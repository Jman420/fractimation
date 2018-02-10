# fractimation
A Fractal Animation Framework for Matplotlib

# Description
Fractimation is a framework and player meant for exploring and animating fractal iterations.
The framework can likely be used for general animation purposes as well.

# Features
- Multibrot and Multi-Julia Sets
- Iteration caching for playback scrubbing
- Support custom color maps
- Infinite zoom support

# Dependencies
- Matplotlib (https://matplotlib.org/)
- numpy (http://www.numpy.org/)
- plotplayer (https://github.com/Jman420/plotplayer)

# Usage
Zoom Controls :
- Zoom In : Draw rectangle with left mouse button to select area to zoom
- Zoom Out : Right click mouse button

Keyboard Shortcuts :
* Play - Space & Enter
* Skip Ahead 1 Frame - Right
* Skip Back 1 Frame - Left
* Skip to Beginning - Home
* Skip to End - End

# Examples
See [fractimation_test.py](fractimation-python/fractimation_test.py), [multibrotRenderer.py](fractimation-python/multibrotRenderer.py), [multijuliaRenderer.py](fractimation-python/multijuliaRenderer.py)