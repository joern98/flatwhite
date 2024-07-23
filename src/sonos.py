from dataclasses import dataclass
import logging

import soco
from soco import events_twisted
soco.config.EVENTS_MODULE = events_twisted

import json

@dataclass
class TrackDataPayload:
    title: str
    artist: str
    album: str
    album_art_uri: str

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
        payload = TrackDataPayload(track_meta_data.title, track_meta_data.creator, track_meta_data.album, track_meta_data.album_art_uri)
        self.__on_change_callback(payload)

    def on_change(self, callback):
        self.__on_change_callback = callback

    def get_current_track_info(self):
        return self.__sonos.get_current_track_info()

        
    

    
