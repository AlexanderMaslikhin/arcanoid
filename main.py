from time import sleep
import curses
import curses.ascii
import locale
from game.arcanoid import GameField

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

level = {
    1: (10, 3, 15),
    2: (10, 4, 10),
    3: (15, 3, 15),
    4: (15, 4, 15),
    5: (15, 5, 10),
    6: (20, 3, 15),
    7: (20, 4, 15),
    8: (20, 5, 15),
    9: (20, 5, 10),
}


def show_menu():
    print("Игра по типу арканоида. ")
    print("Управление стрелками вправо и влево.")
    print("Дается три попытки")
    print("Блоки разного цвета, цвет блока показывает его броню от 1 до 5")
    print("При ударе мячом блок теряет 1 очко брони или исчезает, если брони больше нет")
    print("Для паузы нажмите 'p'")
    print("Если надоест, нажмите 'q' для выхода")
    print("-" * 20)
    print("Выберите сложность игры:")
    for i, lvl in level.items():
        print(f"\t{i}. Скорость {lvl[0]}, тольщина стены {lvl[1]}, длина ракетки {lvl[2]}")
    while True:
        choice = input("Ваш выбор: ")
        if choice.isdigit():
            choice = int(choice)
            if 0 < choice < len(level):
                return choice
        print("Попробуйте еще раз")


def run(window, difficulty_level):
    speed, wall_thick, pad_size = level[difficulty_level]
    window.leaveok(True)
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()

    window.scrollok(False)
    window.keypad(True)

    curses.start_color()
    curses.use_default_colors()
    field = GameField(window, speed=speed, pad_size=pad_size, wall_thickness=wall_thick)
    return field.run_game()


score = curses.wrapper(run, show_menu())

print(f'Вы набрали {score} очков')
