from io import BytesIO
import logging
import requests
import datetime

from PIL import Image
from twisted.internet import reactor, task

from  .weather import WeatherService

from .gui import Textbox, GUIImage, GUI_Renderer, Line
from .constants import RESOURCE_PATH, BLACK, GRAY_DARK, GRAY_LIGHT, WHITE, WIDTH, HEIGHT
from .sonos import SonosService, TrackDataPayload

class View:

    def __init__(self) -> None:
        self.__renderer = GUI_Renderer(WIDTH, HEIGHT, mode='L')
        self._elements = []
        self._on_change_callback = None

    def get(self) -> Image.Image:
        self.__renderer.render(self._elements)
        return self.__renderer.get_image()
    
    def on_change(self, callback):
        self._on_change_callback = callback

    def _changed(self):
        if self._on_change_callback is not None:
            self._on_change_callback(self)



class CurrentTrackView(View):

    def __init__(self) -> None:
        super().__init__()
        self.__textbox_title = Textbox(0, 0, WIDTH-1, 77, "...", font=Textbox.LARGE, color=BLACK)
        self.__textbox_artist = Textbox(0, 78, WIDTH-100-1, HEIGHT-1, "...", font=Textbox.SMALL, color=GRAY_DARK)
        self.__image_album_art = GUIImage(WIDTH-100-0, HEIGHT-100, WIDTH-1, HEIGHT-1)
        self.__separator = Line(0, HEIGHT-42, WIDTH-1, HEIGHT-42, color=GRAY_DARK)
        self.__next_title = Textbox(0, HEIGHT-40, WIDTH-100, HEIGHT-1, "...", font=Textbox.SMALL, color=GRAY_DARK, wrap=False)
        self.__next_artist = Textbox(0, HEIGHT-20, WIDTH-100, HEIGHT-1, "...", font=Textbox.SMALL, color=GRAY_LIGHT, wrap=False)
        
        self._elements.extend([
            self.__textbox_artist,
            self.__textbox_title,
            self.__separator,
            # self.__image_album_art, 
            self.__next_title, 
            self.__next_artist
        ])

    def initialize(self):
        self.__sonos_service = SonosService()
        self.__sonos_service.on_change(self.sonos_change_callback)
    	
    def sonos_change_callback(self, payload: TrackDataPayload):
        self.__textbox_title.text = payload.title
        self.__textbox_artist.text = payload.artist
        self.__next_title.text = payload.next_title
        self.__next_artist.text = payload.next_artist
        album_art_response = requests.get(payload.album_art_uri)
        album_art = Image.open(BytesIO(album_art_response.content))
        self.__image_album_art.set_image(album_art)
        self._changed()


class WeatherView(View):
    HALF_HEIGHT = HEIGHT//2
    PADDING = 2

    def __init__(self) -> None:
        super().__init__()
        self.__separator = Line(0, self.HALF_HEIGHT, WIDTH-1, self.HALF_HEIGHT)
        self.__current_temperature = Textbox(self.PADDING, self.PADDING, WIDTH-1-self.PADDING, self.PADDING + 20, "xx °C")
        self.__next_temperature_max = Textbox(self.PADDING, self.HALF_HEIGHT + self.PADDING, WIDTH-1-self.PADDING, self.PADDING + 20, "xx °C")
        self.__next_temperature_min = Textbox(self.PADDING, self.HALF_HEIGHT + self.PADDING + 26, WIDTH-1-self.PADDING, self.HALF_HEIGHT + self.PADDING + 46, "xx °C", font=Textbox.SMALL)
        self.__next_date = Textbox(5*WIDTH//8, self.PADDING + self.HALF_HEIGHT, WIDTH-1, self.PADDING + self.HALF_HEIGHT + 20, "05.05.1998", font=Textbox.SMALL, wrap=False)

        self._elements.extend([
            self.__separator, 
            self.__current_temperature, 
            self.__next_temperature_max, 
            self.__next_temperature_min, 
            self.__next_date
        ])

    def initialize(self):
        self.__weather_sevice = WeatherService()
        self.update()

    def update(self):
        weather = self.__weather_sevice.get_current_weather()
        temperature_unit_str = weather["current_units"]["temperature_2m"]
        self.__current_temperature.text = str(weather["current"]["temperature_2m"]) + ' ' + temperature_unit_str

        # only flip to actual next day after 7am
        current_time = datetime.datetime.now()
        next_day_index = 0 if current_time.hour < 7 else 1
        logging.info(f"Displaying weather forecast for {weather['daily']['time'][next_day_index]}")
        self.__next_temperature_max.text = str(weather["daily"]["temperature_2m_max"][next_day_index]) + ' ' + temperature_unit_str
        self.__next_temperature_min.text = str(weather["daily"]["temperature_2m_min"][next_day_index]) + ' ' + temperature_unit_str
        iso_date = datetime.date.fromisoformat(weather['daily']['time'][next_day_index])
        self.__next_date.text = iso_date.strftime("%d.%m.%Y")
        self._changed()
        