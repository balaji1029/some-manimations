from manim import *

class SecondPassScene(Scene):
    def construct(self):
        # make a lattice of 9 APs in a 3x3 grid
        self.time_scale = 2.0

        run_time = 0.5

        ap_positions = [
            LEFT + UP, ORIGIN + UP, RIGHT + UP,
            LEFT + ORIGIN, ORIGIN + ORIGIN, RIGHT + ORIGIN,
            LEFT + DOWN, ORIGIN + DOWN, RIGHT + DOWN
        ]

        aps = [Dot(pos, color=BLUE) for pos in ap_positions]
        
        self.add(
            *aps
        )

        # add random STAs and a lot of STAs allocated to central AP in different squares but a bit further from APs
        sta_positions = [
            ORIGIN + [0.2, 0.4, 0],
            ORIGIN + [-0.3, 0.2, 0],
            ORIGIN + [0.3, -0.4, 0],
            LEFT + UP + [0.4, -0.4, 0],
            LEFT + DOWN + [0.4, 0.4, 0],
            RIGHT + UP + [-0.4, -0.4, 0],
            RIGHT + DOWN + [-0.4, 0.4, 0],
            LEFT + ORIGIN + [0.4, 0, 0],
        ]

        sta_lines = []

        for sta_pos in sta_positions:
            sta = Dot(sta_pos, color=GREEN)
            closest_ap = min(aps, key=lambda ap: np.linalg.norm(ap.get_center() - sta.get_center()))
            line = DashedLine(closest_ap.get_center(), sta.get_center(), dash_length=0.1, color=YELLOW)
            sta_lines.append((sta, line))
            self.add(sta)
            self.add(line)

        sta_line_1_new = DashedLine(aps[1].get_center(), sta_positions[1], dash_length=0.1, color=RED)

        self.play(FadeOut(sta_lines[1][1]), Write(sta_line_1_new), run_time=run_time)

        sta_line_2_new = DashedLine(aps[7].get_center(), sta_positions[2], dash_length=0.1, color=RED)

        self.play(FadeOut(sta_lines[2][1]), Write(sta_line_2_new), run_time=run_time)
