from io import BytesIO
import logging
import os
import time
import platform

import requests
from twisted.internet import reactor

from .sonos import SonosService, TrackDataPayload
from .gui import *
from .constants import RESOURCE_PATH, BLACK, GRAY_DARK, GRAY_LIGHT, WHITE
from .input import KEY1_PRESSED, KEY2_PRESSED

if platform.system() == "Linux":
    from .output import EPD as Output
elif platform.system() in ["Windows", "Darwin"]:
    from .output import ImageShow as Output

logging.basicConfig(level=logging.INFO, filename="flatwhite_log.txt", filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug(f"RESOURCE_PATH = {RESOURCE_PATH}")

WIDTH = 264
HEIGHT = 176

textbox_title = None
textbox_artist = None
guiimage_album_art = None


def setup_gui(output):
    global textbox_title, textbox_artist, guiimage_album_art

    PAD_X = 2
    PAD_Y = 2
    b = GUI.builder().set_output(output).set_size(WIDTH, HEIGHT)

    textbox_title = Textbox(PAD_X, PAD_Y, WIDTH-PAD_X-1, PAD_Y+77, "...", font=Textbox.LARGE, color=BLACK)
    textbox_artist = Textbox(PAD_X, PAD_Y+78, WIDTH-PAD_X-1, HEIGHT-PAD_Y-1, "...", font=Textbox.SMALL, color=GRAY_DARK)
    guiimage_album_art = GUIImage(WIDTH-100-PAD_X, HEIGHT-100-PAD_Y, WIDTH-1-PAD_X, HEIGHT-1-PAD_Y, Image.new('L', (64, 64), GRAY_LIGHT))
    b.add_element(textbox_title).add_element(textbox_artist).add_element(guiimage_album_art)
    return b.build()
     
def main():
    output = Output()
    gui = setup_gui(output)    

    sonos_service = SonosService()

    def change_callback(payload: TrackDataPayload):
        global textbox_title, textbox_artist, guiimage_album_art
        textbox_title.text = payload.title
        textbox_artist.text = payload.artist
        album_art_response = requests.get(payload.album_art_uri)
        album_art = Image.open(BytesIO(album_art_response.content))
        album_art.show()
        guiimage_album_art.set_image(album_art)
        gui.update()
        
    sonos_service.on_change(change_callback)    

    KEY1_PRESSED.subscribe(reactor.stop)

    def before_shutdown():
        output.clear()
        output.clean()

    reactor.addSystemEventTrigger("before", "shutdown", before_shutdown)
