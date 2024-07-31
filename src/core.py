import logging
import platform

from twisted.internet import reactor

from .constants import RESOURCE_PATH, BLACK, GRAY_DARK, GRAY_LIGHT, WHITE
from .input import KEY1_PRESSED, KEY2_PRESSED, KEY3_PRESSED
from .views import CurrentTrackView, View, WeatherView

if platform.system() == "Linux":
    from .output import EPD as Output
elif platform.system() in ["Windows", "Darwin"]:
    from .output import ImageShow as Output
     
def main():

    output = Output()

    current_track_view = CurrentTrackView()
    current_track_view.initialize()
    weather_view = WeatherView()
    weather_view.initialize()

    def change_to_view(view: View):
        return lambda: output.show_image(view.get())
    
    KEY2_PRESSED.subscribe(change_to_view(current_track_view))
    KEY3_PRESSED.subscribe(change_to_view(weather_view))

    KEY1_PRESSED.subscribe(reactor.stop)

    change_to_view(weather_view)()

    def before_shutdown():
        output.clear()
        output.clean()

    reactor.addSystemEventTrigger("before", "shutdown", before_shutdown)
