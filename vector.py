from pdb import run
from manim import *
import numpy as np
import math
import random

class DetailedFastLoop_Reordered(Scene):
    def construct(self):

        run_time = 0.5
        # --- CONFIGURATION ---
        self.camera.background_color = "#111111"
        
        # ==========================================
        # SCENE 1: NORMAL OPERATION
        # ==========================================
        self.next_section("Normal Operation")
        
        # Title
        title = Text("Fast-Loop Interference Avoidance", font_size=36).to_edge(UP)
        self.add(title)

        # Create APs
        ap_config = [
            {"pos": [-4, -2, 0], "ch": 100, "color": TEAL},
            {"pos": [4, -2, 0], "ch": 96, "color": TEAL},
            {"pos": [0, 2, 0], "ch": 52, "color": BLUE}, # The Victim AP
        ]
        
        aps = VGroup()
        ranges = VGroup()
        labels = VGroup()
        
        for conf in ap_config:
            ap = Dot(conf["pos"], color=conf["color"], radius=0.15)
            # Add an "Antenna" feel
            antenna = Line(conf["pos"], [conf["pos"][0], conf["pos"][1]+0.3, 0], color=GRAY)
            ap_group = VGroup(antenna, ap)
            
            # Wifi Range
            wifi_range = Circle(radius=3.5, color=conf["color"], fill_opacity=0.1).move_to(conf["pos"])
            
            # Label
            lbl = MathTex(f"CH = {conf['ch']}", font_size=28, color=conf["color"]).next_to(ap, DOWN)
            
            aps.add(ap_group)
            ranges.add(wifi_range)
            labels.add(lbl)

        # Clients (STAs)
        stas = VGroup()
        connections = VGroup()
        for _ in range(5):
            # Random position near the center AP (the one that will switch)
            offset = np.random.normal(0, 1.0, 2)
            pos = ap_config[2]["pos"] + np.append(offset, 0)
            sta = Square(side_length=0.15, color=GREEN, fill_opacity=1).move_to(pos)
            stas.add(sta)
            # Line to AP
            line = DashedLine(sta.get_center(), ap_config[2]["pos"], color=GREEN, stroke_opacity=0.5)
            connections.add(line)

        self.add(
            ranges, aps, labels
        )
        self.add(stas, connections)
        self.wait(2)

        # ==========================================
        # SCENE 2: RADAR EVENT
        # ==========================================
        self.next_section("Radar Detection")
        
        # The Victim AP (Index 2 in our groups)
        victim_ap = aps[2]
        victim_lbl = labels[2]
        
        radar_origin = [1, 2.5, 0]
        radar_dot = Dot(radar_origin, color=RED)
        radar_text = Text("RADAR PULSE DETECTED", font_size=42, color=RED, weight=BOLD).move_to([0,0,0])
        radar_sub = Text("Microsecond burst on Channel 52", font_size=24, color=RED_A).next_to(radar_text, DOWN)
        
        # Pulse animation
        pulses = VGroup()
        for i in range(3):
            p = Circle(radius=0.1, color=RED, stroke_width=4).move_to(radar_origin)
            pulses.add(p)
        
        self.add(radar_dot)
        
        # Animate ripples
        self.play(
            LaggedStart(
                *[
                    Transform(
                        p, 
                        Circle(radius=6, color=RED, stroke_opacity=0).move_to(radar_origin),
                        rate_func=linear, run_time=run_time
                    ) for p in pulses
                ],
                lag_ratio=0.3
            ),
            Flash(victim_ap, color=RED, flash_radius=1),
            victim_lbl.animate.set_color(RED)
        )
        
        # Alert Overlay
        alert_box = Rectangle(width=10, height=3, color=RED, fill_color=BLACK, fill_opacity=0.8)
        self.add(alert_box, radar_text, radar_sub)
        self.wait(1.5)
        
        # Clean up everything to prepare for Step 1
        self.play(
            FadeOut(radar_dot),
            FadeOut(pulses),
            FadeOut(alert_box),
            FadeOut(radar_text),
            FadeOut(radar_sub),
            victim_lbl.animate.set_color(victim_ap[1].get_color()), # Reset label color
            *[FadeOut(r) for r in ranges],
            *[FadeOut(a) for a in aps],
            *[FadeOut(l) for l in labels],
            *[FadeOut(s) for s in stas],
            *[FadeOut(c) for c in connections],
            FadeOut(title),
            run_time=run_time
        )

        # ==========================================
        # SCENE 3: THE FORMULA (STEP 1)
        # ==========================================
        self.next_section("Step 1: The Formula")

        slide_title_1 = Text("Step 1: The Scoring Formula", font_size=32, color=YELLOW).to_edge(UP)
        self.play(Write(slide_title_1), run_time=run_time)

        # The math equation
        formula = MathTex(
            r"S(c) = w_1 S_{intf} + w_2 S_{airtime} + w_3 S_{BW} + w_4 S_{DFS}",
            font_size=42
        )
        
        self.play(Write(formula))
        self.wait(1)
        
        # Highlight the DFS term briefly to transition to next step
        frame_dfs = SurroundingRectangle(formula[0][-5:], color=BLUE, buff=0.1)
        dfs_label = Text("How do we get this?", font_size=20, color=BLUE).next_to(frame_dfs, DOWN)

        self.play(Create(frame_dfs), Write(dfs_label), run_time=run_time)
        self.wait(1.5)

        # Clear Scene
        self.play(FadeOut(formula), FadeOut(slide_title_1), FadeOut(frame_dfs), FadeOut(dfs_label), run_time=run_time)

        # ==========================================
        # SCENE 4: PROBABILITY GRAPH (STEP 2)
        # ==========================================
        self.next_section("Step 2: DFS Probability")

        # Slide Title
        slide_title_2 = Text("Step 2: Historical DFS Probability", font_size=32, color=BLUE).to_edge(UP)
        self.play(Write(slide_title_2), run_time=run_time)

        # Histogram (DFS Probability)
        mu, sigma = 52.0, 1.5
        axes = Axes(
            x_range=[46, 58, 2], y_range=[0, 0.5, 0.1],
            x_length=8, y_length=4,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 24}
        ).move_to(ORIGIN)
        
        x_lbl = axes.get_x_axis_label("Channel", edge=DOWN, direction=DOWN).scale(0.8)
        y_lbl = axes.get_y_axis_label("P(Radar)", edge=LEFT, direction=LEFT).scale(0.8)
        
        # Generate Gaussian Curve
        def pdf(x):
            return 1.0 / (sigma * math.sqrt(2 * math.pi)) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)
        
        curve = axes.plot(pdf, color=BLUE_C)
        area = axes.get_area(curve, x_range=[46, 58], color=BLUE, opacity=0.3)
        
        hist_group = VGroup(axes, x_lbl, y_lbl, curve, area)

        self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=run_time)
        self.play(Create(curve), FadeIn(area), run_time=run_time)
        
        explanation = Text("Gaussian Distribution of Radar Events", font_size=24, color=BLUE_C).next_to(axes, UP)
        self.play(Write(explanation), run_time=run_time)
        self.wait(1)

        # Clear Scene
        self.play(FadeOut(hist_group), FadeOut(explanation), FadeOut(slide_title_2), run_time=run_time)

        # ==========================================
        # SCENE 5: ADAPTIVE WEIGHTS
        # ==========================================
        # self.next_section("Adaptive Weights")

        # slide_title_3 = Text("Adaptive Weights Configuration", font_size=32, color=WHITE).to_edge(UP)
        # self.play(Write(slide_title_3))

        # # --- Table Construction ---
        # # 1. High Load
        # table2 = Table(
        #     [
        #         [r'\text{Weight}', r'\text{Value}'],
        #         ['w_1 (Intf)', '0.25'],
        #         ['w_2 (Airtime)', '0.25'],
        #         ['w_3 (BW)', '0.45'],
        #         ['w_4 (DFS)', '0.15']
        #     ],
        #     include_outer_lines=True,
        #     element_to_mobject=lambda el: MathTex(el, font_size=36)
        # ).scale(0.50)

        # # 2. Medium Load
        # table3 = Table(
        #     [
        #         [r'\text{Weight}', r'\text{Value}'],
        #         ['w_1 (Intf)', '0.35'],
        #         ['w_2 (Airtime)', '0.25'],
        #         ['w_3 (BW)', '0.15'],
        #         ['w_4 (DFS)', '0.25']
        #     ],
        #     include_outer_lines=True,
        #     element_to_mobject=lambda el: MathTex(el, font_size=36)
        # ).scale(0.50)

        # # 3. Low Load
        # table4 = Table(
        #     [
        #         [r'\text{Weight}', r'\text{Value}'],
        #         ['w_1 (Intf)', '0.25'],
        #         ['w_2 (Airtime)', '0.25'],
        #         ['w_3 (BW)', '0.45'],
        #         ['w_4 (DFS)', '0.15']
        #     ],
        #     include_outer_lines=True,
        #     element_to_mobject=lambda el: MathTex(el, font_size=36)
        # ).scale(0.50)

        # # 4. No Load
        # table5 = Table(
        #     [
        #         [r'\text{Weight}', r'\text{Value}'],
        #         ['w_1 (Intf)', '0.45'],
        #         ['w_2 (Airtime)', '0.375'],
        #         ['w_3 (BW)', '0.15'],
        #         ['w_4 (DFS)', '0.125']
        #     ],
        #     include_outer_lines=True,
        #     element_to_mobject=lambda el: MathTex(el, font_size=36)
        # ).scale(0.50)

        # # Positioning
        # table2.to_corner(UL, buff=1.0).shift(RIGHT * 0.5)
        # table3.to_corner(UR, buff=1.0).shift(LEFT * 0.5)
        # table4.to_corner(DL, buff=1.0).shift(RIGHT * 0.5)
        # table5.to_corner(DR, buff=1.0).shift(LEFT * 0.5)

        # # Labels
        # table2_text = Text("High Load", font_size=24, color=RED).next_to(table2, RIGHT)
        # table3_text = Text("Medium Load", font_size=24, color=ORANGE).next_to(table3, LEFT)
        # table4_text = Text("Low Load", font_size=24, color=YELLOW).next_to(table4, RIGHT)
        # table5_text = Text("High Interference", font_size=24, color=GREEN).next_to(table5, LEFT)

        # self.play(
        #     FadeIn(table2), FadeIn(table3), FadeIn(table4), FadeIn(table5),
        #     Write(table2_text), Write(table3_text), Write(table4_text), Write(table5_text)
        # )
        # self.wait(3)

        # # Clear Scene
        # self.play(
        #     FadeOut(table2), FadeOut(table3), FadeOut(table4), FadeOut(table5),
        #     FadeOut(table2_text), FadeOut(table3_text), FadeOut(table4_text), FadeOut(table5_text),
        #     FadeOut(slide_title_3)
        # )

        # ==========================================
        # SCENE 6: SELECTION TABLE (STEP 3 Part A)
        # ==========================================
        self.next_section("Step 3: Ranking")
        
        step_select = Text("Step 3: Ranking & Switching", font_size=32, color=GREEN).to_edge(UP)
        self.play(Write(step_select), run_time=run_time)

        # Final Scores Table
        final_data = [
            ["CH", "Intf", "DFS P", "Airtime", "Score"],
            ["48", "High", "0.8", "5%", "0.12"],
            ["52", "High", "1.0", "10%", "0.22"], # Current
            ["56", "Low", "0.8", "5%", "0.25"],
            ["60", "V. Low", "0.5", "5%", "0.40"], # Winner
            ["100", "Low", "0.0", "15%", "0.38"],
        ]

        final_table = Table(
            final_data,
            include_outer_lines=True,
            h_buff=0.8, v_buff=0.4,
            line_config={"stroke_width": 1},
            element_to_mobject=lambda t: Text(t, font_size=20)
        )
        
        self.play(Create(final_table), run_time=run_time)
        self.wait(0.5)

        # Highlight Current (Bad)
        bad_row = final_table.get_rows()[2]
        bad_rect = SurroundingRectangle(bad_row, color=RED)
        bad_lbl = Text("Current (Radar)", font_size=20, color=RED).next_to(bad_rect, LEFT)
        
        self.play(Create(bad_rect), Write(bad_lbl), run_time=run_time)
        self.wait(0.5)

        # Highlight Winner (Good)
        good_row = final_table.get_rows()[4]
        good_rect = SurroundingRectangle(good_row, color=GREEN)
        good_lbl = Text("Best Fallback", font_size=20, color=GREEN).next_to(good_rect, LEFT)

        self.play(ReplacementTransform(bad_rect, good_rect), ReplacementTransform(bad_lbl, good_lbl), run_time=run_time)
        self.wait(1.5)

        # ==========================================
        # SCENE 7: EXECUTION (STEP 3 Part B)
        # ==========================================
        self.next_section("Switching")

        self.play(FadeOut(final_table), FadeOut(good_rect), FadeOut(good_lbl), FadeOut(step_select), run_time=run_time)

        # Bring map back to life
        self.play(
            LaggedStart(
                *[FadeIn(r) for r in ranges],
                *[FadeIn(a) for a in aps],
                *[FadeIn(l) for l in labels],
                lag_ratio=0.1
            ), run_time=run_time
        )
        # Ranges should be dim
        self.play(ranges.animate.set_opacity(0.1), run_time=run_time)

        # Change Channel Label
        # Victim AP is index 2, label index 2
        old_label = labels[2]
        new_label = MathTex("CH = 60", font_size=32, color=GREEN).next_to(aps[2], DOWN)
        
        # Color change to indicate switch
        switch_indicator = Circle(radius=0.5, color=GREEN).move_to(aps[2])
        
        self.play(
            Transform(old_label, new_label),
            Transform(aps[2][1], Dot(ap_config[2]["pos"], color=GREEN, radius=0.15)), # Change AP dot color
            Broadcast(switch_indicator, focal_point=aps[2].get_center()), run_time=run_time
        )
        
        # Reconnect Clients
        self.play(FadeIn(stas))
        
        # Animate connection lines redrawing
        new_connections = VGroup()
        for sta in stas:
            line = DashedLine(sta.get_center(), ap_config[2]["pos"], color=GREEN, stroke_opacity=0.8)
            new_connections.add(line)

        self.play(Create(new_connections), run_time=run_time)

        success_text = Text("Switch Complete: Latency < 200ms", font_size=24, color=GREEN).next_to(aps[2], UP).shift(UP)
        self.play(Write(success_text), run_time=run_time)

        self.wait(1)