from manim import *

class ExposedNode(Scene):
    def construct(self):

        main_ap = Dot(ORIGIN + UP, color=BLUE)
        main_label = Text("Associated AP", font_size=24).next_to(main_ap, UP)

        sta = Dot(ORIGIN + LEFT, color=GREEN)
        sta_label = Text('STA', font_size=24).next_to(sta, DOWN)

        hidden_ap = Dot(ORIGIN + RIGHT, color=RED)
        hidden_label = Text('Exposed Node AP', font_size=24).next_to(hidden_ap, DOWN).shift(RIGHT * 0.5)

        self.add(main_ap, main_label, sta, sta_label, hidden_ap, hidden_label)

        ap_range = Circle(radius=1, color=BLUE, fill_opacity=0.1).move_to(main_ap.get_center())
        hidden_range = Circle(radius=1, color=RED, fill_opacity=0.1).move_to(hidden_ap.get_center())
        self.add(ap_range, hidden_range)
        self.play(ap_range.animate.scale(1.6).set_fill(opacity=0.2), hidden_range.animate.scale(1.6).set_fill(opacity=0.2), run_time=1)
        self.play(ap_range.animate.scale(10/16).set_fill(opacity=0.1), hidden_range.animate.scale(10/16).set_fill(opacity=0.1), run_time=1)