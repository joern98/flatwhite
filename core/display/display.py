from typing import Tuple
from PIL import Image


class Display:

    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
    
    def size(self):
        return (self.width, self.height)

    def show_image(self, image: Image.Image):
        pass

    def clear(self):
        pass

    def clean(self):
        pass

class DebugDisplay(Display):

    def __init__(self, width = 264, height = 176) -> None:
        super().__init__(width, height)

    def show_image(self, image: Image.Image):
        image.show(f"Debug Display, {self.width}x{self.height}")