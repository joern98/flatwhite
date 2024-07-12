from typing import Tuple
import logging

from PIL import Image

# Base Display class
class Display:

    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
    
    def size(self):
        return (self.width, self.height)

    def show_image(self, image: Image.Image):
        pass

    def clear(self):
        pass

    def clean(self):
        pass


# ImageShow output display for debuggung purposes, using PIL.Image.show()
class ImageShow(Display):

    def __init__(self, width = 264, height = 176) -> None:
        super().__init__(width, height)

    def show_image(self, image: Image.Image):
        image.show(f"ImageShow, {self.width}x{self.height}")


# EPD (E-Paper Display) output
class EPD(Display):

    def __init__(self) -> None:
        from lib.waveshare_epd import epd2in7_V2
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