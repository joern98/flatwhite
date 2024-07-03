from PIL import ImageDraw

class Component:

    def __init__(self, draw_border=False) -> None:
        self.position = (0, 0)
        self.size = (0, 0)
        self.padding = (0, 0, 0, 0)  # left, top, right, bottom
        self.draw_border = draw_border

    def bounds(self):
        x0 = self.position[0]
        y0 = self.position[1]
        x1 = x0 + self.size[0] - 1
        y1 = y0 + self.size[1] - 1
        return x0, y0, x1, y1
    
    def padded_bounds(self):
        x0, y0, x1, y1 = self.bounds()
        x0 += self.padding[0]
        y0 += self.padding[1]
        x1 -= self.padding[2]
        y1 -= self.padding[3]
        return x0, y0, x1, y1
    
    def padded_size(self):
        x = self.size[0] - self.padding[0] - self.padding[2]
        y = self.size[1] - self.padding[1] - self.padding[3]
        return x, y
    
    def draw(self, canvas: ImageDraw.ImageDraw):
        if self.draw_border:
            canvas.rectangle(self.bounds(), fill=None, outline=0)


class Text(Component):

    def __init__(self, text, draw_border=False) -> None:
        super().__init__(draw_border)
        self.text: str = text

    def __get_max_line_length(self, canvas: ImageDraw.ImageDraw):
        i = 0
        while canvas.textbbox(self.padded_bounds()[:2], self.text[:i])[2] <= self.padded_bounds()[2]:
            i += 1
        return i
    
    def __find_previous_space_index(self, start):
        for i in range(start, 0, -1):
            if self.text[i] == ' ':
                return i
            
    def __adjust_line_breaks(self, canvas):
        text_bounds = canvas.multiline_textbbox(self.position, self.text)
        if text_bounds[2] > self.padded_bounds()[2]:
            new_line_pos = self.__find_previous_space_index(self.__get_max_line_length(canvas))
            a = self.text[:new_line_pos]
            b = self.text[new_line_pos+1:]
            self.text = a + '\n' + b


    def draw(self, canvas):
        self.__adjust_line_breaks(canvas)
        canvas.multiline_text(self.padded_bounds()[:2], self.text, fill=0)
        super().draw(canvas)


class ProgressBar(Component):

    def __init__(self, draw_border=False) -> None:
        super().__init__(draw_border)
        self.progress = 0

    def set_progress(self, p):
        self.progress = p
    
    def draw(self, canvas):
        x0, y0, x1, y1 = self.padded_bounds()
        x1 = x0 + int((self.padded_size()[0]-1)*self.progress)
        canvas.rectangle((x0, y0, x1, y1), fill=0, outline=None)


