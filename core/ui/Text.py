from .Component import Component

class Text(Component):

    def __init__(self, text) -> None:
        super().__init__()
        self.text = text

    def draw(self, canvas):
        canvas.text(self.position, self.text, fill=0)
        super().draw(canvas)