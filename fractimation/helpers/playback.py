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
    