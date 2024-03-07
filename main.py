import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, master, rows, cols, mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.flags = 0
        self.game_over = False

        # Создание поля
        self.field = [[0 for _ in range(cols)] for _ in range(rows)]
        self.create_mines()
        self.calculate_numbers()

        # Создание интерфейса
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                self.buttons[i][j] = tk.Button(master, width=2, command=lambda i=i, j=j: self.click(i, j))
                self.buttons[i][j].grid(row=i, column=j)

    def create_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.field[row][col] == 0:
                self.field[row][col] = -1
                mines_placed += 1

    def calculate_numbers(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.field[i][j] != -1:
                    count = 0
                    for x in range(max(0, i - 1), min(i + 2, self.rows)):
                        for y in range(max(0, j - 1), min(j + 2, self.cols)):
                            if self.field[x][y] == -1:
                                count += 1
                    self.field[i][j] = count

    def click(self, row, col):
        if self.game_over or self.buttons[row][col]["state"] != "normal":
            return

        if self.field[row][col] == -1:
            self.buttons[row][col].config(text="💣", bg="red")
            self.game_over = True
            messagebox.showinfo("Game Over", "You lose!")
        else:
            self.reveal(row, col)

    def reveal(self, row, col):
        queue = [(row, col)]
        while queue:
            row, col = queue.pop(0)
            if self.field[row][col] != 0:
                self.buttons[row][col].config(text=str(self.field[row][col]), bg="lightgrey")
            else:
                self.buttons[row][col].config(text=" ", bg="lightgrey")
                for x in range(max(0, row - 1), min(row + 2, self.rows)):
                    for y in range(max(0, col - 1), min(col + 2, self.cols)):
                        if self.buttons[x][y]["state"] == "normal":
                            queue.append((x, y))

            self.buttons[row][col].config(state="disabled")
        if self.check_win():
            self.game_over = True
            messagebox.showinfo("Congratulations", "You win!")

    def check_win(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.field[i][j] != -1 and self.buttons[i][j]["state"] == "normal":
                    return False
        return True

def main():
    root = tk.Tk()
    root.title("Minesweeper")
    rows = 8
    cols = 8
    mines = 9
    Minesweeper(root, rows, cols, mines)
    root.mainloop()

if __name__ == "__main__":
    main()
