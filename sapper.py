import random
import tkinter as tk
from typing import List, Type
from random import shuffle
from tkinter.messagebox import showinfo

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
        self.mine_cnt = 0  # The numbers of mines.
        self.is_open = False

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
    ROW: int = 10  # Default value.
    COLUMN: int = 10  # Default value.
    MINE: int = 25  # Default value.
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

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
        if Sapper.IS_FIRST_CLICK:
            self.mines_setting(clicked_button.number)
            self.cnt_mines()
            self.print_buttons()
        if clicked_button.is_mine:
            # Check if the cell has a mine and changing the button configuration based on the result.
            clicked_button.config(
                text="*", background="red", disabledforeground="black"
            )
            clicked_button.is_open = True
            Sapper.IS_GAME_OVER = True
            showinfo("Game over", "GAME OVER!")
            for i in range(1, Sapper.ROW + 1):
                for j in range(1, Sapper.COLUMN + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn["text"] = "*"

        else:
            # Assigning the font color of the cell value according to the number of mines.
            color = colors.get(clicked_button.mine_cnt, "black")
            if clicked_button.mine_cnt:
                clicked_button.config(
                    text=clicked_button.mine_cnt, disabledforeground=color
                )
                clicked_button.is_open = True
            else:
                # The breadth first search method to open all empty cells (mines counter = 0).
                self.breadth_frst_search(clicked_button)
                clicked_button.is_open = True
        # After clicking the button provides a new button visualization.
        clicked_button.config(state="disabled")
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_frst_search(self, btn: MyButton):
        """
        The breadth first search method to open all empty cells (mines counter = 0).
        :param btn: The value of mines counter.
        :return:None
        """
        queue = [btn]

        while queue:
            # The loop checks the value of the nearest cells.
            cur_btn = (
                queue.pop()
            )  # The queue of cells is initialized with empty cell (mines counter = 0).
            color = colors.get(cur_btn.mine_cnt, "black")
            if cur_btn.mine_cnt:
                # If current cell has a mine this cell will be colored with 'color' variable.
                cur_btn.config(text=cur_btn.mine_cnt, disabledforeground=color)
            else:
                # If not current cell has a mine this cell will be colored with black color.
                cur_btn.config(text="", disabledforeground=color)
                cur_btn.is_open = True
            # After clicking the button provides a new button visualization.
            cur_btn.config(state="disabled")
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.mine_cnt == 0:
                # To get the values of all the nearest cells.
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if not abs(dx - dy) == 1:
                        #     continue
                        next_btn = self.buttons[x + dx][y + dy]
                        if (
                            not next_btn.is_open
                            and 1 <= next_btn.x <= Sapper.ROW
                            and 1 <= next_btn.y <= Sapper.COLUMN
                            and next_btn not in queue
                        ):
                            queue.append(next_btn)

    def create_widgets(self):
        """
        Create the cells of the minefield using their coordinates.

        :return: None
        """
        count = 1
        for i in range(1, Sapper.ROW + 1):
            for j in range(1, Sapper.COLUMN + 1):
                # Determining the minefield area.
                button = self.buttons[i][j]
                button.number = count
                button.grid(row=i, column=j)
                count += 1

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

    def mines_setting(self, number):
        """
        Setting mines in the minefield.
        :return: None
        """
        index_mines = self.get_mines_location(number)
        print(index_mines)  # To check the position of mines only.

        for i in range(1, Sapper.ROW + 1):
            # Determining the rows of the minefield.
            for j in range(1, Sapper.COLUMN + 1):
                # Determining the column of the minefield.
                btn = self.buttons[i][j]

                if btn.number in index_mines:
                    btn.is_mine = True  # If the cell value is True, the mine is there; otherwise, it is False by
                    # default.

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
    def get_mines_location(exclude_number: int):
        """
        Generating random coordinates for the mines location on the minefield.
        :return: None
        """
        indexes = list(
            range(1, (Sapper.ROW * Sapper.COLUMN + 1))
        )  # Determining the minefield area.
        print(f"Exclude cell {exclude_number}")
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[
            : Sapper.MINE
        ]  # The list length has been limited by the number of mines.


if __name__ == "__main__":
    game = Sapper()
    game.start()
