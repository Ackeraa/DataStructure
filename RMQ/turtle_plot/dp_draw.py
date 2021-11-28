import turtle
from turtle2gif import turtle2gif

turtle.title("DP")
turtle.hideturtle()
s = turtle.getscreen()
t = turtle.Turtle()
t.hideturtle()
t.shape("circle")
t.shapesize(1, 1, 1)

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
        t.goto(self.left + col * self.grid_size + self.grid_size / 2.2,
               self.top - row * self.grid_size - self.grid_size / 1.5)
        t.pendown()
        t.write(text, font=("Times", 24))

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
    rect = Rect(5, 5, 80)
    rect.draw_rect()
    turtle.tracer(False)
    for i in range(5):
        rect.draw_text(str(i), -1, i)
        rect.draw_text(str(i), i, -1)
    turtle.tracer(True)

    INF = 10000

    a = [3, 2, 4, 1, 5]
    f = [[ INF for _ in range(5)] for _ in range(5)]

    t.speed(8)
    for i in range(5):
        f[i][i] = a[i]
        rect.paint_rect(i, i, "grey")
        rect.draw_text(str(f[i][i]), i, i)
        rect.paint_rect(i, i, "blue")
        rect.draw_text(str(f[i][i]), i, i)

    for l in range(1, 5):
        for i in range(0, 5 - l):
            j = i + l
            f[i][j] = min(f[i][j - 1], f[i + 1][j])

            rect.paint_rect(i, j, "grey")
            rect.paint_rect(i, j - 1, "grey")
            turtle.tracer(False)
            rect.draw_text(str(f[i][j - 1]), i, j - 1)
            rect.paint_rect(i + 1, j, "grey")
            rect.draw_text(str(f[i + 1][j]), i + 1, j)
            turtle.update()
            turtle.tracer(True)
            rect.paint_rect(i, j, "blue")
            rect.draw_text(str(f[i][j]), i, j)
            turtle.delay(10)
            turtle.tracer(False)
            rect.paint_rect(i, j - 1, "blue")
            rect.draw_text(str(f[i][j - 1]), i, j - 1)
            rect.paint_rect(i + 1, j, "blue")
            rect.draw_text(str(f[i + 1][j]), i + 1, j)
            turtle.tracer(True)
            turtle.delay(10)

turtle2gif.convert(draw)
