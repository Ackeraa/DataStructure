import rabit

r = rabit.Rabit(15, 600)

a = [[31, 41, 59],
    [16, 18, 3] ,
    [27, 18, 28],
    [66, 73, 84],
    [12, 2, 5],
    [66, 26, 6],
    [60, 22, 14],
    [72, 99, 27]]
b = [[1, 2, 3],
     [2, 3, 1],
     [2, 1, 3],
     [1, 2, 3],
     [3, 1, 2],
     [3, 2, 1],
     [3, 2, 1],
     [2, 3, 1]]
c = ["yellow",
     "green",
     "green",
     "yellow",
     "red",
     "grey",
     "grey",
     "blue"]

r.begin_hide()
gap = 0
for i in range(4):
    for j in range(3):
        r.draw_rect(5, i * 3 + j + gap)
        r.draw_text(5, i * 3 + j + gap, str(a[i][j]))
        r.paint_rect(5, i * 3 + j + gap, color = c[i])
        r.draw_text(6, i * 3 + j + gap, str(b[i][j]))
    gap += 1


gap = 0
for i in range(4):
    for j in range(3):
        r.draw_rect(8, i * 3 + j + gap)
        r.draw_text(8, i * 3 + j + gap, str(a[i + 4][j]))
        r.paint_rect(8, i * 3 + j + gap, color = c[i + 4])
        r.draw_text(9, i * 3 + j + gap, str(b[i + 4][j]))
    gap += 1

r.end_hide()
r.save2eps("2.eps")
