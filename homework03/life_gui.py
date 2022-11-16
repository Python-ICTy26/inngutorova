import random
import time

import pygame
from life import GameOfLife
from pygame import QUIT
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 15, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen_size = (
            self.life.cols * self.cell_size,
            self.life.rows * self.cell_size,
        )
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        for x in range(0, self.life.cols):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (x * self.cell_size, 0),
                (x * self.cell_size, self.life.rows * self.cell_size),
            )
        for y in range(0, self.life.rows):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (0, y * self.cell_size),
                (self.life.cols * self.cell_size, y * self.cell_size),
            )

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    color = "green"
                else:
                    color = "white"
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(color),
                    (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size),
                )

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    x = (x - 1) // self.cell_size
                    y = (y - 1) // self.cell_size
                    self.life.curr_generation[y][x] = 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not paused:
                            paused = True
                        else:
                            paused = False

            self.draw_grid()
            self.draw_lines()
            if not paused:
                self.life.step()
            pygame.display.flip()
            clock.tick(self.speed)
            time.sleep(0.5)
        pygame.quit()
