import random
import os
import tkinter as tk
from tkinter import messagebox


class SerhatGUI:
    def __init__(self, master):
        self.master = master
        self.size = 8
        self.num_mines = 10
        self.buttons = []
        self.field = None
        self.mines = None
        self.revealed = None
        self.game_over = False

        # Set window title and icon
        master.title("Serhat")
        master.configure(bg='#2c3e50')

        # Create menu with modern styling
        menubar = tk.Menu(master)
        game_menu = tk.Menu(menubar, tearoff=0, bg='#34495e', fg='white')
        game_menu.add_command(label="New Game", command=self.new_game)

        # Add difficulty menu
        difficulty_menu = tk.Menu(game_menu, tearoff=0, bg='#34495e', fg='white')
        difficulty_menu.add_command(label="Easy (8x8, 10 mines)", command=lambda: self.set_difficulty(8, 10))
        difficulty_menu.add_command(label="Medium (16x16, 40 mines)", command=lambda: self.set_difficulty(16, 40))
        difficulty_menu.add_command(label="Hard (24x24, 99 mines)", command=lambda: self.set_difficulty(24, 99))
        game_menu.add_cascade(label="Difficulty", menu=difficulty_menu)

        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="Game", menu=game_menu)
        master.config(menu=menubar)

        # Create button grid with modern styling
        self.button_frame = tk.Frame(master, bg='#2c3e50', padx=10, pady=10)
        self.button_frame.pack(expand=True)

        self.new_game()

    def set_difficulty(self, size, mines):
        self.size = size
        self.num_mines = mines
        self.new_game()

    def new_game(self):
        self.game_over = False
        # Clear existing buttons
        for row in self.buttons:
            for button in row:
                button.destroy()

        # Initialize game
        self.field, self.mines = create_minefield(self.size, self.num_mines)
        self.revealed = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.buttons = []

        # Calculate numbers
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] != '*':
                    count = count_adjacent_mines(self.field, i, j, self.size)
                    self.field[i][j] = str(count) if count > 0 else ' '

        # Create buttons with modern styling
        for i in range(self.size):
            button_row = []
            for j in range(self.size):
                btn = tk.Button(self.button_frame, width=2, height=1,
                                command=lambda x=i, y=j: self.click(x, y),
                                font=('Arial', 10, 'bold'),
                                bg='#3498db',
                                activebackground='#2980b9',
                                relief='raised',
                                bd=1)
                btn.grid(row=i, column=j, padx=1, pady=1)
                btn.bind('<Button-3>', lambda e, x=i, y=j: self.right_click(x, y))
                button_row.append(btn)
            self.buttons.append(button_row)

    def click(self, x, y):
        if self.game_over or self.revealed[x][y]:
            return

        if (x, y) in self.mines:
            self.game_over = True
            self.buttons[x][y].config(text='💣', bg='#e74c3c')
            messagebox.showinfo("Game Over", "BOOM! You hit a mine!")
            self.reveal_all()
        else:
            self.reveal_empty_cells_gui(x, y)
            if self.check_win():
                self.game_over = True
                messagebox.showinfo("Congratulations", "You won! 🎉")
                self.reveal_all()

    def right_click(self, x, y):
        if not self.revealed[x][y] and not self.game_over:
            current = self.buttons[x][y].cget('text')
            if current == '':
                self.buttons[x][y].config(text='🚩', fg='#e74c3c')
            elif current == '🚩':
                self.buttons[x][y].config(text='')

    def reveal_empty_cells_gui(self, x, y):
        if not (0 <= x < self.size and 0 <= y < self.size) or self.revealed[x][y]:
            return

        self.revealed[x][y] = True
        cell_value = self.field[x][y]

        # Color coding for numbers
        colors = {
            '1': '#2ecc71',
            '2': '#3498db',
            '3': '#e74c3c',
            '4': '#8e44ad',
            '5': '#c0392b',
            '6': '#16a085',
            '7': '#2c3e50',
            '8': '#7f8c8d'
        }

        self.buttons[x][y].config(
            text=cell_value,
            state='disabled',
            bg='#ecf0f1',
            disabledforeground=colors.get(cell_value, 'black')
        )

        if cell_value == ' ':
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    self.reveal_empty_cells_gui(x + dx, y + dy)

    def check_win(self):
        unrevealed_count = sum(row.count(False) for row in self.revealed)
        return unrevealed_count == len(self.mines)

    def reveal_all(self):
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) in self.mines:
                    self.buttons[i][j].config(text='💣', bg='#e74c3c')
                else:
                    cell_value = self.field[i][j]
                    colors = {
                        '1': '#2ecc71',
                        '2': '#3498db',
                        '3': '#e74c3c',
                        '4': '#8e44ad',
                        '5': '#c0392b',
                        '6': '#16a085',
                        '7': '#2c3e50',
                        '8': '#7f8c8d'
                    }
                    self.buttons[i][j].config(
                        text=cell_value,
                        state='disabled',
                        bg='#ecf0f1',
                        disabledforeground=colors.get(cell_value, 'black')
                    )


def create_minefield(size, num_mines):
    field = [[' ' for _ in range(size)] for _ in range(size)]
    mines = set()

    while len(mines) < num_mines:
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            field[x][y] = '*'

    return field, mines


def count_adjacent_mines(field, x, y, size):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < size and 0 <= new_y < size:
                if field[new_x][new_y] == '*':
                    count += 1
    return count


if __name__ == '__main__':
    root = tk.Tk()
    game = SerhatGUI(root)
    root.mainloop()
