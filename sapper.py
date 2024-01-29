import random
import tkinter as tk
from typing import List, Type
from random import shuffle


class MyButton(tk.Button):
    """
    Class MyButton describes a cell of the minefield

    Attributes:
        - master: Tkinter base widget,
        - x: Number of the minefield row,
        - y: Number of the minefield column,
        - number: The cell's number,
        - is_mine: The flag indicates whether the cell has a mine or not.

    Methods:
        - __init__: Creates the instance of class 'MyButton',
        - __repr__: Defines the string representation of class 'MyButton',
    """

    def __init__(self, master, x: int, y: int, number: int, *args, **kwargs):
        """
        Creates the instance of class 'MyButton'

        :param master: Creates the instance of class 'MyButton'
        :param x: Number of the minefield row
        :param y: Number of the minefield column
        :param number: The cell's number
        :param args: Additional arguments        :param kwargs: Additional arguments
        """
        super(MyButton, self).__init__(
            master, width=3, font="Calibri 15 bold", *args, **kwargs
        )
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False

    def __repr__(self):
        return f"MyButton {self.x} {self.y} {self.number} {self.is_mine}"


class Sapper:
    """
    There is all logic of Sapper game here.

    Attributes:
        - WINDOW: The instance of the toplevel widget of Tk which represents the main window,
        - ROW: The width of the minefield,
        - COLUMN: The length of the minefield,
        - MINE: The number of mines.

    Methods:
        - __init__: Creates the instance of class 'Sapper',
        - create_widgets: Create the cells of the minefield using their coordinates,
        - start: Encapsulate methods: 'create_widgets', 'print_buttons' and 'Sapper.WINDOW.mainloop()'
        - print_buttons: Print all buttons (cells) to the console to check their attributes,
        - mines_setting:  Setting mines in the minefield,
        - get_mines_location: Generating random coordinates for the mines location on the minefield.
    """

    WINDOW = tk.Tk()
    ROW: int = 10  # Default value.
    COLUMN: int = 7  # Default value.
    MINE: int = 3  # Default value.

    def __init__(self):
        """
        Creates the instance of class 'Sapper'
        """
        self.buttons: List[
            List[MyButton]
        ] = []  # The list of the cells on the minefield.
        cnt = 1  # The button number is the coordinate of its location as well.
        for i in range(Sapper.ROW):
            temp: List[MyButton] = []  # Collecting rows of the cells.
            for j in range(Sapper.COLUMN):
                btn = MyButton(Sapper.WINDOW, x=i, y=j, number=cnt)
                temp.append(btn)
                cnt += 1
            self.buttons.append(temp)

    def create_widgets(self):
        """
        Create the cells of the minefield using their coordinates.

        :return: Nothing
        """
        for i in range(Sapper.ROW):
            for j in range(Sapper.COLUMN):
                button = self.buttons[i][j]
                button.grid(row=i, column=j)

    def start(self):
        """
        Encapsulate methods: 'create_widgets', 'print_buttons' and 'Sapper.WINDOW.mainloop()'
        :return: Nothing
        """
        self.create_widgets()
        self.mines_setting()
        self.print_buttons()
        Sapper.WINDOW.mainloop()

    def print_buttons(self):
        """
        Print all buttons (cells) to the console to check their attributes.
        :return: Nothing
        """
        for btn in self.buttons:
            print(btn)

    def mines_setting(self):
        """
        Setting mines in the minefield.
        :return: Nothing
        """
        index_mines = self.get_mines_location()
        print(index_mines)  # To check the position of mines only.
        for row_btn in self.buttons:
            for btn in row_btn:
                if btn.number in index_mines:
                    btn.is_mine = True  # If the cell value is True, the mine is there; otherwise, it is False by
                    # default.

    @staticmethod
    def get_mines_location():
        """
        Generating random coordinates for the mines location on the minefield.
        :return: Nothing
        """
        indexes = list(range(1, (Sapper.ROW * Sapper.COLUMN + 1)))
        shuffle(indexes)
        return indexes[
            : Sapper.MINE
        ]  # The list length has been limited by the number of mines.


if __name__ == "__main__":
    game = Sapper()
    game.start()
