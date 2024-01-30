import random
import tkinter as tk
from typing import List, Type
from random import shuffle

colors = {
    1: "#42e3f5",
    2: "#42a4f5",
    3: "#4275f5",
    5: "#7842f5",
    6: "#a742f5",
    7: "#42f551",
    8: "#f5a442",
}  # Setting colors for each value of the mine counter.


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

    def __init__(self, master, x: int, y: int, number=0, *args, **kwargs):
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
        self.mine_cnt = 0

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
        - click: Handling the buttons clicks,
        - create_widgets: Create the cells of the minefield using their coordinates,
        - start: Encapsulate methods: 'create_widgets', 'print_buttons' and 'Sapper.WINDOW.mainloop()'
        - print_buttons: Print all buttons (cells) to the console to check their attributes,
        - mines_setting:  Setting mines in the minefield,
        - get_mines_location: Generating random coordinates for the mines location on the minefield.

    """

    WINDOW = tk.Tk()
    ROW: int = 5  # Default value.
    COLUMN: int = 5  # Default value.
    MINE: int = 5  # Default value.

    def __init__(self):
        """
        Creates the instance of class 'Sapper'
        """
        self.buttons: List[
            List[MyButton]
        ] = []  # The list of the cells on the minefield.

        for i in range(
            Sapper.ROW + 2
        ):  # Two extra rows have been added to simplify calculation of the number of cells.
            temp: List[MyButton] = []  # Collecting rows of the cells.
            for j in range(
                Sapper.COLUMN + 2
            ):  # Two extra columns have been added to simplify calculation of the number of cells.
                btn = MyButton(
                    Sapper.WINDOW, x=i, y=j
                )  # The number zero is the default button number.
                btn.config(
                    command=lambda button=btn: self.click(button)
                )  # The command can't be executed directly in 'btn' because the button object doesn't yet
                # exist.
                temp.append(btn)
            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):
        """
        Handling the buttons clicks.
        :param clicked_button: The instance of class 'MyButton'
        :return:
        """
        if clicked_button.is_mine:
            # Check if the cell has a mine and changing the button configuration based on the result.
            clicked_button.config(
                text="*", background="red", disabledforeground="black"
            )
        else:
            # Assigning the font color of the cell value according to the number of mines.
            color = colors.get(clicked_button.mine_cnt, "black")
            if clicked_button.mine_cnt:
                clicked_button.config(
                    text=clicked_button.mine_cnt, disabledforeground=color
                )
            else:
                # If the number of mines is 0 the cell switches off.
                clicked_button.config(text="", disabledforeground=color)
        # After clicking the button provides a new button visualization.
        clicked_button.config(state="disabled")
        clicked_button.config(relief=tk.SUNKEN)

    def create_widgets(self):
        """
        Create the cells of the minefield using their coordinates.

        :return: None
        """
        for i in range(1, Sapper.ROW + 1):
            for j in range(1, Sapper.COLUMN + 1):
                # Determining the minefield area.
                button = self.buttons[i][j]
                button.grid(row=i, column=j)

    def open_all_buttons(self):
        """
        Opening the values of all buttons for debugging purposes
        :return: None
        """

        for i in range(Sapper.ROW + 2):
            for j in range(Sapper.COLUMN + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text="*", background="red", disabledforeground="black")

                elif btn.mine_cnt in colors:
                    color = colors.get(
                        btn.mine_cnt, "black"
                    )  # Assigning the font color of the cell value according to the number of mines.
                    btn.config(text=btn.mine_cnt, fg=color)

    def start(self):
        """
        Encapsulate methods: 'create_widgets', 'print_buttons' and 'Sapper.WINDOW.mainloop()'
        :return: None
        """
        self.create_widgets()
        self.mines_setting()
        self.cnt_mines()
        self.print_buttons()
        # self.open_all_buttons()  # Opening the values of all buttons for debugging purposes.
        Sapper.WINDOW.mainloop()

    def print_buttons(self):
        """
        Print all buttons (cells) to the console to check their attributes.
        :return: None
        """

        for i in range(1, Sapper.ROW + 1):
            for j in range(1, Sapper.COLUMN + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print("M", end="")
                else:
                    print(btn.mine_cnt, end="")
            print()

    def mines_setting(self):
        """
        Setting mines in the minefield.
        :return: None
        """
        index_mines = self.get_mines_location()
        print(index_mines)  # To check the position of mines only.
        cnt = 1  # The button number is the coordinate of its location as well.
        for i in range(1, Sapper.ROW + 1):
            # Determining the rows of the minefield.
            for j in range(1, Sapper.COLUMN + 1):
                # Determining the column of the minefield.
                btn = self.buttons[i][j]
                btn.number = cnt
                if btn.number in index_mines:
                    btn.is_mine = True  # If the cell value is True, the mine is there; otherwise, it is False by
                    # default.
                cnt += 1

    def cnt_mines(self):
        """
        Counting the mines located next to the cell.
        :return: None
        """
        for i in range(1, Sapper.ROW + 1):
            for j in range(1, Sapper.COLUMN + 1):
                btn = self.buttons[i][j]
                mine_cntr = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            # Pascal triangle algorithm.
                            ngbr_cells = self.buttons[i + row_dx][j + col_dx]
                            if ngbr_cells.is_mine:
                                mine_cntr += 1
                btn.mine_cnt = mine_cntr

    @staticmethod
    def get_mines_location():
        """
        Generating random coordinates for the mines location on the minefield.
        :return: None
        """
        indexes = list(
            range(1, (Sapper.ROW * Sapper.COLUMN + 1))
        )  # Determining the minefield area.
        shuffle(indexes)
        return indexes[
            : Sapper.MINE
        ]  # The list length has been limited by the number of mines.


if __name__ == "__main__":
    game = Sapper()
    game.start()
