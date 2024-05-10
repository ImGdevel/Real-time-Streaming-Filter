import sys, os



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Icons:
    play_button = resource_path('resources/icons/cil-media-play.png')
    puse_button = resource_path('resources/icons/cil-media-pause.png')
    stop_button = resource_path('resources/icons/cil-media-stop.png')
    clone = resource_path('resources/icons/cil-clone.png')
    plus = resource_path('resources/icons/cil-plus.png')
    dust_bin = resource_path('resources/icons/cil-dust-bin.png')
    smiley_sticker = resource_path('resources/icons/cil-smiley-sticker.png')
    folder_open = resource_path('resources/icons/cil-folder-open')
    reload = resource_path('resources/icons/cil-reload.png')
    camera = resource_path('resources/icons/cil-camera.png')
    
