import videofig
import mandelbrot_videofig

width, height = 1024, 768
xmin, xmax = -2, 0.5
ymin, ymax = -1.25, 1.25
escapeValue = 2.0

mandelbrotRenderer = mandelbrot_videofig.mandelbrot_videofig(width, height, xmin, xmax, ymin, ymax, escapeValue)
videofig.videofig(50, mandelbrotRenderer.iterate, 3)