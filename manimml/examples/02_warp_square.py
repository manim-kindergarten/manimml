from manimlib import *
from manimml import ManimML


class WarpSquare(Scene):
    def construct(self):
        app = ManimML(scene=self, file='02_warp_square.xml', data={})
        square = app['square']
        self.play(square.animate.apply_complex_function(np.exp))
        self.wait()