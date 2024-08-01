import logging
import platform

from twisted.internet import reactor

from .constants import RESOURCE_PATH, BLACK, GRAY_DARK, GRAY_LIGHT, WHITE
from .input import KEY1_PRESSED, KEY2_PRESSED, KEY3_PRESSED, KEY4_PRESSED
from .views import CurrentTrackView, View, WeatherView, FontCheckerView

if platform.system() == "Linux":
    from .output import EPD as Output
elif platform.system() in ["Windows", "Darwin"]:
    from .output import ImageShow as Output

class FlatwhiteCore:

    def __init__(self) -> None:
        self.__output = Output()

        self.__current_track_view = CurrentTrackView()
        self.__current_track_view.initialize()
        self.__current_track_view.on_change(self.__on_view_change)
        self.__weather_view = WeatherView()
        self.__weather_view.initialize()
        self.__weather_view.on_change(self.__on_view_change)

        self.__font_checker_view = FontCheckerView()
        self.__font_checker_view.initialize()
        self.__font_checker_view.on_change(self.__on_view_change)

        self.__active_view = None

        KEY1_PRESSED.subscribe(self.__change_to_view_fn(self.__current_track_view))
        KEY2_PRESSED.subscribe(self.__change_to_view_fn(self.__weather_view))
        KEY3_PRESSED.subscribe(self.__change_to_view_fn(self.__font_checker_view))
        self.__change_to_view_fn(self.__font_checker_view)()
        
    def __change_to_view_fn(self, view: View):
        def impl():
            if self.__show(view.get()):
                self.__active_view = view

        return impl 
    
    
    def __on_view_change(self, view: View):
        if view == self.__active_view:
            self.__show(view.get())

    def __show(self, image):
        return self.__output.show_image(image, force_binary=True)

    def exit(self):
        self.__active_view = None
        self.__output.clear()
        self.__output.clean()
     
    
def main():
    
    flatwhite_core = FlatwhiteCore()

    KEY4_PRESSED.subscribe(reactor.stop)

    def before_shutdown():
        flatwhite_core.exit()
        KEY4_PRESSED.unsubscribe(reactor.stop)

    reactor.addSystemEventTrigger("before", "shutdown", before_shutdown)
