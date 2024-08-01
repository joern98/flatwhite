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
    
    def show_image(self, image: Image.Image, force_binary=False) -> bool:
        return False

    def clear(self):
        pass

    def clean(self):
        pass

# ImageShow output display for debuggung purposes, using PIL.Image.show()
class ImageShow(Output):

    def __init__(self, width = 264, height = 176) -> None:
        super().__init__(width, height)

    def show_image(self, image: Image.Image, force_binary=False) -> bool:
        if force_binary:
            image = image.point(lambda x: 255 if x > 248 else 0, '1')
        image.show(f"ImageShow, {self.width}x{self.height}")
        return True


# EPD (E-Paper Display) output
class EPD(Output):

    def __init__(self) -> None:
        try:
            self.epd = epd2in7_V2.EPD()
        except Exception as e:
            logging.critical("Failed to create EPD class!")
            logging.debug(e)

        self.__lock = False
        super().__init__(self.epd.height, self.epd.width)

    def show_image(self, image: Image.Image, force_binary=False):
        success = False
        logging.debug(f"EPD is locked for {image.__repr__()}: {self.__lock}")
        if not self.__lock:
            self.__lock = True
            try:
                if image.mode == '1' or force_binary:
                    self.__show_image_binary(image)
                    success = True
                elif image.mode == 'L':
                    self.__show_image_greyscale(image)
                    success = True
                else:
                    logging.error(f"Image mode not supported for {image.__repr__()}!")
                
            except:
                self.clean()
                logging.error(f"An error occured during image display of {image.__repr__()}!")

            finally:
                self.__lock = False
        logging.debug(f"EPD show_image was successful for {image.__repr__()}: {success}")
        return success

    def __show_image_greyscale(self, image: Image.Image):
        try:
            self.epd.init()
            self.epd.Init_4Gray()
            self.epd.display_4Gray(self.epd.getbuffer_4Gray(image))
            self.epd.sleep()
        except:
            raise

    def __show_image_binary(self, image: Image.Image):
        if image.mode == 'L':
            image = image.point(lambda x: 255 if x > 248 else 0, '1')
        try:
            self.epd.init_Fast()
            self.epd.display_Fast(self.epd.getbuffer(image))
            self.epd.sleep()
        except:
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