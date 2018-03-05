import matplotlib.pylab as pylab
import numpy
import time

from plotplayer.plotplayer import PlotPlayer
from plotplayer.managers.window_manager import WindowManager

from fractimation.ui.zoom_handler import ZoomHandler
from fractimation.functionality.zoomable_complex_range import ZoomableComplexRange

from fractimation.data_models.complex_range_params import ComplexRangeParams
from fractimation.data_models.dimension_params import DimensionParams
from fractimation.data_models.image_params import ImageParams

from fractimation.helpers.formula_tools import generate_complex_range

from fractimation.iterators.multibrot import Multibrot
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

multibrot_window_mngr = WindowManager(window_title="Multibrot Set", toolbar_visible=False)
multibrot_viewer = PlotPlayer(multibrot_window_mngr)

image_dimensions = DimensionParams(width, height)
c_values_params = ComplexRangeParams(real_number_min, real_number_max, imaginary_number_min, imaginary_number_max)
multibrot_fractal = Multibrot(c_values_params, image_dimensions, escape_value)

multibrot_image_params = ImageParams(recolor_image=True)
multibrot_renderer = CachedImageRenderer(multibrot_viewer.get_render_manager().get_animation_axes(), multibrot_fractal, image_dimensions, multibrot_image_params)
multibrot_renderer.preheat_render_cache(max_iterations)

multibrot_zoom_backend = ZoomableComplexRange(multibrot_renderer)
multibrot_zoom_handler = ZoomHandler(multibrot_zoom_backend, multibrot_viewer)

multibrot_viewer.initialize(max_iterations, multibrot_renderer.render_to_canvas, "multibrotFractal")

PlotPlayer.show_players()

# Julia Set
multijulia_window_mngr = WindowManager(window_title="Julia Set", toolbar_visible=False)
multijulia_viewer = PlotPlayer(multijulia_window_mngr)
real_number_min, real_number_max = -1.5, 1.5               # Min & Max values for X values in fractal equation
imaginary_number_min, imaginary_number_max = -1.5, 1.5     # Min & Max values for Y values in fractal equation
constant_real_number, constant_imaginary_number = 0.0, 0.8 # Constant C value
power = 2                                                  # Power to raise Z value to for each iteration of fractal equation
escape_value = 10.0                                        # Limit at which Z values will reach infinity
multijulia_fractal = Multijulia(width, height, real_number_min, real_number_max, imaginary_number_min, imaginary_number_max,
                                        constant_real_number, constant_imaginary_number, power, escape_value, color_map)
multijulia_zoom_handler = ZoomHandler(multijulia_fractal, multijulia_viewer)
multijulia_viewer.initialize(max_iterations, multijulia_fractal.render, "multijuliaFractal")
multijulia_fractal.preheat_render_cache(max_iterations)

# Newton Fractal
newton_fractal_window_mngr = WindowManager(window_title="Newton Fractal", toolbar_visible=False)
newton_fractal_viewer = PlotPlayer(newton_fractal_window_mngr)
real_number_min, real_number_max = -5, 5                   # Min & Max values for X values in fractal equation
imaginary_number_min, imaginary_number_max = -5, 5         # Min & Max values for Y values in fractal equation
constant_real_number, constant_imaginary_number = 1.0, 0.0 # Constant C value
coefficient_array = [ -1, 0, 0, 0, 1 ]                     # Representation of polynomial equation coefficients in accending order (ie. c + x + x**2 + ... + x**n)
escape_value = 1e-4
newton_fractal = NewtonFractal(width, height, real_number_min, real_number_max, imaginary_number_min, imaginary_number_max,
                                      coefficient_array, constant_real_number, constant_imaginary_number, escape_value, color_map)
newton_zoom_handler = ZoomHandler(newton_fractal, newton_fractal_viewer)
newton_fractal_viewer.initialize(max_iterations, newton_fractal.render, "newtonFractal")
newton_fractal.preheat_render_cache(max_iterations)

PlotPlayer.show_players()

# Sierpinski Triangle (3**iteration triangles per iteration)
sierpinski_triangle_window_mngr = WindowManager(window_title="Sierpinski Triangle")
sierpinski_triangle_viewer = PlotPlayer(sierpinski_triangle_window_mngr)
sierpinski_triangle_viewer.get_render_manager().set_slider_visible(True)
sierpinski_triangle_iterations = 7                      # Be careful with this number; iterations explode at 3**iteration computations
sierpinski_triangle_line_widths = numpy.linspace(1.0, 0.1, sierpinski_triangle_iterations + 1)
sierpinski_triangle_fractal = SierpinskiTriangle(sierpinski_triangle_line_widths)
sierpinski_triangle_viewer.initialize(sierpinski_triangle_iterations, sierpinski_triangle_fractal.render, "sierpinskiTriangle")
sierpinski_triangle_fractal.preheat_render_cache(sierpinski_triangle_iterations)

# Sierpinski Carpet (8**iteration rectangles per iteration)
sierpinski_carpet_window_mngr = WindowManager(window_title="Sierpinski Carpet")
sierpinski_carpet_viewer = PlotPlayer(sierpinski_carpet_window_mngr)
sierpinski_carpet_viewer.get_render_manager().set_slider_visible(True)
sierpinski_carpet_iterations = 4                        # Be careful with this number; iterations explode at 8**iteration computations
sierpinski_carpet_line_widths = numpy.linspace(1.0, 0.1, sierpinski_carpet_iterations + 1)
sierpinski_carpet_fractal = SierpinskiCarpet(sierpinski_carpet_line_widths)
sierpinski_carpet_viewer.initialize(sierpinski_carpet_iterations, sierpinski_carpet_fractal.render,  "sierpinskiCarpet")
sierpinski_carpet_fractal.preheat_render_cache(sierpinski_carpet_iterations)

# Fibonacci Square
fibonacci_square_window_mngr = WindowManager(window_title="Fibonocci Square")
fibonacci_square_viewer = PlotPlayer(fibonacci_square_window_mngr)
fibonacci_square_viewer.get_render_manager().set_slider_visible(True)
fibonacci_square_iterations = 15
fibonacci_square_line_widths = numpy.linspace(0.1, 1.0, fibonacci_square_iterations + 1)
fibonacci_square_fractal = FibonacciSquare(fibonacci_square_line_widths)
fibonacci_square_viewer.initialize(fibonacci_square_iterations, fibonacci_square_fractal.render, "fibonocciSquare")
fibonacci_square_fractal.preheat_render_cache(fibonacci_square_iterations)

# Golden Spiral
golden_spiral_window_mngr = WindowManager(window_title="Golden Spiral")
golden_spiral_viewer = PlotPlayer(golden_spiral_window_mngr)
golden_spiral_viewer.get_render_manager().set_slider_visible(True)
golden_spiral_iterations = 15
golden_spiral_line_widths = numpy.linspace(0.01, 0.05, golden_spiral_iterations + 1)
golden_spiral_fractal = GoldenSpiral(golden_spiral_line_widths)
golden_spiral_viewer.initialize(golden_spiral_iterations, golden_spiral_fractal.render, "goldenSpiral")
golden_spiral_fractal.preheat_render_cache(golden_spiral_iterations)

# Render Viewers
PlotPlayer.show_players()
