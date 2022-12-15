import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                screen.move(1 + i, 1 + j)
                if self.life.curr_generation[i][j] == 1:
                    screen.addch("*")
                else:
                    screen.addch(" ")

    def run(self) -> None:
        screen = curses.initscr()
        curses.resize_term(self.life.rows + 2, self.life.cols + 2)
        running = True
        while running:
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.life.step()
            time.sleep(0.01)
            screen.refresh()
        curses.endwin()
