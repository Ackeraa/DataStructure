import rabit

r = rabit.Rabit(11, 600)

a = [6, 9, 8, 10]
b = [10, 20, 15, 30]
r.begin_hide()
for i in range(4):
    r.draw_rect(5, i + 1)
    r.draw_text(5, i + 1, str(a[i]))

for i in range(4):
    r.draw_rect(5, i + 6)
    r.draw_text(5, i + 6, str(b[i]))
r.end_hide()
r.save2eps("1.eps")
