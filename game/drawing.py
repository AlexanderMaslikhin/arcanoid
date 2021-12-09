from abc import ABC, abstractmethod
from .functions import correct_y, line_track
import curses


class DrawObject(ABC):
    def __init__(self, x, y):
        self.position = [x, y]

    @abstractmethod
    def draw(self, windows):
        pass

    def get_xy(self):
        return tuple(self.position)

    def __getattr__(self, item):
        if item in 'xy':
            if item == 'x':
                ret = self.position[0]
            elif item == 'y':
                ret = self.position[1]
            return ret
        else:
            raise AttributeError(f'There is no attrubute {item}')


class Block(DrawObject):
    def __init__(self, x, y, armor, length):
        super().__init__(x, y)
        self.char = curses.ACS_BOARD
        assert 0 < armor < 6
        self.armor = armor
        self.length = length
        self.checked = False

    def draw(self, window):
        self.checked = False
        for i in range(self.length):
            window.addch(correct_y(self.y, window.getmaxyx()[0]), self.x + i, self.char, curses.color_pair(self.armor))

    # def is_inside(self, x, y):
    #     res = self.y == y and self.x <= x < self.x + self.len
    #     if res and self.armor:
    #         self.armor -= 1
    #     return res

    def hit(self):
        if self.armor:
            self.armor -= 1
            with open("log_block.txt", "a") as f:
                f.write(f'i was hit {self}. my new armor{self.armor}\n')

    def i_am_here(self, other):
        x, y = other
        res = self.y == y and self.x <= x < self.x + self.length
        return res


class Ball(DrawObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.char = ord('*')
        bias = y - x
        self.track = [1, 1, bias]  # x direction(1,-1), k - tan(angle) k может быть любым, но пока для простоты 1, bias. y = k*x+bias

    def step(self):
        self.position[0] += self.track[0]  # changing x coord
        self.position[1] = line_track(*self.track[1:], self.position[0])  # get y coord

    def get_ort(self):
        y_dir = self.track[1] // abs(self.track[1])
        return self.track[0], y_dir

    def update_track(self, on_x, on_y, on_track):
        if sum((on_x, on_y, on_track)):
            if on_x and on_y or on_track and not on_x and not on_y:
                self.track[0] = -self.track[0]  # changing direction on X axis
            elif on_x:
                self.track[0] = -self.track[0]  # changing direction on X axis
                self.track[1] = -self.track[1]  # changing angle
            elif on_y:
                self.track[1] = -self.track[1]  # changing angle
            self.track[2] = self.position[1] - self.track[1] * self.position[0] # chaging bias b = y - k*x
        pass

    def draw(self, window):
        window.addch(correct_y(self.y, window.getmaxyx()[0]), self.x, self.char, curses.color_pair(0))


class Pad(DrawObject):
    def __init__(self, x, y, length):
        super().__init__(x, y)
        self.length = length
        self.char = curses.ACS_BOARD

    def update_pad(self, key):
        if key == curses.KEY_LEFT:
            self.position[0] -= 2
        if key == curses.KEY_RIGHT:
            self.position[0] += 2

    def draw(self, window):
        for i in range(self.length):
            window.addch(correct_y(self.y, window.getmaxyx()[0]), self.x + i, self.char, curses.color_pair(0))

    def on_me(self, x, y):
        return self.y == y - 1 and self.x <= x < self.x + self.length


class Wall:
    def __init__(self, thickness, length, start_y):
        assert 0 < thickness < 6
        self.blocks = []
        block_len = length // 15
        start_at = (length % 15) // 2
        for i in range(thickness, 0, -1):
            armor = i + 1
            for j in range(15):
                self.blocks.append(Block(start_at + j * block_len, start_y + i, armor, block_len))

    def del_killed(self):
        for elem in self.blocks[:]:
            if not elem.armor:
                self.blocks.remove(elem)

    def is_empty(self):
        return len(self.blocks) == 0

    def __len__(self):
        return len(self.blocks)

    def draw(self, window):
        [elem.draw(window) for elem in self.blocks]

    def find_block(self, coord):
        for i, block in enumerate(self.blocks):
            if block.i_am_here(coord):
                return True, i
        return False, -1
        pass

    def is_hit_me(self, cur_pos, ort):

        """
        3 bit число по нахождению объектов на пути мяча
            X Y Diag   | __ пример
            1 1  1     | *   011(x=0, y=1, diag=1, направление вверх и вправо)
        """

        self.del_killed()
        # with open("log_block.txt", "a") as f:
        #     f.write(f'{on_x}, {on_y}, {on_track}\n')
        # return on_x, on_y, on_track

