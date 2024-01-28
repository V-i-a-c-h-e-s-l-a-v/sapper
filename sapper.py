import tkinter as tk
from typing import List

window = tk.Tk()

# The grid size of the battlefield.
row: int = 5  # Default value.
column: int = 3  # Default value.

buttons: List[List[tk.Button]] = []  # The list of cells on the battlefield.
for i in range(row):
    temp = []
    for j in range(column):
        btn = tk.Button(window, width=3, font="Calibri 15 bold")
        temp.append(btn)
    buttons.append(temp)

for row_btn in buttons:
    print(row_btn)

for i in range(row):
    for j in range(column):
        btn = buttons[i][j]
        btn.grid(row=i, column=j)


if __name__ == "__main__":
    window.mainloop()
