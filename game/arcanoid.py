import _curses
import curses
from random import randint
from time import sleep
from .drawing import Ball
from .drawing import Wall
from .drawing import Pad
from .functions import blocks_colors, correct_y

# passing arguments:
# {
#     speed: 10 or 20 or 30 (steps per second)
#     pad_size: 10 or 15 or 20 (length of pad in symbols)
#     wall_thickness: form 1 to 5 (count of layers in the wall)
# }


class GameField:
    def __init__(self, window, **kwargs):
        self.prepare = False
        self.window = window
        self.start_msg = "Для старта игры нажмите любую кнопку кроме стрелок вправо/влево."
        self.step_time = 1/kwargs['speed']
        self.pad_size = kwargs['pad_size']
        self.field_height, self.field_width = self.window.getmaxyx()
        self.ball = Ball(self.field_width // 2, 3)
        for pair, fg_color in blocks_colors.items():
            curses.init_pair(pair, fg_color, -1)
        self.wall = Wall(kwargs['wall_thickness'], self.field_width, self.field_height - 3 - kwargs['wall_thickness'])
        self.score = 0
        self.pad = Pad((self.field_width - self.pad_size) // 2, 2, self.pad_size, self.field_width)
        self.lives = 3

    def create_field(self):
        self.prepare = True
        self.pad.set_position((self.field_width - self.pad_size) // 2)
        self.ball.set_position(self.pad.x + self.pad_size // 2, 3)
        self.redraw()
        while True:
            key = self.window.getch()
            if key in (curses.KEY_LEFT, curses.KEY_RIGHT):
                self.pad.update_pad(key)
            else:
                break
            self.ball.set_position(self.pad.x + self.pad_size // 2, 3)
            self.redraw()
        self.prepare = False

    def redraw(self):
        self.window.clear()
        # draw all objects
        self.ball.draw(self.window)
        self.wall.draw(self.window)
        self.pad.draw(self.window)
        if self.prepare:
            self.window.addstr(self.field_height // 2,
                               (self.field_width - len(self.start_msg)) // 2,
                               self.start_msg.upper())
        score_str = f'Score: {self.score}'
        self.window.addstr(self.field_height-1, self.field_width - len(score_str) - 1, score_str)
        self.window.addstr(self.field_height-1, 0, 'TRIES:[' + '*' * self.lives + ' ' * (3 - self.lives) + ']')
        self.window.refresh()
        sleep(self.step_time)

    def run_game(self):
        while self.lives:
            self.create_field()
            self.window.nodelay(True)
            while not self.wall.is_empty() and self.ball.y > 1:
                key = self.window.getch()
                curses.flushinp()
                if key == ord('q'):
                    return self.score
                if key in (curses.KEY_RIGHT, curses.KEY_LEFT):
                    self.pad.update_pad(key)
                self.ball.step()
                on_track = self.wall.is_hit_me(self.ball.get_xy(), self.ball.get_ort())
                self.score = self.score + 100 * bin(on_track).count('1')
                # checking borders of window and pad collision
                if self.ball.x == 0 or self.ball.x == self.field_width - 1:
                    on_track = on_track | 4
                if self.ball.y == self.field_height or self.pad.on_me(self.ball.x, self.ball.y):
                    on_track = on_track | 2
                if on_track:
                    self.ball.update_track(on_track)
                self.redraw()
            if self.wall.is_empty():
                return self.score
            self.window.nodelay(False)
            self.lives -= 1
        return self.score
        pass

