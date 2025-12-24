from manim import *

class FirstPassScene(Scene):
    def construct(self):
        # make the time scale faster
        self.time_scale = 2.0

        run_time = 0.5

        # Four APs in a square formation
        ap_positions = [
            LEFT + UP,
            RIGHT + UP,
            RIGHT + DOWN,
            LEFT + DOWN
        ]
        aps = [Dot(pos, color=BLUE) for pos in ap_positions]
        ap_label1 = Text("AP1", font_size=24).next_to(aps[0], UP)
        ap_label2 = Text("AP2", font_size=24).next_to(aps[1], UP)
        ap_label3 = Text("AP3", font_size=24).next_to(aps[2], DOWN)
        ap_label4 = Text("AP4", font_size=24).next_to(aps[3], DOWN)
        
        self.add(
            aps[0], aps[1], aps[2], aps[3],
            ap_label1, ap_label2, ap_label3, ap_label4
        )

        print(LEFT + UP)
        print(RIGHT + UP)
        print(LEFT + DOWN)
        print(RIGHT + DOWN)

        sta1 = Dot(ORIGIN + [0.5, 0.5, 0], color=GREEN)
        line1 = DashedLine(aps[0].get_center(), sta1.get_center(), dash_length=0.1, color=YELLOW)

        self.play(Create(sta1), run_time=run_time)
        self.play(Write(line1), run_time=run_time)

        sta2 = Dot(ORIGIN + [-0.4, -0.3, 0], color=GREEN)
        line2 = DashedLine(aps[1].get_center(), sta2.get_center(), dash_length=0.1, color=YELLOW)

        self.play(Create(sta2), run_time=run_time)
        self.play(Write(line2), run_time=run_time)

        sta3 = Dot(ORIGIN + [-0.3, 0.4, 0], color=GREEN)
        line3 = DashedLine(aps[2].get_center(), sta3.get_center(), dash_length=0.1, color=YELLOW)

        self.play(Create(sta3), run_time=run_time)
        self.play(Write(line3), run_time=run_time)
