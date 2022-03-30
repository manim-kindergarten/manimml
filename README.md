# Manim Markup Language

使用 xml 编写 manim.

整容前 (来自 [3b1b](https://github.com/3b1b/manim)):
```py
from manimlib import *


class TextExample(Scene):
    def construct(self):
        # To run this scene properly, you should have "Consolas" font in your computer
        # for full usage, you can see https://github.com/3b1b/manim/pull/680
        text = Text("Here is a text", font="Consolas", font_size=90)
        difference = Text(
            """
            The most important difference between Text and TexText is that\n
            you can change the font more easily, but can't use the LaTeX grammar
            """,
            font="Arial", font_size=24,
            # t2c is a dict that you can choose color for different text
            t2c={"Text": BLUE, "TexText": BLUE, "LaTeX": ORANGE}
        )
        VGroup(text, difference).arrange(DOWN, buff=1)
        self.play(Write(text))
        self.play(FadeIn(difference, UP))
        self.wait(3)

        fonts = Text(
            "And you can also set the font according to different words",
            font="Arial",
            t2f={"font": "Consolas", "words": "Consolas"},
            t2c={"font": BLUE, "words": GREEN}
        )
        fonts.set_width(FRAME_WIDTH - 1)
        slant = Text(
            "And the same as slant and weight",
            font="Consolas",
            t2s={"slant": ITALIC},
            t2w={"weight": BOLD},
            t2c={"slant": ORANGE, "weight": RED}
        )
        VGroup(fonts, slant).arrange(DOWN, buff=0.8)
        self.play(FadeOut(text), FadeOut(difference, shift=DOWN))
        self.play(Write(fonts))
        self.wait()
        self.play(Write(slant))
        self.wait()
```

整容后:
```xml
<manim>
  <VGroup call.arrange="DOWN, buff=1">
    <Text id="text" args="'Here is a text'" font="'Consolas'" font_size="90" />
    <Text id="difference"
      font="'Arial'"
      font_size="24"
      t2c="{'Text':BLUE, 'TexText':BLUE, 'LaTeX':ORANGE}"
    >
      The most important difference between Text and TexText is that\n
      you can change the font more easily, but can't use the LaTeX grammar
    </Text>
  </VGroup>
  <VGroup call.arrange="DOWN, buff=.8">
    <Text id="fonts"
      font="'Arial'"
      t2f="{'font': 'Consolas', 'words': 'Consolas'}"
      t2c="{'font': BLUE, 'words': GREEN}"
      call.set_width="FRAME_WIDTH - 1"
    >
      And you can also set the font according to different words
    </Text>
    <Text id="slant"
      font="'Consolas'"
      t2s="{'slant': ITALIC}"
      t2w="{'weight': BOLD}"
      t2c="{'slant': ORANGE, 'weight': RED}"
    >
      And the same as slant and weight
    </Text>
  </VGroup>
</manim>
```

```py
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
```
