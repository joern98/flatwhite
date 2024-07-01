from PIL import Image

from .display import Display

class DebugDisplay(Display):

    def __init__(self, width = 264, height = 176) -> None:
        super().__init__(width, height)

    def show_image(self, image: Image.Image):
        image.show(f"Debug Display, {self.width}x{self.height}")