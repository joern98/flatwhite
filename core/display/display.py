from typing import Tuple
from PIL import Image


class Display:

    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

    def show_image(self, image: Image.Image):
        pass

    def clear(self):
        pass

    def clean(self):
        pass