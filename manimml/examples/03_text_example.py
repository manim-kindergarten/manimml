from manimlib import *
from manimml import ManimML


class TextExample(Scene):
    def construct(self):
        app = ManimML(scene=self, file='03_text_example.xml', data={})
        text, difference, fonts, slant = app['text', 'difference', 'fonts', 'slant']

        self.play(Write(text))
        self.play(FadeIn(difference, UP))
        self.wait(3)
        self.play(FadeOut(text), FadeOut(difference, shift=DOWN))
        self.play(Write(fonts))
        self.wait()
        self.play(Write(slant))
        self.wait()
