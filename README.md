# fractimation
A Fractal Animation Framework for Matplotlib

# Description
Fractimation is a framework and player meant for exploring and animating fractal iterations.
The framework can likely be used for general animation purposes as well.

# Supported Fractals
- Multibrot and Multi-Julia Sets
- Sierpinski Carpet and Triangles
- Fibonacci Squares and Golden Spiral

# Features
- Iteration caching for playback scrubbing
- Support custom color maps
- Infinite zoom support with selectable area
- Save animations as video
- Support Cache Preheating for all renderers

# Dependencies
- Matplotlib (https://matplotlib.org/)
- numpy (http://www.numpy.org/)
- plotplayer (https://github.com/Jman420/plotplayer)

# Usage
## Zoom Controls (for Fractal Equations like Multibrot and Multi-Julia):
- Zoom Selection : Draw rectangle with left mouse button to select area to zoom
- Zoom In : Double click left mouse button
- Zoom Out : Single click right mouse button

## Keyboard Shortcuts :
* Play/Stop - Space & Enter
* Skip Ahead - Right
* Skip Back - Left
* Jump Ahead - Up
* Jump Back - Down
* Skip to Beginning - Home
* Skip to End - End

## Saving as Video
To save an animation as a video press and hold the 's' key and then press one of the following keys
to select the output format:
* V - mp4 video using ffmpeg (must have ffmpeg installed)
* H - HTML5 video
* J - Javascript video

## Matplotlib Controls
See https://matplotlib.org/users/navigation_toolbar.html for more built in Matplotlib controls.

# Examples
See [fractimation_test.py](fractimation-python/fractimation_test.py), [multibrotRenderer.py](fractimation-python/multibrotRenderer.py), [multijuliaRenderer.py](fractimation-python/multijuliaRenderer.py)

# Issues
## Inaccurate Framerate
Matplotlib's FuncAnimation module does not seem to keep accurate frameRate, instead waiting
for a pre-defined interval between method calls.  This will result in longer playback times
than expected given the provided frameRate parameter.  For instance, an animation with 30
frames at a frameRate of 30 frames per second should complete in 1 second, but if the
animation function on average takes 0.01 seconds then the full playback time will be
1.30 seconds.

A dynamic sleep timer is needed to smooth the framerate by determining the difference
between the wait interval and the last call to render.  For example, if interval is 33.33
milliseconds and animation function takes 3.33 milliseconds to execute then sleep timer
should wait for 30 milliseconds before rendering the next frame.

This issue can be mitigated by caching each frame within the renderer instead of
calculating the frame each time.  This will provide accurate playback on playthroughs after
the initial playback.  Another option is preheating the renderer cache by rendering all
frames before showing the animation.