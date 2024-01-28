import tkinter as tk
from typing import List


class MyButton(tk.Button):
    def __init__(self, master, x, y, *args, **kwargs):
        super(MyButton, self).__init__(
            master, width=3, font="Calibri 15 bold", *args, **kwargs
        )
        self.x = x
        self.y = y
        self.is_mine = False

    def __repr__(self):
        return f"MyButton {self.x} {self.y}"


class Sapper:
    """
    There is all logic of Sapper game here
    """

    WINDOW = tk.Tk()

    ROW: int = 10  # Default value.
    COLUMN: int = 7  # Default value.

    def __init__(self):
        self.buttons: List[List[tk.Button]] = []  # The list of cells on the minefield.
        for i in range(Sapper.ROW):
            temp = []
            for j in range(Sapper.COLUMN):
                btn = MyButton(Sapper.WINDOW, x=i, y=j)
                temp.append(btn)
            self.buttons.append(temp)

    def create_widgets(self):
        """
        Creates the cells of the minefield using coordinates

        :return: Nothing
        """
        for i in range(Sapper.ROW):
            for j in range(Sapper.COLUMN):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def start(self):
        """
        Encapsulate methods: 'create_widgets', 'print_buttons' and 'Sapper.WINDOW.mainloop()'
        :return: Nothing
        """
        self.create_widgets()
        self.print_buttons()
        Sapper.WINDOW.mainloop()

    def print_buttons(self):
        for btn in self.buttons:
            print(btn)


if __name__ == "__main__":
    game = Sapper()
    game.start()
