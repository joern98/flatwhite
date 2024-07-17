import logging
import os
import time
import platform

from twisted.internet import reactor

from .sonos import SonosService
from .gui import *
from .constants import RESOURCE_PATH, BLACK, GRAY_DARK, GRAY_LIGHT, WHITE

if platform.system() == "Linux":
    from .output import EPD as Output
elif platform.system() in ["Windows", "Darwin"]:
    from .output import ImageShow as Output

logging.basicConfig(level=logging.DEBUG)

logging.debug(f"RESOURCE_PATH = {RESOURCE_PATH}")

WIDTH = 264
HEIGHT = 176

textbox_title = None
textbox_artist = None


def setup_gui(output):
    global textbox_title, textbox_artist

    PAD_X = 2
    PAD_Y = 2
    b = GUI.builder().set_output(output).set_size(WIDTH, HEIGHT)

    textbox_title = Textbox(PAD_X, PAD_Y, WIDTH-PAD_X-1, PAD_Y+77, "...", font=Textbox.LARGE, color=BLACK)
    textbox_artist = Textbox(PAD_X, PAD_Y+78, WIDTH-PAD_X-1, HEIGHT-PAD_Y-1, "...", font=Textbox.SMALL, color=GRAY_DARK)
    b.add_element(textbox_title).add_element(textbox_artist)
    return b.build()
     
def main():
    output = Output()
    gui = setup_gui(output)    

    sonos_service = SonosService()

    def change_callback(title, artist):
        global textbox_title, textbox_artist
        textbox_title.text = title
        textbox_artist.text = artist
        gui.update()
        
    sonos_service.on_change(change_callback)

    def before_shutdown():
        output.clear()
        output.clean()

    reactor.addSystemEventTrigger("before", "shutdown", before_shutdown)
