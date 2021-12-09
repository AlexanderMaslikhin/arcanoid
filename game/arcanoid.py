import _curses
import curses
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
        self.logfile = open("logging.txt", 'w')
        self.window = window
        self.step_time = 1/kwargs['speed']
        self.pad_size = kwargs['pad_size']
        self.field_height, self.field_width = self.window.getmaxyx()
        self.ball = Ball(self.field_width // 2, 3)
        for pair, fg_color in blocks_colors.items():
            curses.init_pair(pair, fg_color, -1)
        self.wall = Wall(kwargs['wall_thickness'], self.field_width, self.field_height - 3 - kwargs['wall_thickness'])
        self.score = 0
        self.pad = Pad((self.field_width - self.pad_size) // 2, 2, self.pad_size)

    def create_field(self):
        self.redraw()
        pass

    # def is_anybody(self, cur_pos, ort):
    #     on_x = self.find_collision(cur_pos[0] + ort[0], cur_pos[1])
    #     on_y = self.find_collision(cur_pos[0], cur_pos[1] + ort[1])
    #     both = self.find_collision(cur_pos[0] + ort[0], cur_pos[1] + ort[1])
    #     return on_x, on_y, both
    #
    # def update_objects(self):
    #     # depending on ball_position
    #     # change blocks attributes and ball track
    #     self.ball.update_track(*self.is_anybody(self.ball.get_xy(), self.ball.get_ort()))
    #     pass
    #
    # def step(self):
    #     pass

    # def update_pad(self, key):
    #     pass

    def redraw(self):
        self.window.clear()
        # draw all objects
        self.ball.draw(self.window)
        self.wall.draw(self.window)
        self.pad.draw(self.window)
        self.window.addstr(0,0, f'ball_x = {self.ball.x}, ball_y = {correct_y(self.ball.y, self.field_height)} height = {self.field_height}, width = {self.field_width}')
        self.window.refresh()
        sleep(self.step_time)

    def run_game(self):
        while not self.wall.is_empty() and self.ball.y > 1:
            key = self.window.getch()
            if key == ord('q'):
                break
            if key in (curses.KEY_RIGHT, curses.KEY_LEFT):
                self.pad.update_pad(key)
            self.ball.step()
            on_x, on_y, on_track = self.wall.is_hit_me(self.ball.get_xy(), self.ball.get_ort())
            self.score = self.score + 100 * sum((on_x, on_y, on_track)) if on_x or on_y or on_track else self.score
            # checking borders of window and pad collision
            if self.ball.x == 1 or self.ball.x == self.field_width - 1:
                on_x = True
            elif self.ball.y == self.field_height - 1:
                on_y = True
            if self.pad.on_me(self.ball.x, self.ball.y):
                on_y = True
            self.ball.update_track(on_x, on_y, on_track)
            self.redraw()
        pass

