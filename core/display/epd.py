import logging
import os
import time

from PIL import Image

from lib.waveshare_epd import epd2in7_V2

from .display import Display

class EPD(Display):

    def __init__(self) -> None:
        try:
            self.epd = epd2in7_V2.EPD()
        except Exception as e:
            logging.critical("Failed to create EPD class!")
            logging.debug(e)

        super().__init__(self.epd.height, self.epd.width)


    def show_image(self, image: Image.Image):
        try:
            self.epd.init_Fast()
            self.epd.display_Fast(self.epd.getbuffer(image))
            self.epd.sleep()
        except:
            self.clean()
            raise

    def clear(self):
        try:
            self.epd.init()
            self.epd.Clear()
            self.epd.sleep()
        except:
            self.clean()
            raise

    def clean(self):
        logging.debug("Calling module_exit() for cleanup")
        epd2in7_V2.epdconfig.module_exit(cleanup=True)