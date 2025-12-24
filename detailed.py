from manim import *
import numpy as np
import math
import random

class DetailedFastLoop(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        self.camera.background_color = "#111111"
        
        # --- SCENE 1: NORMAL OPERATION ---
        self.next_section("Normal Operation")
        
        # Title
        title = Text("Fast-Loop Interference Avoidance", font_size=36).to_edge(UP)
        self.play(Write(title))

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

        self.play(
            LaggedStart(
                *[Create(r) for r in ranges],
                *[FadeIn(a) for a in aps],
                *[Write(l) for l in labels],
                lag_ratio=0.2
            )
        )
        self.play(FadeIn(stas), Create(connections))
        self.wait(1)

        # --- SCENE 2: RADAR EVENT ---
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
        
        self.play(FadeIn(radar_dot))
        
        # Animate ripples
        self.play(
            LaggedStart(
                *[
                    Transform(
                        p, 
                        Circle(radius=6, color=RED, stroke_opacity=0).move_to(radar_origin),
                        rate_func=linear, run_time=1.5
                    ) for p in pulses
                ],
                lag_ratio=0.3
            ),
            Flash(victim_ap, color=RED, flash_radius=1),
            victim_lbl.animate.set_color(RED)
        )
        
        # Alert Overlay
        alert_box = Rectangle(width=10, height=3, color=RED, fill_color=BLACK, fill_opacity=0.8)
        self.play(FadeIn(alert_box), Write(radar_text), Write(radar_sub))
        self.wait(1.5)
        
        # Clean up for Analysis View
        self.play(
            FadeOut(alert_box), FadeOut(radar_text), FadeOut(radar_sub),
            FadeOut(radar_dot), FadeOut(pulses),
            FadeOut(stas), FadeOut(connections),
            ranges.animate.set_opacity(0.05), # Dim the map
            aps.animate.set_opacity(0.2),
            labels.animate.set_opacity(0.2)
        )

        # --- SCENE 3: PROBABILITY & SCORING ---
        self.next_section("Scoring Logic")

        # Step Label
        step_lbl = Text("Step 2: Fallback Channel Scoring", font_size=32, color=YELLOW).to_edge(UP)
        self.play(Transform(title, step_lbl))

        # 1. Histogram (DFS Probability)
        mu, sigma = 52.0, 1.5
        axes = Axes(
            x_range=[46, 58, 2], y_range=[0, 0.5, 0.1],
            x_length=6, y_length=3,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 20}
        ).shift(LEFT * 3)
        
        x_lbl = axes.get_x_axis_label("Channel", edge=DOWN, direction=DOWN).scale(0.6)
        y_lbl = axes.get_y_axis_label("P(Radar)", edge=LEFT, direction=LEFT).scale(0.6)
        
        # Generate Gaussian Curve
        def pdf(x):
            return 1.0 / (sigma * math.sqrt(2 * math.pi)) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)
        
        curve = axes.plot(pdf, color=BLUE_C)
        area = axes.get_area(curve, x_range=[46, 58], color=BLUE, opacity=0.3)
        
        hist_group = VGroup(axes, x_lbl, y_lbl, curve, area)
        
        self.play(Create(axes), Write(x_lbl), Write(y_lbl))
        self.play(Create(curve), FadeIn(area))
        
        explanation = Text("Historic Radar Probability", font_size=24, color=BLUE_C).next_to(axes, UP)
        self.play(Write(explanation))
        self.wait(1)

        # 2. The Formula
        formula = MathTex(
            r"S(c) = w_1 S_{intf} + w_2 S_{airtime} + w_3 S_{BW} + w_4 S_{DFS}",
            font_size=34
        ).shift(RIGHT * 3.5 + UP * 1)
        
        self.play(Write(formula))

        # 3. Dynamic Weights Table (Showing adaptability)
        table_data_high = [
            ["Metric", "Weight"],
            ["Interference", "0.25"],
            ["Airtime", "0.25"],
            ["Bandwidth", "0.45"], # Prioritize BW in high load
            ["DFS Risk", "0.15"]
        ]
        
        t_high = Table(
            table_data_high, 
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": GRAY},
            element_to_mobject=lambda t: Text(t, font_size=20)
        ).scale(0.6).next_to(formula, DOWN, buff=0.5)

        load_lbl = Text("Context: High Traffic Load", font_size=24, color=RED).next_to(t_high, UP)
        
        self.play(Create(t_high), Write(load_lbl))
        self.wait(1)
        
        # Highlight Bandwidth weight
        hl_rect = SurroundingRectangle(t_high.get_rows()[3], color=YELLOW)
        self.play(Create(hl_rect))
        self.wait(0.5)
        self.play(FadeOut(hl_rect))

        # --- SCENE 4: SELECTION TABLE ---
        self.next_section("Selection")
        
        # Clear analysis view
        self.play(
            FadeOut(hist_group), FadeOut(explanation),
            FadeOut(formula), FadeOut(t_high), FadeOut(load_lbl)
        )
        
        step_select = Text("Step 3: Best Candidate Selection", font_size=32, color=GREEN).to_edge(UP)
        self.play(Transform(title, step_select))

        # Final Scores Table
        # Note: Assuming Higher Score = Better Candidate based on your example table where Ch 60 was 0.40
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
        
        self.play(Create(final_table))
        self.wait(1)

        # Highlight Current (Bad)
        bad_row = final_table.get_rows()[2]
        bad_rect = SurroundingRectangle(bad_row, color=RED)
        bad_lbl = Text("Current (Radar)", font_size=20, color=RED).next_to(bad_rect, LEFT)
        
        self.play(Create(bad_rect), Write(bad_lbl))
        self.wait(0.5)

        # Highlight Winner (Good)
        good_row = final_table.get_rows()[4]
        good_rect = SurroundingRectangle(good_row, color=GREEN)
        good_lbl = Text("Best Fallback", font_size=20, color=GREEN).next_to(good_rect, LEFT)
        
        self.play(ReplacementTransform(bad_rect, good_rect), ReplacementTransform(bad_lbl, good_lbl))
        self.wait(1.5)

        # --- SCENE 5: EXECUTION ---
        self.next_section("Switching")
        
        self.play(FadeOut(final_table), FadeOut(good_rect), FadeOut(good_lbl), FadeOut(title))

        # Bring map back to life
        self.play(
            ranges.animate.set_opacity(0.1),
            aps.animate.set_opacity(1),
            labels.animate.set_opacity(1)
        )
        
        # Change Channel Label
        # Victim AP is index 2, label index 2
        old_label = labels[2]
        new_label = MathTex("CH = 60", font_size=32, color=GREEN).next_to(aps[2], DOWN)
        
        # Color change to indicate switch
        switch_indicator = Circle(radius=0.5, color=GREEN).move_to(aps[2])
        
        self.play(
            Transform(old_label, new_label),
            Transform(aps[2][1], Dot(ap_config[2]["pos"], color=GREEN, radius=0.15)), # Change AP dot color
            Broadcast(switch_indicator, focal_point=aps[2].get_center())
        )
        
        # Reconnect Clients
        self.play(FadeIn(stas))
        
        # Animate connection lines redrawing
        new_connections = VGroup()
        for sta in stas:
            line = DashedLine(sta.get_center(), ap_config[2]["pos"], color=GREEN, stroke_opacity=0.8)
            new_connections.add(line)
            
        self.play(Create(new_connections))
        
        success_text = Text("Switch Complete: Latency < 200ms", font_size=24, color=GREEN).next_to(aps[2], UP)
        self.play(Write(success_text))
        
        self.wait(2)