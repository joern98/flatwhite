import logging
import os
import time
import platform

from twisted.internet import reactor

from .sonos import SonosService
from .gui import *
from .config import RESOURCE_PATH

if platform.system() == "Linux":
    from .output import EPD as Output
elif platform.system() in ["Windows", "Darwin"]:
    from .output import ImageShow as Output

logging.basicConfig(level=logging.DEBUG)

logging.debug(f"RESOURCE_PATH = {RESOURCE_PATH}")

BLACK = 0x00
WHITE = 0xFF

WIDTH = 264
HEIGHT = 176

tb_title = None
tb_artist = None

def setup_gui(output):
    global tb_title, tb_artist

    PAD_X = 2
    PAD_Y = 2
    b = GUI.builder()
    b.set_output(output)
    b.set_size(WIDTH, HEIGHT)
    tb_title = b.textbox(PAD_X, PAD_Y, WIDTH-PAD_X-1, PAD_Y+49, "...")
    tb_artist = b.textbox(PAD_X, PAD_Y+50, WIDTH-PAD_X-1, HEIGHT-PAD_Y-1, "...")
    return b.build()
     
def main():
    output = Output()
    gui= setup_gui(output)    

    sonos_service = SonosService()

    def change_callback(title, artist):
        global tb_title, tb_artist
        tb_title.text = title
        tb_artist.text = artist
        gui.update()
        
    sonos_service.on_change(change_callback)

    def before_shutdown():
        output.clear()
        output.clean()

    reactor.addSystemEventTrigger("before", "shutdown", before_shutdown)
