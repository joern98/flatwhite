import logging
import platform

from twisted.internet import reactor

from .constants import RESOURCE_PATH, BLACK, GRAY_DARK, GRAY_LIGHT, WHITE
from .input import KEY1_PRESSED, KEY2_PRESSED
from .views import CurrentTrackView, View, WeatherView

if platform.system() == "Linux":
    from .output import EPD as Output
elif platform.system() in ["Windows", "Darwin"]:
    from .output import ImageShow as Output
     
def main():
    KEY1_PRESSED.subscribe(reactor.stop)

    output = Output()
    #view = CurrentTrackView()
    view = WeatherView()

    def on_view_change_callback(view: View):
        output.show_image(view.get())
        
    view.on_change(on_view_change_callback)
    view.initialize()



    def before_shutdown():
        output.clear()
        output.clean()

    reactor.addSystemEventTrigger("before", "shutdown", before_shutdown)
