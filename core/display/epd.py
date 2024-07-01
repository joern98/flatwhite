import logging
import os
import time

from typing import *
from PIL import Image

from lib.waveshare_epd import epd2in7_V2

from .display import Display

class EPD(Display):

    def __init__(self, size: Tuple[int, int]) -> None:
        super().__init__(size)
        self.epd = epd2in7_V2.EPD()

    def show_image(image: Image.Image):
        epd.init_Fast()
        epd.display_Fast(epd.getbuffer(image))
        epd.sleep()