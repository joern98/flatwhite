import logging
import os
import time
import platform

import soco
from soco import events_twisted
soco.config.EVENTS_MODULE = events_twisted
from twisted.internet import reactor


from PIL import Image, ImageDraw, ImageFont
from .ui.Component import Component, Text, ProgressBar
from .ui.Layout import Layout, VerticalLayout, HorizontalLayout

if platform.system() == "Linux":
    from .display.epd import EPD as Display
elif platform.system() == "Windows":
    from .display.display import DebugDisplay as Display

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

def setup_sonos():
     sonos = soco.SoCo("192.168.178.26")
     logging.info(sonos.player_name)
     logging.info(sonos.ip_address)
     return sonos

     
def main():
    epd = Display()

    sonos = setup_sonos()

    try:
        image = Image.new('1', (epd.width, epd.height), 0xff)
        draw = ImageDraw.Draw(image)
        draw.font = font18

        root = HorizontalLayout()
        root.size = image.size
        v1 = VerticalLayout()
        v1.append_child(Text("A", True), 1)
        v1.append_child(Text("B", True), 1)
        v1.append_child(Text("C", True), 1)
        v1.append_child(Text("D", True), 1)
        v2 = VerticalLayout()
        title_text = Text("...")
        title_text.padding = (4, 4, 4, 4)
        artist_text = Text("...")
        artist_text.padding = (4, 4, 4, 4)
        v2.append_child(title_text, 50)
        v2.append_child(artist_text, 30)
        #progress = ProgressBar()
        #progress.padding = (2, 2, 2, 2)
        #v2.append_child(progress, 10)
        #v2.append_child(Component(), 10)
        root.append_child(v1, 5)
        root.append_child(v2, 95)

        root.draw(draw)
        epd.show_image(image)     

        last_event_timestamp = 0        

        def on_av_event(event):
            nonlocal last_event_timestamp
            try:
                logging.debug(f"av_event {event.seq}")
                logging.debug(event.variables)
                logging.debug(event.timestamp)
                if event.timestamp - last_event_timestamp < 1:
                     return
                last_event_timestamp = event.timestamp
                track_info = sonos.get_current_track_info()
                title_text.text = track_info["title"]
                artist_text.text = track_info["artist"]
                image = Image.new('1', epd.size(), 0xff)
                draw = ImageDraw.Draw(image)
                draw.font = font18
                root.draw(draw)
                epd.show_image(image)

            except Exception as e:
                logging.error('There was an error handling the event')
                logging.debug(e)


        av_subscription: soco.events.Subscription = sonos.avTransport.subscribe().subscription
        av_subscription.callback = on_av_event


        def before_shutdown():
            epd.clear()
            epd.clean()

        reactor.addSystemEventTrigger("before", "shutdown", before_shutdown)
    
    except Exception as e:
         logging.error("An error occurred")
         logging.debug(e)
         exit(1)
