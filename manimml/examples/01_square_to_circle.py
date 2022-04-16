from manimlib import *
from manimml import ManimML


class SquareToCircle(Scene):
    def construct(self):
        app = ManimML(file='01_square_to_circle.xml', data={})
        square = app['square']
        circle = app['circle']
        self.play(ShowCreation(square))
        self.wait()
        self.play(ReplacementTransform(square, circle))
        self.wait()
