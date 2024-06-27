import os
import time
import logging
logging.basicConfig(level=logging.DEBUG)

from PIL import Image, ImageDraw, ImageFont

from lib.waveshare_epd import epd2in7_V2


RESOURCE_PATH = os.path.join(os.path.dirname(__file__), "res")
logging.debug(f"RESOURCE_PATH = {RESOURCE_PATH}")

font18 = ImageFont.truetype(os.path.join(RESOURCE_PATH, "Font.ttc"), 18)

def display_image(epd: epd2in7_V2.EPD, image: Image.Image):
    epd.init_Fast()
    epd.display_Fast(epd.getbuffer(image))
    epd.sleep()


def clear_image(epd: epd2in7_V2.EPD):
    epd.init()
    epd.Clear()
    epd.sleep()

def get_test_image_h(epd):
        # Horizontal image, epd.height is the long side with 276 pixels
        # 264x176
        width, height = epd.height, epd.width

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
    try:
        epd = epd2in7_V2.EPD()
    except Exception as e:
        logging.critical("Failed to create EPD class!")
        logging.debug(e)
        exit(1)

    try:
        # SIMPLE BINARY IMAGE
        image = get_test_image_h(epd)
        display_image(epd, image)
        
        time.sleep(5)

        clear_image(epd)

    except KeyboardInterrupt:
        logging.warning("Keyboard interrupt, clear and exit")
        clear_image(epd)
    
    except Exception as e:
        logging.error("An error occured during execution!")
        logging.debug(e)

    finally:
        logging.debug("Calling module_exit() for cleanup")
        epd2in7_V2.epdconfig.module_exit(cleanup=True)


if __name__ == "__main__":
    main()