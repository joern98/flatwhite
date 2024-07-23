from typing import Tuple
import logging

from PIL import Image

try:
    from lib.waveshare_epd import epd2in7_V2
except:
    logging.warning("Failed to import epd2in7_V2 module, EPD will not work!")

# Base Display class
class Output:

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
class ImageShow(Output):

    def __init__(self, width = 264, height = 176) -> None:
        super().__init__(width, height)

    def show_image(self, image: Image.Image):
        image.show(f"ImageShow, {self.width}x{self.height}")

    def partial_update(self, image, bounds):
        self.show_image(image)


# EPD (E-Paper Display) output
class EPD(Output):

    def __init__(self) -> None:
        try:
            self.epd = epd2in7_V2.EPD()
        except Exception as e:
            logging.critical("Failed to create EPD class!")
            logging.debug(e)

        super().__init__(self.epd.height, self.epd.width)

    def show_image(self, image: Image.Image):
        try:
            self.epd.init()
            self.epd.Init_4Gray()
            self.epd.display_4Gray(self.epd.getbuffer_4Gray(image))
            self.epd.sleep()
        except:
            self.clean()
            raise

    def partial_update(self, image, bounds):
        try:
            self.epd.init()
            self.epd.display_Partial(self.epd.getbuffer(image), bounds[0], bounds[1], bounds[2], bounds[3])
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