from copy import deepcopy  # Alt+Enter
from random import randint
from typing import Callable
import os  # Te permite acceder a to_do el contenido de tu sistema operativo

os.system('cls')


class Minesweeper:
    """Template to create the minesweeper dashboards"""

    def __init__(self, rows: int = 12, columns: int = 15):
        self.rows = rows
        self.columns = columns
        self.base_dashboard = []
        self.coordinates = []
        self.hidden_dashboard = []

    def create_dashboard(self) -> list[list]:
        """
        This function is responsible for creating the base board for the minesweeper game,
        using user-supplied values.

        :return: a matrix of dimension rows x columns.
        """

        self.base_dashboard = [['-' for _ in range(self.columns)] for _ in range(self.rows)]
        self.hidden_dashboard = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

        return deepcopy(self.base_dashboard)

    @staticmethod
    def show_dashboard(dashboard: list[list] = None):
        """
        This function takes care of printing the minesweeper dashboard created by the user.
        :return: str
        """
        for i in dashboard:
            for j in i:
                print(j, end=' ')
            print()

    def insert_mines(self):
        """
        This function is responsible for inserting the number of mines given on the base board at random.
        :return: list[list], list
        """
        mines_number = round((self.rows * self.columns) / 8)
        for minas in range(mines_number):
            i = randint(0, self.rows - 1)
            j = randint(0, self.columns - 1)
            self.coordinates.append((i, j))
            self.hidden_dashboard[i][j] = 9
        return self.hidden_dashboard, self.coordinates

    def dashboard_clues(self):
        """
        This function generates a clue board associated with the number of mines and their position.
        :return: list[list]
        """
        for i in range(self.rows):
            for j in range(self.columns):
                if self.hidden_dashboard[i][j] == 9:
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if 0 <= i + x <= self.rows - 1 and 0 <= j + y <= self.rows - 1:
                                if self.hidden_dashboard[i + x][j + y] != 9:
                                    self.hidden_dashboard[i + x][j + y] += 1

        return self.hidden_dashboard

    def dashboard_starting_point(self):
        """
        This function is responsible for generating the board with the player's starting position.
        :return: int, list[list]
        """
        upper_limit_i = round(len(self.hidden_dashboard) / 2 + 1)
        lower_limit_i = round(len(self.hidden_dashboard) / 2 - 1)
        lower_limit_j = round(len(self.hidden_dashboard) / 2 - 1)
        upper_limit_j = round(len(self.hidden_dashboard) / 2 + 1)
        i = randint(lower_limit_i, upper_limit_i)
        j = randint(lower_limit_j, upper_limit_j)
        starting_point = self.base_dashboard[i][j]
        self.base_dashboard[i][j] = 'x'
        self.show_dashboard(self.base_dashboard)
        return i, j, starting_point

    def diffusion_algorithm(self, i: int, j: int):
        """
        Diffusion algorithm function to discover the board.
        """
        coordinates_list = [(i, j)]
        while len(coordinates_list) != 0:
            f, c = coordinates_list.pop()
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if 0 <= f + x <= self.rows - 1 and 0 <= c + y <= self.columns - 1:
                        if self.base_dashboard[f + x][c + y] == '-' and self.hidden_dashboard[f + x][c + y] == 0:
                            self.base_dashboard[f + x][c + y] = ' '

                            if (f + x, c + y) not in coordinates_list:
                                coordinates_list.append((f + x, c + y))
                        else:
                            self.base_dashboard[f + x][c + y] = self.hidden_dashboard[f + x][c + y]
        return self.base_dashboard

    def play(self, mov: Callable):
        """
        This function simulates the player's click on the minesweeper box.
        """
        self.create_dashboard()
        hidden_dashboard, coordinates = self.insert_mines()
        i, j, position = self.dashboard_starting_point()
        self.dashboard_clues()
        flagged_mines = []
        condition = True

        while condition:
            start = mov()

            if start == 'w':
                if i == 0:
                    pass
                else:
                    self.base_dashboard[i][j] = position  # 'x' ---> '-'
                    i -= 1
                    position = self.base_dashboard[i][j]
                    self.base_dashboard[i][j] = 'x'

            elif start == 's':
                if i == self.rows - 1:
                    pass
                else:
                    self.base_dashboard[i][j] = position  # 'x' ---> '-'
                    i += 1
                    position = self.base_dashboard[i][j]
                    self.base_dashboard[i][j] = 'x'

            elif start == 'a':
                if j == 0:
                    pass
                else:
                    self.base_dashboard[i][j] = position  # 'x' ---> '-'
                    j -= 1
                    position = self.base_dashboard[i][j]
                    self.base_dashboard[i][j] = 'x'

            elif start == 'd':
                if j == self.columns - 1:
                    pass
                else:
                    self.base_dashboard[i][j] = position  # 'x' ---> '-'
                    j += 1
                    position = self.base_dashboard[i][j]
                    self.base_dashboard[i][j] = 'x'

            elif start == 'm':
                flagged_mines.append((i, j))
                if len(flagged_mines) == len(self.coordinates):
                    if flagged_mines.sort() == self.coordinates.sort():
                        self.base_dashboard[i][j] = '#'
                        condition = False
                else:
                    position = '#'
                    self.base_dashboard[i][j] = '#'

            elif start == 'n':
                position = '-'
                self.base_dashboard[i][j] = position
                flagged_mines.remove((i, j))
                print(flagged_mines)

            elif start == 'z':
                q = self.hidden_dashboard[i][j]
                if coordinates.count((i, j)) != 0:  # if q == 9:
                    self.base_dashboard[i][j] = '@'
                    condition = False
                elif q != 0:
                    self.base_dashboard[i][j] = q
                    position = q
                elif q == 0:
                    self.base_dashboard[i][j] = ' '
                    self.diffusion_algorithm(i, j)
                    self.base_dashboard = [
                        [' ' if self.base_dashboard[i][j] == 0 else self.base_dashboard[i][j] for j in
                         range(self.columns)]
                        for i in range(self.rows)]
                    position = self.base_dashboard[i][j]
            else:
                print('Error. Introduce a valid option.\n')

            os.system('cls')
            self.show_dashboard(self.base_dashboard)

        if self.base_dashboard[i][j] == '@':
            os.system('cls')
            self.show_dashboard(self.base_dashboard)
            print('\nYou lost :(')
        else:
            os.system('cls')
            self.show_dashboard(self.base_dashboard)
            print(f'\nYou won! :). You found {len(self.coordinates)} mines!')
