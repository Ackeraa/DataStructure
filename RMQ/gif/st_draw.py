import turtle
from math import pow, log
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
    def __init__(self, grids):
        self.grid_size = 600 / grids
        self.left = -305
        self.top = 305


    def draw_rect(self, row, col, rows, cols):
        t.penup()
        t.setheading(0)
        t.goto(self.left + col * self.grid_size, self.top - row * self.grid_size) 
        t.pendown()
        for i in range(2):
            t.fd(self.grid_size * cols)
            t.rt(90)
            t.fd(self.grid_size * rows)
            t.rt(90)

    def paint_rect(self, row, col, rows, cols, color):
        t.fillcolor(color)
        t.penup()
        t.setheading(0)
        t.goto(self.left + col * self.grid_size, self.top - row * self.grid_size) 
        t.pendown()
        t.begin_fill()
        for i in range(2):
            t.fd(self.grid_size * cols)
            t.rt(90)
            t.fd(self.grid_size * rows)
            t.rt(90)
        t.end_fill()
    
    def draw_text(self, row, col, text):
        t.penup()
        t.goto(self.left + col * self.grid_size + self.grid_size / 2.5,
               self.top - row * self.grid_size - self.grid_size / 1.2) 
        t.pendown()
        t.write(text, font=("Times", 24))
        t.penup()

def draw():
    rect = Rect(13)

    n = 10
    a = [2, 9, 7, 6, 5, 1, 8, 3, 4, 6]
    f = [[0 for _ in range(n)] for _ in range(n)]
    
    left = 4
    top = 1
    turtle.tracer(False)
    for i in range(n):
        k = int(log(n - i) / log(2))
        for j in range(k + 1):
            rect.draw_rect(top + i, left + j, 1, 1)

    k = int(log(n) / log(2)) 
    for i in range(n):
        rect.draw_text(top + i, left - 1, str(i))
    for i in range(k + 1):
        rect.draw_text(top - 1, left + i, str(i))
    turtle.tracer(True)

    t.speed(8)
    for i in range(n):
        f[i][0] = a[i] 
        t.speed(6)
        rect.paint_rect(top + i, left, 1, 1, "grey")
        rect.draw_text(top + i, left, str(a[i]))
        turtle.tracer(False)
        t.pencolor("white")
        rect.paint_rect(top + 11, 4, 1, 12, "white")
        t.pencolor("black")
        text = f"f[{i}][0] = a[{i}]" 
        rect.draw_text(top + 11, 4, text)
        turtle.tracer(True)
        rect.paint_rect(top + i, left, 1, 1, "blue")
        rect.draw_text(top + i, left, str(a[i]))
    for l in range(1, k + 1):
        for i in range(n):
            if i + int(pow(2, l)) - 1 >= n:
                break
            f[i][l] = min(f[i][l - 1], f[i + int(pow(2, l - 1))][l - 1])
            
            rect.paint_rect(top + i, left + l, 1, 1, "grey")
            turtle.tracer(False)
            t.pencolor("white")
            rect.paint_rect(top + 11, 4, 1, 12, "white")
            t.pencolor("black")
            text = f"f[{i}][{l}] = min(f[{i}][{l-1}], f[{i + int(pow(2, l-1))}][{l-1}])" 
            rect.draw_text(top + 11, 4, text)
            rect.paint_rect(top + i, left + l - 1, 1, 1, "grey")
            rect.draw_text(top + i, left + l - 1, str(f[i][l - 1]))
            rect.paint_rect(top + i + int(pow(2, l - 1)), left + l - 1, 1, 1, "grey")
            rect.draw_text(top + i + int(pow(2, l - 1)), left + l - 1,
                           str(f[i + int(pow(2, l - 1))][l - 1]))
            turtle.tracer(True)

            t.speed(5)
            rect.paint_rect(top + i, left + l, 1, 1, "blue")
            rect.draw_text(top + i, left + l, str(f[i][l]))

            turtle.tracer(False)
            rect.paint_rect(top + i, left + l - 1, 1, 1, "blue")
            rect.draw_text(top + i, left + l - 1, str(f[i][l - 1]))

            rect.paint_rect(top + i + int(pow(2, l - 1)), left + l - 1, 1, 1, "blue")
            rect.draw_text(top + i + int(pow(2, l - 1)), left + l - 1,
                           str(f[i + int(pow(2, l - 1))][l - 1]))
            turtle.tracer(True)

turtle2gif.convert(draw, 5, 7)
