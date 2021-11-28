import turtle
from math import sqrt
from turtle2gif import turtle2gif

turtle.title("BLOCK")
turtle.hideturtle()
s = turtle.getscreen()
t = turtle.Turtle()
t.hideturtle()
t.shape("circle")
t.shapesize(1, 1, 1)
t.pensize(3)

class Rect():
    def __init__(self, rows, cols, grid_size):
        self.rows = rows
        self.cols = cols
        self.grid_size = grid_size
        self.width = cols * grid_size
        self.height = rows * grid_size
        self.left = -self.width / 2
        self.top = self.height / 2

    def draw_text(self, text, row, col):
        t.penup()
        t.goto(self.left + col * self.grid_size + self.grid_size / 2.7,
               self.top - row * self.grid_size - self.grid_size / 1.2)
        t.pendown()
        t.write(text, font=("Times", 24))

    def draw_line(self, col):
        t.setheading(-90)
        t.penup()
        t.goto(self.left + col * self.grid_size, self.top + self.grid_size)
        t.pendown()
        t.forward(4 * self.grid_size)

    def draw_rect(self):
        turtle.tracer(False)
        t.setheading(0)
        for i in range(self.rows + 1):
            t.penup()
            t.goto(self.left, self.top - i * self.grid_size)
            t.pendown()
            t.forward(self.width)

        t.right(90)
        for i in range(self.cols + 1):
            t.penup()
            t.goto(self.left + i * self.grid_size, self.top)
            t.pendown()
            t.forward(self.height)
        turtle.tracer(True)

    def paint_rect(self, row, col, color):
        t.fillcolor(color)
        t.setheading(0)
        t.penup()
        t.goto(self.left + col * self.grid_size,
               self.top - row * self.grid_size)
        t.pendown()
        t.begin_fill()
        t.fd(self.grid_size)
        t.right(90)
        t.fd(self.grid_size)
        t.right(90)
        t.fd(self.grid_size)
        t.right(90)
        t.fd(self.grid_size)
        t.end_fill()

def draw():

    INF = 10000
    n = 14
    a = [3, 5, 4, 1, 2, 9, 7, 6, 5, 8, 2, 4, 7, 4]
    len_b = int(sqrt(n))
    cnt_b = (n - 1) // len_b + 1
    f = [INF for _ in range(cnt_b)] 

    rect = Rect(2, 14, 45)
    rect.draw_rect()
    turtle.tracer(False)
    for i in range(14):
        rect.draw_text(str(i), -1, i)
        rect.draw_text(str(a[i]), 1, i)
        if i and i % len_b == 0:
            rect.draw_line(i)
    turtle.tracer(True)

    t.speed(8)
    for i in range(cnt_b):
        for j in range(i * len_b, i * len_b + len_b):
            if j >= n:
                break
            rect.paint_rect(1, j, "grey")
            rect.draw_text(str(a[j]), 1, j)
            rect.paint_rect(1, j, "white")
            rect.draw_text(str(a[j]), 1, j)
            if f[i] > a[j]:
                f[i] = a[j]
                k = i * len_b + len_b // 2
                rect.paint_rect(0, k, "white")
                rect.draw_text(str(a[j]), 0, k)
            else:
                pass

    rect.draw_text('ans:', 4, 5)
    turtle.tracer(False)
    for i in range(1, 14):
        rect.paint_rect(1, i, "grey")
        rect.draw_text(str(a[i]), 1, i)
    turtle.tracer(True)

    t.speed(5)
    ans = INF
    i = 1
    j = 13
    ith = i // len_b
    jth = j // len_b
    for k in range(i, ith * len_b + len_b):
        if k > j:
            break
        rect.paint_rect(1, k, "blue")
        rect.draw_text(str(a[k]), 1, k)
        ans = min(ans, a[k])
        t.pencolor("white")
        rect.paint_rect(4, 7, "white")
        t.pencolor("black")
        rect.draw_text(str(ans), 4, 7)
    for k in range(max(i, jth * len_b), j + 1):
        rect.paint_rect(1, k, "blue")
        rect.draw_text(str(a[k]), 1, k)
        ans = min(ans, a[k])
        t.pencolor("white")
        rect.paint_rect(4, 7, "white")
        t.pencolor("black")
        rect.draw_text(str(ans), 4, 7)

    for k in range(ith + 1, jth):
        pos = k * len_b + len_b // 2
        rect.paint_rect(0, pos, "blue")
        rect.draw_text(str(f[k]), 0, pos)
        ans = min(ans, f[k])
        t.pencolor("white")
        rect.paint_rect(4, 7, "white")
        t.pencolor("black")
        rect.draw_text(str(ans), 4, 7)

turtle2gif.convert(draw, 10, 10)
