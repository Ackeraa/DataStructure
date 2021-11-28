import rabit

def draw():
    text = ['5', '4', '1', '3', '-', '10', '9', '6', '8']
    choice = [0, 1, 2, 2, 1, 2, 2, 2, 2, 3]
    r.begin_hide()
    for i in range(4):
        r.draw_rect(5, i + 1)
        r.draw_text(5, i + 1, text[i])
    for i in range(4):
        r.draw_rect(5, i + 6)
        r.draw_text(5, i + 6, text[i + 5])
    r.end_hide()

    k = 0
    r.speed(0)
    for i in range(4):
        for j in range(4 - i):
            r.begin_hide()
            r.draw_rect(5, i + 1, 1, j + 1, color="red")
            r.draw_rect(5, i + 6, 1, j + 1, color="red")
            r.end_hide()

            r.begin_hide()
            r.paint_rect(5, choice[k] + 1, 1, 1, color="red")
            r.paint_rect(5, choice[k] + 6, 1, 1, color="red")
            r.clear_rect(7, 4, 1, 5)
            r.draw_text(7, 5, f"RMQ_B({i}, {j}) = {choice[k]}")
            r.end_hide()


            r.begin_hide()
            r.draw_rect(5, i + 1, 1, j + 1)
            r.draw_rect(5, i + 6, 1, j + 1)
            r.paint_rect(5, choice[k] + 1, 1, 1, color="white")
            r.paint_rect(5, choice[k] + 6, 1, 1, color="white")
            r.end_hide()
            
            k += 1

if __name__ == '__main__':
    r = rabit.Rabit(11, 600)
#    r.hold()
    rabit.convert2gif(draw, 60, 10)

