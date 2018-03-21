from matplotlib.image import AxesImage

from ..app_events.cache_events import CacheEvents

class DrawHandler(object):

    _renderer = None
    _render_axes = None
    _caption_label = None
    _draw_canvas = None

    def __init__(self, renderer, render_axes):
        image_params = renderer.get_image_params()
        self._draw_canvas = AxesImage(render_axes, cmap=image_params.color_map)
        self._draw_canvas.set_clip_path(render_axes.patch)
        render_axes.add_image(self._draw_canvas)

        self._caption_label = render_axes.text(0.5, 0.5,
                                               str(),
                                               horizontalalignment='center',
                                               verticalalignment='center',
                                               fontsize=18,
                                               transform=render_axes.transAxes,
                                               visible=False)

        if hasattr(renderer, 'events') and isinstance(renderer.events, CacheEvents):
            renderer.events.on_start_populating_cache += self.show_caption
            renderer.events.on_complete_populating_cache += self.hide_caption

        self._renderer = renderer
        self._render_axes = render_axes

    def draw(self, frame_num, axes):
        frame = self._renderer.render(frame_num)
        self._draw_canvas.set_data(frame)
        self._draw_canvas.autoscale()
        self._draw_canvas.set_extent(self._draw_canvas.get_extent())

    def show_caption(self, text):
        figure = self._render_axes.get_figure()
        self._caption_label.set_text(text)
        self._caption_label.set_visible(True)
        figure.canvas.draw()

    def hide_caption(self):
        figure = self._render_axes.get_figure()
        self._caption_label.set_visible(False)
        figure.canvas.draw()
