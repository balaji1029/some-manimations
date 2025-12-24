from manim import *
import numpy as np
import random
import matplotlib.pyplot as plt
import math

class FastLoop(Scene):
    def construct(self):
        # make three APs (Access Points) in the scene
        AP1 = Dot([-3, -3, 0], color=BLUE)
        AP2 = Dot([4, -3, 0], color=BLUE)
        AP3 = Dot([0, 3, 0], color=BLUE)

        # Design ranges of the APs
        range1 = Circle(radius=3, color=BLUE).move_to(AP1.get_center())
        range2 = Circle(radius=4, color=BLUE).move_to(AP2.get_center())
        range3 = Circle(radius=5, color=BLUE).move_to(AP3.get_center())

        channel_label1 = MathTex("CH = 100", font_size=32, color=BLUE).next_to(AP1, DOWN)
        channel_label2 = MathTex("CH = 96", font_size=32, color=BLUE).next_to(AP2, DOWN)
        channel_label3 = MathTex("CH = 52", font_size=32, color=BLUE).next_to(AP3, DOWN)

        # fill circles with transparent color
        range1.set_fill(BLUE, opacity=0.1)
        range2.set_fill(BLUE, opacity=0.1)
        range3.set_fill(BLUE, opacity=0.1)


        # self.play(Create(AP1), Create(AP2), Create(AP3))
        # self.play(Create(range1), Create(range2), Create(range3))
        # self.play(Create(channel_label1), Create(channel_label2), Create(channel_label3))
        self.add(AP1, AP2, AP3,
                 range1, range2, range3,
                 channel_label1, channel_label2, channel_label3)
        stas = []
        for _ in range(4):
            x = random.uniform(-6, 6)
            y = random.uniform(-4, 4)
            sta = Dot([x, y, 0], color=GREEN)
            stas.append(sta)
            self.add(sta)

        radar = Dot([1, 1, 0], color=RED)
        radar_label = MathTex("RADAR", font_size=32, color=RED).next_to(radar, DOWN)
        self.play(Create(radar), Write(radar_label))

        # make radar blink with oscillating radius animation
        for _ in range(2):
            pulse = Circle(radius=0.5, color=RED).move_to(radar.get_center())
            pulse.set_fill(RED, opacity=0.2)
            self.play(GrowFromCenter(pulse), run_time=0.5)
            self.play(pulse.animate.scale(3).set_opacity(0), run_time=1)
            self.remove(pulse)
        self.wait(1)

        # clear the stuff
        self.play(
            FadeOut(AP1), FadeOut(AP2), FadeOut(AP3), 
            FadeOut(range1), FadeOut(range2), FadeOut(range3),
            FadeOut(channel_label1), FadeOut(channel_label2), FadeOut(channel_label3),
            FadeOut(radar), FadeOut(radar_label),
            FadeOut(*stas)
        )

        text = Text("RADAR detected on Channel 52", font_size=48, color=RED)
        self.play(Write(text))
        self.wait(1)

        self.play(FadeOut(text))

        # make a random gaussian data with mode 1
        mu = 52.0
        sigma = 1.5
        N = 5000 # number of samples
        bins = 30 # histogram bins


        # Generate samples
        samples = np.random.normal(loc=mu, scale=sigma, size=N)


        # Compute histogram (density=True so heights approximate PDF)
        counts, edges = np.histogram(samples, bins=bins, density=True)
        bin_width = edges[1] - edges[0]
        bin_centers = (edges[:-1] + edges[1:]) / 2.0


        # Create axes
        x_min = float(edges[0]) - 0.5 * bin_width
        x_max = float(edges[-1]) + 0.5 * bin_width
        y_max = max(counts) * 1.2


        axes = Axes(
            x_range=[x_min, x_max, (x_max-x_min)/10],
            y_range=[0, y_max, y_max/5],
            x_length=10,
            y_length=5,
            tips=False
        ).to_edge(LEFT)

        x_label = axes.get_x_axis_label('Channel')
        y_label = axes.get_y_axis_label('Radar Probability')
        self.add(axes, x_label, y_label)


        # Draw histogram bars
        bars = VGroup()
        for (center, height) in zip(bin_centers, counts):
            # create a rectangle for each bin
            left = center - 0.5 * bin_width
            rect = Rectangle(
                width=axes.x_axis.unit_size * bin_width,
                height=axes.y_axis.unit_size * height,
                stroke_width=0,
                fill_opacity=0.8,
            )
            # position rect: axes.coords_to_point maps (x, y) to scene coords
            rect.move_to(axes.c2p(center, height / 2))
            rect.set_fill(BLUE)
            bars.add(rect)

        labels = []

        # add markers to the x-axis
        for x in range(46, 58, 2):
            # add numbers to x-axis
            tick = axes.get_x_axis().get_tick(x)
            label = MathTex(str(x), font_size=24).next_to(tick, DOWN)
            labels.append(label)
            self.add(label)

        self.play(LaggedStart(*[GrowFromCenter(b) for b in bars], lag_ratio=0.02), run_time=2)


        # Analytical Gaussian PDF for overlay
        def gaussian_pdf(x):
            return 1.0 / (sigma * math.sqrt(2 * math.pi)) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)


        graph = axes.plot(gaussian_pdf, x_range=[x_min, x_max])
        graph.set_stroke(width=3)

        self.play(Create(graph), run_time=2)

        # clear the stuff
        self.play(
            FadeOut(bars),
            *[FadeOut(label) for label in labels],
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label),
            FadeOut(graph)
        )

        # Updated with realistic channel data
        table = Table(
            [
                ['Channel', 'Interference', 'DFS Prob', 'Airtime', 'BW Score'],
                ['36', 'Low (0.15)', '0.05', '12\\%', '0.25'],
                ['50', 'Med (0.35)', '0.95', '45\\%', '1.0'],
                ['52', 'High (0.65)', '1.0', '38\\%', '0.25'],
                ['54', 'Med (0.40)', '0.88', '28\\%', '0.5'],
                ['56', 'Low (0.20)', '0.72', '15\\%', '0.25'],
                ['58', 'Low (0.18)', '0.45', '18\\%', '0.75'],
                ['106', 'Very Low (0.08)', '0.12', '8\\%', '0.75'],
                ['114', 'Very Low (0.10)', '0.08', '5\\%', '1.0']
            ],
            include_outer_lines=True,
            line_config={"stroke_width": 2},
            top_left_entry=Text("Channel Analysis", font_size=24)
        ).scale(0.45)
        self.play(Create(table))
        self.wait(0.5)

        self.play(FadeOut(table))

        # Scoring formula with actual weights
        formula = MathTex(
            r'S(c) = w_1 S_{intf}(c) + w_2 S_{airtime}(c) + w_3 S_{BW}(c) + w_4 S_{DFS}(c)', 
            font_size=36
        )

        self.play(Write(formula))
        self.wait(0.5)
        self.play(FadeOut(formula))
        
        # Add a line saying , w1 , w2 , w3 , w4 were taken to increase the QoE of the network for different senarioes.


        # Actual weight configurations from adaptive_weights_controller.py
        table2 = Table(
            [
                [r'\text{Weight}', r'\text{Value}'],
                ['w_1 (Intf)', '0.25'],
                ['w_2 (Airtime)', '0.25'],
                ['w_3 (BW)', '0.45'],
                ['w_4 (DFS)', '0.15']
            ],
            include_outer_lines=True,
            element_to_mobject=lambda el: MathTex(el, font_size=48)
        ).scale(0.55)

        table3 = Table(
            [
                [r'\text{Weight}', r'\text{Value}'],
                ['w_1 (Intf)', '0.35'],
                ['w_2 (Airtime)', '0.25'],
                ['w_3 (BW)', '0.15'],
                ['w_4 (DFS)', '0.25']
            ],
            include_outer_lines=True,
            element_to_mobject=lambda el: MathTex(el, font_size=48)
        ).scale(0.55)

        table4 = Table(
            [
                [r'\text{Weight}', r'\text{Value}'],
                ['w_1 (Intf)', '0.25'],
                ['w_2 (Airtime)', '0.25'],
                ['w_3 (BW)', '0.45'],
                ['w_4 (DFS)', '0.15']
            ],
            include_outer_lines=True,
            element_to_mobject=lambda el: MathTex(el, font_size=48)
        ).scale(0.55)

        table5 = Table(
            [
                [r'\text{Weight}', r'\text{Value}'],
                ['w_1 (Intf)', '0.45'],
                ['w_2 (Airtime)', '0.375'],
                ['w_3 (BW)', '0.15'],
                ['w_4 (DFS)', '0.125']
            ],
            include_outer_lines=True,
            element_to_mobject=lambda el: MathTex(el, font_size=48)
        ).scale(0.55)
        
        # show all these tables from table2 to table5 in one page in each quarter of the screen
        table2.to_corner(UL).shift(RIGHT * 0.5)
        table3.to_corner(UR).shift(LEFT * 0.5)
        table4.to_corner(DL).shift(RIGHT * 0.5)
        table5.to_corner(DR).shift(LEFT * 0.5)

        table2_text = Text("High Load", font_size=24).next_to(table2, RIGHT)
        table3_text = Text("Medium Load", font_size=24).next_to(table3, LEFT)
        table4_text = Text("Low Load", font_size=24).next_to(table4, RIGHT)
        table5_text = Text("No Load", font_size=24).next_to(table5, LEFT)

        self.play(
            FadeIn(table2), FadeIn(table3), FadeIn(table4), FadeIn(table5),
            Write(table2_text), Write(table3_text), Write(table4_text), Write(table5_text)
        )

        self.wait(0.5)

        self.play(
            FadeOut(table2), FadeOut(table3), FadeOut(table4), FadeOut(table5),
            FadeOut(table2_text), FadeOut(table3_text), FadeOut(table4_text), FadeOut(table5_text)
        )

        table_end = Table(
            [
                ['Channel', 'Interference', 'RADAR probability', 'Air time utilization','score'],
                ['46', 'Low', '0.7', '5','0.32'],
                ['48', 'Very High', '0.8', '5','0.12'],
                ['50', 'Very High', '1.0', '25','0.05'],
                ['52', 'High', '1,0', '10','0.22'],
                ['54', 'Medium', '1.0', '15','0.18'],
                ['56', 'Low','0.8', '5','0.25'],
                ['58', 'Low', '0.7', '5','0.30'],
                ['60', 'Very Low', '0.5', '5','0.40']
            ],
            include_outer_lines=True,
            line_config={"stroke_width": 2},
        ).scale(0.5)

        self.play(FadeIn(table_end))
        self.wait(0.5)
        self.play(FadeOut(table_end))

        # display the first image again

        self.play(
            Create(AP1), Create(AP2), Create(AP3),
            Create(range1), Create(range2), Create(range3),
            Create(channel_label1), Create(channel_label2), Create(channel_label3),
            *[Create(sta) for sta in stas]
        )

        self.play(Transform(channel_label3, MathTex("CH = 100", font_size=32, color=BLUE).next_to(AP3, DOWN)))