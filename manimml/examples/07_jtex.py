from manimlib import *
from manimgl_mathjax import JTex
from manimml import ManimML

class TestJtex(Scene):
    def construct(self):
        # pass globals so that manimml can find the definition of JTex
        ml = ManimML(file='07_jtex.xml', data=globals())
        self.add(*ml.objs)
