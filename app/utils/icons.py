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
    loading = resource_path('resources/icons/cil-loading.png')
    browser = resource_path('resources/icons/cil-browser.png')
    devices = resource_path('resources/icons/cil-devices.png')
    recode = resource_path('resources/icons/cil-camera-roll.png')
    arrow_left = resource_path('resources/icons/cil-caret-left.png')
    arrow_right = resource_path('resources/icons/cil-caret-right.png')
    arrow_top = resource_path('resources/icons/cil-caret-top.png')
    arrow_bottom = resource_path('resources/icons/cil-caret-bottom.png')
    screen_desktop = resource_path('resources/icons/cil-screen-desktop.png')
    cam = resource_path('resources/icons/cil-cam.png')
    
    mini = resource_path('resources/icons/icon_restore.png')
    bell = resource_path('resources/icons/cil-bell.png')
    
    
    
