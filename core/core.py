import logging
import os
import time
import platform

from PIL import Image, ImageDraw, ImageFont
from .ui.Component import Component
from .ui.Layout import Layout, VerticalLayout, HorizontalLayout
from .ui.Text import Text

if platform.system() == "Linux":
    from .display.epd import EPD as Display
elif platform.system() == "Windows":
    from .display.debug_display import DebugDisplay as Display

logging.basicConfig(level=logging.DEBUG)

RESOURCE_PATH = os.path.join(os.path.dirname(__file__), "..", "res")
logging.debug(f"RESOURCE_PATH = {RESOURCE_PATH}")

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

def main():
    epd = Display()

    try:
        image = Image.new('1', (epd.width, epd.height), 0xff)
        draw = ImageDraw.Draw(image)
        draw.font = font18

        root = HorizontalLayout()
        root.size = image.size
        v1 = VerticalLayout()
        v1.append_child(Text("ABC"), 1)
        v1.append_child(Text("123"), 1)
        v2 = VerticalLayout()
        v2.append_child(Text("DEF"), 1)
        v2.append_child(Text("456"), 1)
        root.append_child(v1, 2)
        root.append_child(v2, 1)
        root.draw(draw)


        epd.show_image(image)

        time.sleep(5)

        epd.clear()
        epd.clean()

    except KeyboardInterrupt:
        logging.warning("Keyboard interrupt, clear and exit")
        epd.clear()
        epd.clean()
        exit(1) 