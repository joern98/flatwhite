from PIL import ImageDraw

class Component:

    def __init__(self) -> None:
        self.position = (0, 0)
        self.size = (0, 0)

    def draw(self, canvas: ImageDraw.ImageDraw):
        coords = [self.position, (self.position[0] + self.size[0]-1, self.position[1] + self.size[1]-1)]
        canvas.rectangle(coords, fill=None, outline=0, width=1)