from io import BytesIO
import requests


from PIL import Image

from .gui import Textbox, GUIImage, GUI_Renderer
from .constants import RESOURCE_PATH, BLACK, GRAY_DARK, GRAY_LIGHT, WHITE, WIDTH, HEIGHT
from .sonos import SonosService, TrackDataPayload

class View:

    def __init__(self) -> None:
        self.__renderer = GUI_Renderer(WIDTH, HEIGHT)
        self._elements = []
        self._on_change_callback = None

    def get(self) -> Image.Image:
        self.__renderer.render(self._elements)
        return self.__renderer.get_image()
    
    def on_change(self, callback):
        self._on_change_callback = callback


class CurrentTrackView(View):

    def __init__(self) -> None:
        super().__init__()
        self.__textbox_title = Textbox(0, 0, WIDTH-1, 77, "...", font=Textbox.LARGE, color=BLACK)
        self.__textbox_artist = Textbox(0, 78, WIDTH-100-0-1, HEIGHT-1, "...", font=Textbox.SMALL, color=GRAY_DARK)
        self.__image_album_art = GUIImage(WIDTH-100-0, HEIGHT-100, WIDTH-1-0, HEIGHT-1)
        
        self._elements.extend([self.__textbox_artist, self.__textbox_title, self.__image_album_art])


    def init(self):
        self.__sonos_service = SonosService()
        self.__sonos_service.on_change(self.sonos_change_callback)    


    def sonos_change_callback(self, payload: TrackDataPayload):
        self.__textbox_title.text = payload.title
        self.__textbox_artist.text = payload.artist
        album_art_response = requests.get(payload.album_art_uri)
        album_art = Image.open(BytesIO(album_art_response.content))
        self.__image_album_art.set_image(album_art)
        self._on_change_callback(self)
