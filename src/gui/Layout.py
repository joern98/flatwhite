from typing import *
from .Component import Component#
import math

class Layout(Component):

    def __init__(self) -> None:
        super().__init__()
        self.children: List[Component] = []
        self.ratios = []

    def draw(self, canvas):
        for c in self.children:
            c.draw(canvas)
        super().draw(canvas)

    def append_child(self, c: Component, r):
        self.ratios.append(r)
        self.children.append(c)


class VerticalLayout(Layout):

    def draw(self, canvas):
        sum_ratios = sum(self.ratios)
        pos_y = self.position[1]
        for i in range(len(self.children)):
            c = self.children[i]
            p = (self.position[0], pos_y)
            s = (self.size[0], math.floor(self.size[1] * (self.ratios[i]/sum_ratios))) 
            c.position = p
            c.size = s
            pos_y += s[1]
            c.draw(canvas)
        super().draw(canvas)

class HorizontalLayout(Layout):

    def draw(self, canvas):
        sum_ratios = sum(self.ratios)
        pos_x = self.position[0]
        for i in range(len(self.children)):
            c = self.children[i]
            p = (pos_x, self.position[1])
            s = (math.floor(self.size[0] * (self.ratios[i]/sum_ratios)), self.size[1]) 
            c.position = p
            c.size = s
            pos_x += s[0]
            c.draw(canvas)
        super().draw(canvas)

