from manim import *
import math

class TriangulationAnimation(Scene):
    def construct(self):
        # make background white
        self.camera.background_color = BLACK

        # Points (known A, B) and unknown C
        A = Dot([-3, -3, 0], color=BLUE)
        B = Dot([4, -3, 0], color=BLUE)
        C = Dot([0, 3, 0], color=BLUE)
        # make D show up at the top of every other line in the scene
        D = Dot([0, -1, 0], color=RED)

        # label_A = Text("", font_size=32, color=BLUE).next_to(A, DOWN)
        label_A = MathTex("AP_1", font_size=32, color=BLUE).next_to(A, DOWN)
        label_B = MathTex("AP_2", font_size=32, color=BLUE).next_to(B, DOWN)
        label_C = MathTex("AP_3", font_size=32, color=BLUE).next_to(C, UP)
        label_D = MathTex("STA", font_size=32, color=RED).next_to(D, DOWN)

        # self.play(Create(A), Create(B), Create(C))
        # self.play(Write(label_A), Write(label_B), Write(label_C))
        self.add(A, B, C, )
        self.wait(0.5)

        AD_line = Line(A.get_center(), D.get_center(), color=GREEN)
        BD_line = Line(B.get_center(), D.get_center(), color=GREEN)
        CD_line = Line(C.get_center(), D.get_center(), color=GREEN)
        AD_text = MathTex(r"d_{AP_1 \leftrightarrow STA}", font_size=36, color=GREEN).next_to(AD_line, LEFT)
        BD_text = MathTex(r"d_{AP_2 \leftrightarrow STA}", font_size=36, color=GREEN).next_to(BD_line, RIGHT)
        CD_text = MathTex(r"d_{AP_3 \leftrightarrow STA}", font_size=36, color=GREEN).next_to(CD_line, LEFT)    

        self.play(Create(AD_line), Create(BD_line), Create(CD_line), Write(AD_text), Write(BD_text), Write(CD_text))

        # Reveal target point C
        self.play(FadeIn(D), Write(label_D))
        self.wait()

        # make D disappear
        self.play(FadeOut(D), FadeOut(label_D), FadeOut(AD_line), FadeOut(BD_line), FadeOut(CD_line),
                  FadeOut(AD_text), FadeOut(BD_text), FadeOut(CD_text))
        self.wait()

        rA = A.get_center() - D.get_center()
        rB = B.get_center() - D.get_center()
        rC = C.get_center() - D.get_center()

        arc_A = Arc(radius=math.sqrt(rA[0]**2 + rA[1]**2), start_angle=0, angle=PI, color=YELLOW).shift(A.get_center())
        arc_B = Arc(radius=math.sqrt(rB[0]**2 + rB[1]**2), start_angle=PI/3, angle=2*PI/3, color=YELLOW).shift(B.get_center())
        arc_C = Arc(radius=math.sqrt(rC[0]**2 + rC[1]**2), start_angle=PI, angle=PI, color=YELLOW).shift(C.get_center())
        self.play(Create(arc_A), Create(arc_B), Create(arc_C))

        self.wait(0.5)
        label_D = MathTex("STA", font_size=32, color=RED).shift([0.9, -0.5, 0])

        # make D appear again
        self.play(FadeIn(D), Write(label_D), FadeIn(AD_line), FadeIn(BD_line), FadeIn(CD_line),
                  FadeIn(AD_text), FadeIn(BD_text), FadeIn(CD_text))
        self.wait(2)

