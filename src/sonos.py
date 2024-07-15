import logging

import soco
from twisted.internet import reactor


class SonosService:

    def __init__(self) -> None:
        try:
            self.__sonos = soco.SoCo("192.168.178.26")
            logging.info(f"Connected to Sonos Speaker '{self.__sonos.player_name}' with ip adress {self.__sonos.ip_address}")
        except Exception as e:
            logging.error("Failed to connect to Sonos speaker with IP adress 192.168.178.26")
            raise e
        
    
    
