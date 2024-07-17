import logging
import os
from typing import List

from PIL import Image, ImageDraw, ImageFont

from .output import Output
from .config import RESOURCE_PATH

class GUI_Model:

    def __init__(self) -> None:
        self.title = "..."
        self.artist = "..."
        self.current_timecode_seconds = 0
        self.track_length_seconds = 0

class GUIElement:
    """Base class for GUIElements"""

    def __init__(self, x0, y0, x1, y1) -> None:
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def draw(self, canvas: ImageDraw.ImageDraw):
        """Draw the GUIElement on the given canvas"""
        pass

    def bounds(self):
        return (self.x0, self.y0, self.x1, self.y1)

class Rectangle(GUIElement):
    def __init__(self, x0, y0, x1, y1, fill=None, border_color=0x00, border_width=1) -> None:
        super().__init__(x0, y0, x1, y1)
        self.fill = fill
        self.border_color = border_color
        self.border_width = border_width

    def draw(self, canvas: ImageDraw.ImageDraw):
        canvas.rectangle((self.x0, self.y0, self.x1, self.y1), fill=self.fill, outline=self.border_color, width=self.border_width)
        logging.debug(f"Draw rectangle on canvas with bounds {(self.x0, self.y0, self.x1, self.y1)}")

class Textbox(GUIElement):

    __fonts = [ImageFont.truetype(os.path.join(RESOURCE_PATH, "coolvetica", "coolvetica rg.otf"), 24), 
               ImageFont.truetype(os.path.join(RESOURCE_PATH, "coolvetica", "coolvetica rg.otf"), 16)]
    LARGE = 0
    SMALL = 1

    def __init__(self, x0, y0, x1, y1, text, font=LARGE) -> None:
        super().__init__(x0, y0, x1, y1)
        self.text = text
        self.font_index = font

    def draw(self, canvas: ImageDraw.ImageDraw):
        adjusted_text = self.__get_adjusted_text(canvas)
        canvas.multiline_text(self.bounds()[:2], adjusted_text, fill=0, font=self.__fonts[self.font_index])
        logging.debug(f"Draw textbox on canvas with bounds {(self.x0, self.y0, self.x1, self.y1)} and text '{self.text}' adjusted to {repr(adjusted_text)}")


    def __get_max_line_length(self, text, canvas: ImageDraw.ImageDraw):
        i = 0
        while canvas.textbbox(self.bounds()[:2], text[:i])[2] <= self.x1 and i < len(text):
            i += 1
        return i
    
    def __find_previous_space_index(self, text, start):
        for i in range(start, 0, -1):
            if text[i] == ' ':
                return i
            
    def __get_adjusted_text(self, canvas: ImageDraw.ImageDraw):
        a, b = "", self.text
        max_line_length = self.__get_max_line_length(self.text, canvas)
        while canvas.multiline_textbbox(self.bounds()[:2], b)[2] > self.x1:
            new_line_pos = self.__find_previous_space_index(b, max_line_length)
            a += b[:new_line_pos]
            a += '\n' 
            b = b[new_line_pos+1:]
        a += b
        return a

class GUI:

    def builder():
        return GUI_Builder()
    
    # provide interface to other classes to change GUI and initiate re-rendering of GUI 
    def __init__(self, width, height, elements = None, output = None) -> None:
        self.__renderer = GUI_Renderer(width, height)
        self.__elements: List[GUIElement] | None = elements
        self.output: Output | None = output

    def update(self):
        self.__renderer.render(self.__elements)
        try:
            self.output.show_image(self.__renderer.get_image())
        except Exception as e:
            self.output.clean()
            raise e

class GUI_Renderer:
    # render the actual GUI into a PIL.Image of size WIDTH x HEIGHT
    # handle low lever rendering and provide functions like draw_rectangle() or draw_text()
    def __init__(self, width, height) -> None:
        self.__image = None
        self.width = width
        self.height = height


    def get_image(self):
        return self.__image
    
    def render(self, elements: List[GUIElement]):
        image = Image.new('1', (self.width, self.height), 0xFF)
        draw = ImageDraw.Draw(image)
        for e in elements:
            e.draw(draw)
        self.__image = image


class GUI_Builder:

    def __init__(self) -> None:
        self.__elements: List[GUIElement] = []
        self.__output: Output | None = None
        self.width = None
        self.height = None
    
    def build(self):
        gui = GUI(self.width, self.height, self.__elements, self.__output)
        return gui

    def set_output(self, output):
        self.__output = output
        return self
    
    def set_size(self, width, height):
        self.width = width
        self.height = height
        return self

    def add_element(self, element):
        self.__elements.append(element)
        return self
    






