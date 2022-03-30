from manimlib import *
from manimml import ManimML


class TextExample(Scene):
    def construct(self):
        app = ManimML(scene=self, file='03_text_example.xml', data={})
        text = app['text']
        difference = app['difference']
        fonts = app['fonts']
        slant = app['slant']

        VGroup(text, difference).arrange(DOWN, buff=1)
        VGroup(fonts, slant).arrange(DOWN, buff=0.8)

        self.play(Write(text))
        self.play(FadeIn(difference, UP))
        self.wait(3)
        self.play(FadeOut(text), FadeOut(difference, shift=DOWN))
        self.play(Write(fonts))
        self.wait()
        self.play(Write(slant))
        self.wait()
