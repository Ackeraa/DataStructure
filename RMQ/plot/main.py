from manim import *
from global_func import *

class Fig1(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        array1 = get_array(4)
        array2 = get_array(4)
        self.add(VGroup(array1, array2).arrange(RIGHT, buff=2))
        i1 = [0, 1, 2, 3]
        v1 = [5, 2, 3, 1]
        v2 = [10, 7, 8, 6]
        index1 = put_values_up_array(array1, i1)
        index2 = put_values_up_array(array2, i1)
        values1 = put_values_in_array(array1, v1)
        values2 = put_values_in_array(array2, v2)

        self.add(index1)
        self.add(index2)
        self.add(values1)
        self.add(values2)

        for i in range(4):
            for j in  range(i, 4):
                label = self.get_text(i, j, "?")
                label.arrange(RIGHT)
                label.shift(DOWN * 2)
                self.add(label)

                self.play(Create(self.plot_rect(j - i + 1, array1[i].get_center(), RED)),
                          Create(self.plot_rect(j - i + 1, array2[i].get_center(), RED)))
                self.wait()

                mini = v2.index(min(v2[i:j+1]))
                array1[mini].set_fill(RED_B, 0.5)
                array2[mini].set_fill(RED_B, 0.5)
                self.remove(label)
                label = self.get_text(i, j, mini)
                label.arrange(RIGHT)
                label.shift(DOWN * 2)
                self.add(label)
                self.wait()

                self.add(self.plot_rect(j - i + 1, array1[i].get_center(), BLACK),
                         self.plot_rect(j - i + 1, array2[i].get_center(), BLACK))
                array1[mini].set_fill(WHITE)
                array2[mini].set_fill(WHITE)
                self.remove(label)

        self.wait()

    def plot_rect(self, width, pos, color):
        rect = Rectangle(width=width, height=1)
        rect.move_to([pos[0] + (width - 1) / 2, pos[1], pos[2]])
        rect.set_stroke(color)
        return rect

    def get_text(self, i, j, num):
        tex = Tex(r'$RMQ_B$', f'({i}, {j})={num}', color=BLACK)
        return VGroup(tex)

class Fig2(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # get array
        a = []
        for i in range(8):
            a.append(get_array(3, 0.6))
        vg0 = VGroup()
        vg1 = VGroup()
        vg2 = VGroup()
        vg1.add(*[a[i] for i in range(4)])
        vg1.arrange(RIGHT, buff=2)
        vg2.add(*[a[i + 4] for i in range(4)])
        vg2.arrange(RIGHT, buff=2)
        vg0.add(vg1, vg2).arrange(DOWN, buff=4)
        self.add(vg0)

        # put values in array
        vv = [[31, 41, 59],
            [16, 18, 3] ,
            [27, 18, 28],
            [66, 73, 84],
            [12, 2, 5],
            [66, 26, 6],
            [60, 22, 14],
            [72, 99, 27]]
        v = []
        for i in range(len(a)):
            v.append(put_values_in_array(a[i], vv[i]))
            self.add(v[i])
            f_always(v[i].move_to, a[i].get_center)

        vvb = [[1, 2, 3],
             [2, 3, 1],
             [2, 1, 3],
             [1, 2, 3],
             [3, 1, 2],
             [3, 2, 1],
             [3, 2, 1],
             [2, 3, 1]]
        vb = []
        for i in range(len(a)):
            vb.append(put_values_down_array(a[i], vvb[i]))
            self.play(ReplacementTransform(v[i].copy(), vb[i]))
            always(vb[i].next_to, a[i], DOWN)

        self.wait(0.3)
        color = [RED_E, BLUE_E, GREEN_E, RED_E, MAROON_E, PURPLE_E, PURPLE_E, BLUE_E]
        for i in range(len(a)):
            c = color[i]
            for x in a[i]:
                x.set_fill(c, opacity=0.5)

        self.wait(0.3)
        self.play(a[0].animate.move_to(LEFT * 6 + UP * 3))
        self.play(a[3].animate.next_to(a[0], RIGHT))

        self.play(a[1].animate.next_to(a[0], DOWN * 3))
        self.play(a[7].animate.next_to(a[1], RIGHT))

        self.play(a[5].animate.next_to(a[1], DOWN * 3))
        self.play(a[6].animate.next_to(a[5], RIGHT))

        self.play(a[2].animate.next_to(a[5], DOWN * 3))

        self.play(a[4].animate.next_to(a[2], DOWN * 3))

        self.wait()


class Fig3(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # get array
        a = []
        vg = VGroup()
        for i in range(3):
            a.append(get_array(5))
            vg.add(a[i])
        vg.arrange(DOWN, buff=1)
        vg.shift(LEFT * 2)
        self.add(vg)
        
        idx = [0, 1, 2, 3, 4]
        self.add(put_values_up_array(a[0], idx))

        vv = [[4, 5, 1, 3, 2], [3, 4, 1, 5, 2], [2, 5, 1, 4, 3]]
        v = []
        for i in range(3):
            v.append(put_values_in_array(a[i], vv[i]))
            self.add(v[i])

        for i in range(5):
            for j in  range(i, 5):
                label = self.get_text(i, j, "?")
                label.arrange(RIGHT)
                label.shift(RIGHT * 4)
                self.add(label)

                self.play(Create(self.plot_rect(j - i + 1, a[0][i].get_center(), RED)),
                          Create(self.plot_rect(j - i + 1, a[1][i].get_center(), RED)),
                          Create(self.plot_rect(j - i + 1, a[2][i].get_center(), RED)))
                self.wait(0.3)

                mini = vv[0].index(min(vv[0][i:j+1]))
                a[0][mini].set_fill(RED_B, 0.5)
                a[1][mini].set_fill(RED_B, 0.5)
                a[2][mini].set_fill(RED_B, 0.5)
                self.remove(label)
                label = self.get_text(i, j, mini)
                label.arrange(RIGHT)
                label.shift(RIGHT * 4)
                self.add(label)
                self.wait(0.4)

                self.add(self.plot_rect(j - i + 1, a[0][i].get_center(), BLACK),
                         self.plot_rect(j - i + 1, a[1][i].get_center(), BLACK),
                         self.plot_rect(j - i + 1, a[2][i].get_center(), BLACK))
                a[0][mini].set_fill(WHITE)
                a[1][mini].set_fill(WHITE)
                a[2][mini].set_fill(WHITE)
                self.remove(label)

        self.wait()

    def plot_rect(self, width, pos, color):
        rect = Rectangle(width=width, height=1)
        rect.move_to([pos[0] + (width - 1) / 2, pos[1], pos[2]])
        rect.set_stroke(color)
        return rect

    def get_text(self, i, j, num):
        tex = Tex(r'$RMQ_B$', f'({i}, {j})={num}', color=BLACK)
        return VGroup(tex)

class Fig4(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        node = Node("112")
        self.add(node)
        node.shift(RIGHT * 2)
        self.wait()
        self.play(node.trans_value("234"))
        #node.set_value("sd")
        self.wait()
        node.shift(RIGHT * 2)
        self.wait()
        node.set_value_color(RED_E)
        self.wait()
        node.set_color(RED_E)
        self.wait()
        node.set_fill(BLUE)
        self.wait()

class Fig5(Scene):
    def construct(self):
        text1 = Text("Hello")
        text2 = Text("World")
        self.add(text1)
        self.wait()
        self.play(Transform(text1, text2))
        text1.set_color(RED)
        self.wait()
