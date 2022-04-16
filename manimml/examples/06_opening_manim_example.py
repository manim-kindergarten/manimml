from manimlib import *
from manimml import ManimML


class OpeningManimExample(Scene):
    def construct(self):
        matrix = [[1, 1], [0, 1]]
        app = ManimML(file='06_opening_manim_example.xml', data={
            'matrix': matrix
        })

        intro_words = app['intro_words']
        self.play(Write(intro_words))
        self.wait(2)

        # Linear transform
        grid, linear_transform_words = app['grid', 'linear_transform_words']
        self.play(
            ShowCreation(grid),
            FadeTransform(intro_words, linear_transform_words)
        )
        self.wait()
        self.play(grid.animate.apply_matrix(matrix), run_time=3)
        self.wait()

        # Complex map
        c_grid, moving_c_grid, complex_map_words = app['c_grid', 'moving_c_grid', 'complex_map_words']
        moving_c_grid.prepare_for_nonlinear_transform()
        self.play(
            FadeOut(grid),
            Write(c_grid, run_time=3),
            FadeIn(moving_c_grid),
            FadeTransform(linear_transform_words, complex_map_words),
        )
        self.wait()
        self.play(
            moving_c_grid.animate.apply_complex_function(lambda z: z**2),
            run_time=6,
        )
        self.wait(2)
