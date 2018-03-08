import time

def restart_playback(viewer):
    """
    Method to restart playback from the beginning

    Parameters :
      * viewer - An instance of PlotPlayer
    """
    render_handler = viewer.get_render_manager()
    animation_handler = viewer.get_animation_manager()

    viewer.stop()
    animation_handler.render(0)
    render_handler.enforce_limits()
    viewer.play()

def repopulate_render_cache(viewer, renderer, max_frames):
    window_handler = viewer.get_window_manager()
    figure = window_handler.get_figure()
    render_handler = viewer.get_render_manager()
    animation_handler = viewer.get_animation_manager()
    render_axes = render_handler.get_animation_axes()
    
    caption_text = render_axes.text(0.5, 0.5, "Repopulating render cache to current frame!",
                                   horizontalalignment='center', verticalalignment='center',
                                   fontsize=18, transform=render_axes.transAxes)
    figure.canvas.draw()
    
    renderer.populate_render_cache(max_frames)
    caption_text.remove()
    render_handler.render(max_frames, animation_handler.get_total_frames())
    