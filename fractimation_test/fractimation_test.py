import matplotlib.pylab as pylab
import numpy
import time

from plotplayer.plotplayer import PlotPlayer
from plotplayer.managers.window_manager import WindowManager

from fractimation.ui.zoom_handler import ZoomHandler
from fractimation.functionality.zoomable_complex_range import ZoomableComplexRange
from fractimation.ui.pan_handler import PanHandler
from fractimation.functionality.pannable_complex_range import PannableComplexRange

from fractimation.data_models.complex_range_params import ComplexRangeParams
from fractimation.data_models.dimension_params import DimensionParams
from fractimation.data_models.image_params import ImageParams
from fractimation.data_models.formula_params import FormulaParams

from fractimation.helpers.formula_tools import generate_complex_range

from fractimation.iterators.multibrot import Multibrot
from fractimation.iterators.multijulia import Multijulia
from fractimation.iterators.newton_method import NewtonMethod

from fractimation.renderers.cached_image_renderer import CachedImageRenderer

# General Brot & Julia Fractal Parameters
width, height = 1280, 720                              # Width and Height of the image
                                                       # ^^ quick ref : 480p;(640, 480) 720p;(1280, 720) 1080p;(1920, 1080) UHD/4K;(3840, 2160) 8K;(7680, 4320)
max_iterations = 60                                    # Total number of iterations of fractal equation
                                                       # ^^ Careful with this value; we are caching each frame
color_map = "viridis"                                  # Any valid color map name or combination (default : viridis)
                                                       # ^^ reference : https://matplotlib.org/examples/color/colormaps_reference.html

# Mandelbrot Set
real_number_min, real_number_max = -2.0, 0.5               # Min & Max values for X values in fractal equation
imaginary_number_min, imaginary_number_max = -1.25, 1.25   # Min & Max values for Y values in fractal equation
constant_real_number, constant_imaginary_number = 0.0, 0.0 # Initial Z Value
power = 2                                                  # Power to raise Z value to for each iteration of fractal equation
escape_value = 2.0                                         # Limit at which Z values will reach infinity

window_mngr = WindowManager(window_title="Multibrot Set", toolbar_visible=False)
viewer = PlotPlayer(window_mngr)

image_dimensions = DimensionParams(width, height)
z_values_params = ComplexRangeParams(constant_real_number, constant_real_number, constant_imaginary_number, constant_imaginary_number)
c_values_params = ComplexRangeParams(real_number_min, real_number_max, imaginary_number_min, imaginary_number_max)
fractal = Multibrot(c_values_params, image_dimensions, escape_value, z_values_range_params=z_values_params)

image_params = ImageParams(recolor_image=True)
renderer = CachedImageRenderer(viewer.get_render_manager().get_animation_axes(), fractal, image_dimensions, image_params)
renderer.populate_render_cache(max_iterations)

zoom_backend = ZoomableComplexRange(renderer)
zoom_handler = ZoomHandler(zoom_backend, viewer)

pan_backend = PannableComplexRange(renderer)
pan_handler = PanHandler(pan_backend, viewer)

viewer.initialize(max_iterations, renderer.render_to_canvas, "multibrotFractal")

PlotPlayer.show_players()

# Julia Set
real_number_min, real_number_max = -1.5, 1.5               # Min & Max values for X values in fractal equation
imaginary_number_min, imaginary_number_max = -1.5, 1.5     # Min & Max values for Y values in fractal equation
constant_real_number, constant_imaginary_number = 0.0, 0.8 # Constant C value
power = 2                                                  # Power to raise Z value to for each iteration of fractal equation
escape_value = 10.0                                        # Limit at which Z values will reach infinity

window_mngr = WindowManager(window_title="Julia Set", toolbar_visible=False)
viewer = PlotPlayer(window_mngr)

image_dimensions = DimensionParams(width, height)
z_values_params = ComplexRangeParams(real_number_min, real_number_max, imaginary_number_min, imaginary_number_max)
c_values_params = ComplexRangeParams(constant_real_number, constant_real_number, constant_imaginary_number, constant_imaginary_number)
fractal = Multijulia(z_values_params, image_dimensions, escape_value, c_values_range_params=c_values_params)

image_params = ImageParams(recolor_image=True)
renderer = CachedImageRenderer(viewer.get_render_manager().get_animation_axes(), fractal, image_dimensions, image_params)
renderer.populate_render_cache(max_iterations)

zoom_backend = ZoomableComplexRange(renderer)
zoom_handler = ZoomHandler(zoom_backend, viewer)

viewer.initialize(max_iterations, renderer.render_to_canvas, "multijuliaFractal")

# Newton Fractal
real_number_min, real_number_max = -5, 5                   # Min & Max values for X values in fractal equation
imaginary_number_min, imaginary_number_max = -5, 5         # Min & Max values for Y values in fractal equation
constant_real_number, constant_imaginary_number = 1.0, 0.0 # Constant C value
coefficient_array = [ -1, 0, 0, 0, 1 ]                     # Representation of polynomial equation coefficients in accending order (ie. c + x + x**2 + ... + x**n)
escape_value = 1e-4

window_mngr = WindowManager(window_title="Newton Fractal", toolbar_visible=False)
viewer = PlotPlayer(window_mngr)

image_dimensions = DimensionParams(width, height)
z_values_params = ComplexRangeParams(real_number_min, real_number_max, imaginary_number_min, imaginary_number_max)
c_values_params = ComplexRangeParams(constant_real_number, constant_real_number, constant_imaginary_number, constant_imaginary_number)
formula_params = FormulaParams(coefficient_array, escape_value)
fractal = NewtonMethod(z_values_params, c_values_params, image_dimensions, formula_params)

renderer = CachedImageRenderer(viewer.get_render_manager().get_animation_axes(), fractal, image_dimensions, image_params)
renderer.populate_render_cache(max_iterations)

zoom_backend = ZoomableComplexRange(renderer)
zoom_handler = ZoomHandler(zoom_backend, viewer)

viewer.initialize(max_iterations, renderer.render_to_canvas, "newtonFractal")

# Render Viewers
PlotPlayer.show_players()
