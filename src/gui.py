import logging

from PIL import Image, ImageDraw, ImageFont

BLACK = 0x00
WHITE = 0xFF

WIDTH = 264
HEIGHT = 176

class GUI:
    # provide interface to other classes to change GUI and initiate re-rendering of GUI 
    def __init__(self, output) -> None:
        self.__renderer = GUI_Renderer(WIDTH, HEIGHT)
        self.output = output
        self.__build()

    def update(self):
        self.__renderer.render()
        try:
            self.output.show_image(self.__renderer.get_image())
        except Exception as e:
            self.output.clean()
            raise e

    def __build(self):
        self.__renderer.rectangle(0, 0, WIDTH-1, HEIGHT-1)
        self.__renderer.rectangle(WIDTH//3, HEIGHT//3, 2*WIDTH//3, 2*HEIGHT//3)






class GUI_Renderer:
    # render the actual GUI into a PIL.Image of size WIDTH x HEIGHT
    # handle low lever rendering and provide functions like draw_rectangle() or draw_text()
    def __init__(self, width, height) -> None:
        self.__image = None
        self.width = width
        self.height = height
        self.__renderlist = []

    def get_image(self):
        return self.__image
    
    def render(self):
        image = Image.new('1', (self.width, self.height), WHITE)
        draw = ImageDraw.Draw(image)
        for f in self.__renderlist:
            f(draw)
        self.__image = image

    def rectangle(self, x0, y0, x1, y1, border_color=BLACK, fill=None, border_width=1):
        def f(draw: ImageDraw.ImageDraw):
            draw.rectangle((x0, y0, x1, y1), fill=fill, outline=border_color, width=border_width)
        self.__renderlist.append(f)
