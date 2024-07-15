import logging

import soco
from soco import events_twisted
soco.config.EVENTS_MODULE = events_twisted

import json


class SonosService:

    def __init__(self) -> None:
        try:
            self.__sonos = soco.SoCo("192.168.178.26")
            logging.info(f"Connected to Sonos Speaker '{self.__sonos.player_name}' with ip adress {self.__sonos.ip_address}")
        except Exception as e:
            logging.error("Failed to connect to Sonos speaker with IP adress 192.168.178.26")
            raise e
    
        self.__current_track_uri = None

        self.__on_change_callback = None

        self.__sub_avTransport = self.__sonos.avTransport.subscribe().subscription
        self.__sub_avTransport.callback = self.__avt_event_callback

    def __avt_event_callback(self, event):        
        if event.variables["current_track_uri"] == self.__current_track_uri:
            return
        self.__current_track_uri = event.variables["current_track_uri"]

        track_meta_data = event.variables["current_track_meta_data"]
        self.__on_change_callback(track_meta_data.title, track_meta_data.creator)

    def on_change(self, callback):
        self.__on_change_callback = callback

        
    

    
