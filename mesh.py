# make a mesh using manim which shows a square lattice in 3d apace and a central hub at an elevation
from manim import *
from matplotlib.dviread import Box
import numpy as np
class Mesh3D(ThreeDScene):
    def construct(self):
        # make background white
        self.camera.background_color = BLACK
        # make camera perspective


        # Create a grid of points in 3D space
        points = []
        grid_size = 2
        spacing = 2.5
        for x in range(-grid_size, grid_size + 1):
            for y in range(-grid_size, grid_size + 1):
                z = 0  # Flat grid on the z=0 plane
                point = Dot3D(point=np.array([x * spacing, -y * 0.4, y * spacing]), color=rgb_to_color(rgb=(0.2, 0.6, 0.8)))
                point_label = MathTex(r'AP_{(%d,%d)}' % (x, y), font_size=16, color=WHITE).next_to(point, RIGHT)
                if (x, y) == (2, 2):
                    point_label = MathTex(r'AP_{(%d,%d)}' % (x, y), font_size=16, color=WHITE).next_to(point, LEFT)

                points.append(point)
                self.add(point, point_label)

        # Create a central hub, which is a cuboid elevated above the grid
        # hub = Cube(side_length=1, fill_color=RED, fill_opacity=1).shift([0, 2, 0])
        hub = Prism(dimensions=[1.5, 0.7, 3], fill_color=RED, fill_opacity=1)
        hub.shift([0, 2, 0])
        hub_label = MathTex("Central Hub", font_size=32, color=RED).next_to(hub, UP)
        # make green STAs randomly placed on the grid
        stas = [[3.0885200672996866, 3.0148746693326345],
        [-0.20791942114752082, -0.9782689804266784],
        [0.1983778830331877, 2.5114684827744638],
        [2.9423436224423973, -1.3373555064977145],
        [-1.5714941907021864, -3.5072085134511997],
        [-2.8691697156398455, 2.4371741344091795],
        [3.207636248513033, -0.2805272093543931],
        # [3.062173323406009, 3.2865216781199544],
        [-1.7815548324983064, 2.827702505041385],
        [1.9840035118790702, 3.3898106761232247]]
        for sta in stas:
            x = sta[0]
            y = sta[1]
            sta = Dot3D(point=np.array([x, -2, y]), color=GREEN)
            print(x, y)
            sta_label = MathTex("STA", font_size=24, color=GREEN).next_to(sta, DOWN)
            self.add(sta, sta_label)
        self.add(hub, hub_label)

        # Connect each point in the grid to the hub with lines
        # for point in points:
        #     line = Line3D(start=point.get_center(), end=hub.get_center(), color=GREEN)
        #     self.add(line)

        self.wait(2)