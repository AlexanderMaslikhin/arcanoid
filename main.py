from time import sleep
import curses
import curses.ascii
import locale
from game.arcanoid import GameField
from game.functions import line_track
from game.ball import Ball


w_str = ''


def main(stdscr):
    start_x = stdscr.getbegyx()[1]
    stop_x = stdscr.getmaxyx()[1]
    stdscr.leaveok(True)
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()

    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    stdscr.keypad(True)
#    stdscr.nodelay(True)
#     w_str = bytes(w_str)
    while start_x < stop_x:
        stdscr.addch(0, start_x, curses.ACS_BOARD, curses.color_pair(start_x+100))
        stdscr.refresh()
        start_x += 1
        sleep(0.5)
    # s = ''
    # i = 0
    # while True:
    #     key = stdscr.getch()
    #     if key == ord('q'):
    #         break
    #     elif key == curses.KEY_LEFT:
    #         s = 'Left key'
    #     elif key == curses.KEY_RIGHT:
    #         s = 'Right key'
    #     # else:
    #     #     continue
    #     stdscr.clear()
    #     stdscr.addstr(0, 0, s + ' ' + str(i))
    #     sleep(0.1)
    #     stdscr.refresh()
    #     i += 1


locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

# passing arguments:
# {
#     speed: 10 or 20 or 30 (steps per second)
#     pad_size: 10 or 15 or 20 (length of pad in symbols)
#     wall_thickness: form 1 to 5 (count of layers in the wall)
# }


def test(window):
    window.leaveok(True)
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    window.scrollok(False)
    window.keypad(True)

    curses.start_color()
    curses.use_default_colors()
    field = GameField(window, speed=10, pad_size=15, wall_thickness=3)
    field.create_field()
    window.getch()
    window.nodelay(True)
    field.run_game()


#curses.wrapper(test)
w = curses.initscr()
#w.add
test(w)
# curses.start_color()
#print(w.getmaxyx(), w.getyx())
#w.getkey()
# b = Ball(10, 3)
# while True:
#     sym = w.getkey()
#     print(f'start at {b.x}, {b.y}')
#     b.step()
#     b.draw(w)
#     if sym == 'q':
#         break
curses.endwin()
# b = int.from_bytes("Б".encode(code), 'big')
# s = b.to_bytes(2, 'big').decode(code)
# print(b, s)



