import logging
import platform

from twisted.internet import reactor

from .constants import RESOURCE_PATH, BLACK, GRAY_DARK, GRAY_LIGHT, WHITE
from .input import KEY1_PRESSED, KEY2_PRESSED
from .views import CurrentTrackView, View

if platform.system() == "Linux":
    from .output import EPD as Output
elif platform.system() in ["Windows", "Darwin"]:
    from .output import ImageShow as Output
     
def main():
    KEY1_PRESSED.subscribe(reactor.stop)

    output = Output()
    view = CurrentTrackView()

    def on_view_change_callback(view: View):
        image, changed_regions = view.get()
        if len(changed_regions) > 1:
            output.show_image(image)
        else:
            output.partial_update(image, changed_regions[0])
        
    view.on_change(on_view_change_callback)
    view.init()



    def before_shutdown():
        output.clear()
        output.clean()

    reactor.addSystemEventTrigger("before", "shutdown", before_shutdown)
