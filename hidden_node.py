from manim import *

class HiddenNode(Scene):
    def construct(self):
        # Make background black
        self.camera.background_color = BLACK

        # Main AP
        main_ap = Dot(ORIGIN + LEFT, color=BLUE)
        main_label = Text("Associated AP", font_size=24).next_to(main_ap, DOWN).shift(LEFT * 0.5)

        # STA connected to main AP
        sta = Dot(ORIGIN + UP, color=GREEN)
        sta_label = Text("STA", font_size=24).next_to(sta, UP)

        # Hidden Node AP (not connected)
        hidden_ap = Dot(ORIGIN + RIGHT, color=RED)
        hidden_label = Text("Hidden Node AP", font_size=24).next_to(hidden_ap, DOWN).shift(RIGHT * 0.5)

        # Add all elements to the scene
        self.add(main_ap, main_label, sta, sta_label, hidden_ap, hidden_label)

        # show the main AP's range pulsing but not too big
        ap_range = Circle(radius=1, color=BLUE, fill_opacity=0.1).move_to(main_ap.get_center())
        hidden_range = Circle(radius=1, color=RED, fill_opacity=0.1).move_to(hidden_ap.get_center())
        # self.add(Create(ap_range), Create(hidden_range))
        self.add(ap_range, hidden_range)
        self.play(ap_range.animate.scale(1.6).set_fill(opacity=0.2), hidden_range.animate.scale(1.6).set_fill(opacity=0.2), run_time=1)
        self.play(ap_range.animate.scale(10/16).set_fill(opacity=0.1), hidden_range.animate.scale(10/16).set_fill(opacity=0.1), run_time=1)

