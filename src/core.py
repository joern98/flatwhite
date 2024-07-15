import logging
import os
import time
import platform

import soco
from soco import events_twisted
soco.config.EVENTS_MODULE = events_twisted
from twisted.internet import reactor
from PIL import Image, ImageDraw, ImageFont

from .gui import *

if platform.system() == "Linux":
    from .output import EPD as Output
elif platform.system() in ["Windows", "Darwin"]:
    from .output import ImageShow as Output

logging.basicConfig(level=logging.DEBUG)

RESOURCE_PATH = os.path.join(os.path.dirname(__file__), "..", "res")
logging.debug(f"RESOURCE_PATH = {RESOURCE_PATH}")

BLACK = 0x00
WHITE = 0xFF

WIDTH = 264
HEIGHT = 176

font18 = ImageFont.truetype(os.path.join(RESOURCE_PATH, "Font.ttc"), 18)

def get_test_image_h(width, height):
        # Horizontal image, epd.height is the long side with 276 pixels
        # 264x176

        image = Image.new('1', (width, height), 0xFF)
        draw = ImageDraw.Draw(image)
        draw.font = font18
        draw.rectangle((0, 0, width-1, height-1), outline=0)
        draw.text((0, 0), "(0, 0)", fill=0)
        draw.text((width//2, height//2), "Center", fill=0, anchor="mm")
        draw.text((0, height-1), "(0, 175)", fill=0, anchor="ld") 
        draw.text((width-1, height-1), "(263, 175)", fill=0, anchor="rd") 
        draw.text((width-1, 0), "(263, 0)", fill=0, anchor="ra") 
        return image

def setup_sonos():
     sonos = soco.SoCo("192.168.178.26")
     logging.info(sonos.player_name)
     logging.info(sonos.ip_address)
     return sonos

def setup_gui(output):
    b = GUI.builder()
    b.set_output(output)
    b.set_size(WIDTH, HEIGHT)
    b.rectangle(0, 0, WIDTH-1, HEIGHT-1)
    b.rectangle(WIDTH//3, HEIGHT//3, WIDTH-1, HEIGHT-1)
    b.rectangle(2*WIDTH//3, 2*HEIGHT//3, WIDTH-1, HEIGHT-1)
    b.textbox(2*WIDTH//3, 2*HEIGHT//3, WIDTH-1, HEIGHT-1, "Hello World, my ass is on fire up in here")
    return b.build()
     
def main():
    output = Output()
    gui = setup_gui(output)    
    gui.update()

    def before_shutdown():
        output.clear()
        output.clean()

    reactor.addSystemEventTrigger("before", "shutdown", before_shutdown)
