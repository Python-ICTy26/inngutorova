import pathlib
import random
import typing as tp


Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid: Grid = []
        if randomize:
            for i in range(0, self.rows):
                grid.append([])
                for j in range(0, self.cols):
                    grid[i].append(random.randint(0, 1))
        else:
            for i in range(0, self.rows):
                grid.append([])
                for j in range(0, self.cols):
                    grid[i].append(0)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        a = cell[1]
        b = cell[0]
        out: Cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    if 0 <= a + j < len(self.curr_generation[0]) and 0 <= b + i < len(
                        self.curr_generation
                    ):
                        out.append(self.curr_generation[b + i][a + j])
        return out

    def get_next_generation(self) -> Grid:
        out: Grid = []
        for i in range(0, self.rows):
            out.append([])
            for j in range(0, self.cols):
                out[i].append(0)
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[0])):
                cell: Cell = (i, j)
                sum = self.get_neighbours(cell).count(1)
                if self.curr_generation[i][j] and sum == 2 or sum == 3:
                    out[i][j] = 1
        return out

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded and self.is_changing:
            self.prev_generation = self.curr_generation
            self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations >= self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation == self.curr_generation:
            return False
        else:
            return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        file = open(filename)
        whole = file.readlines()
        grid = []
        for i in range(len(whole)):
            if whole[i] != "\n":
                whole[i] = whole[i][:-1]
                row = [int(n) for n in list(whole[i])]
                grid.append(row)
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        file.close()
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, "w")
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[0])):
                file.write(str(self.curr_generation[i][j]))
            file.write("\n")
        file.close()
