import rabit

r = rabit.Rabit(11, 600)

a = [4, 5, 1, 3, 2]
b = [3, 4, 1, 5, 2]
c = [2, 5, 1, 4, 3]
r.begin_hide()
for i in range(5):
    r.draw_rect(3, i + 3)
    r.draw_text(3, i + 3, str(a[i]))

for i in range(5):
    r.draw_rect(5, i + 3)
    r.draw_text(5, i + 3, str(b[i]))

for i in range(5):
    r.draw_rect(7, i + 3)
    r.draw_text(7, i + 3, str(c[i]))
r.end_hide()
r.save2eps("3.eps")
