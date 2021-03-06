import curses


blocks_colors = {
    5: curses.COLOR_RED,
    4: curses.COLOR_YELLOW,
    3: curses.COLOR_GREEN,
    2: curses.COLOR_BLUE,
    1: curses.COLOR_WHITE
}


def line_track(k, bias, x):
    return int(round(k * x + bias))


def correct_y(y, win_height):
    return -y + win_height

