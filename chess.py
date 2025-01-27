import tkinter as tk
from tkinter import messagebox, ttk
import random


class ChessGame:
    def __init__(self):
        # Create difficulty selection window first
        self.difficulty_window = tk.Tk()
        self.difficulty_window.title("Zorluk Seçimi")

        self.difficulty = tk.StringVar(value="orta")

        ttk.Label(self.difficulty_window, text="Zorluk Seviyesi Seçin:").pack(pady=10)
        ttk.Radiobutton(self.difficulty_window, text="Başlangıç", variable=self.difficulty, value="başlangıç").pack()
        ttk.Radiobutton(self.difficulty_window, text="Orta", variable=self.difficulty, value="orta").pack()
        ttk.Radiobutton(self.difficulty_window, text="Zor", variable=self.difficulty, value="zor").pack()

        ttk.Button(self.difficulty_window, text="Başla", command=self.start_game).pack(pady=10)

        self.difficulty_window.mainloop()

    def start_game(self):
        self.difficulty_window.destroy()

        self.window = tk.Tk()
        self.window.title("Chess Game")

        # Create the chess board
        self.board = []
        self.buttons = []
        self.selected = None
        self.turn = "white"
        self.highlighted = []  # Store highlighted squares
        self.game_over = False

        # Initialize the board
        self.init_board()
        self.create_board_gui()

    def init_board(self):
        # Create empty board
        self.board = [[None for _ in range(8)] for _ in range(8)]

        # Set up pawns
        for i in range(8):
            self.board[1][i] = ("black", "pawn")
            self.board[6][i] = ("white", "pawn")

        # Set up other pieces
        pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        for i in range(8):
            self.board[0][i] = ("black", pieces[i])
            self.board[7][i] = ("white", pieces[i])

    def create_board_gui(self):
        # Define piece symbols
        piece_symbols = {
            ("white", "pawn"): "♙",
            ("white", "rook"): "♖",
            ("white", "knight"): "♘",
            ("white", "bishop"): "♗",
            ("white", "queen"): "♕",
            ("white", "king"): "♔",
            ("black", "pawn"): "♟",
            ("black", "rook"): "♜",
            ("black", "knight"): "♞",
            ("black", "bishop"): "♝",
            ("black", "queen"): "♛",
            ("black", "king"): "♚"
        }

        for row in range(8):
            button_row = []
            for col in range(8):
                button = tk.Button(self.window, width=4, height=2,
                                   command=lambda r=row, c=col: self.button_click(r, c),
                                   font=('Arial', 24))
                button.grid(row=row, column=col)
                button_row.append(button)

                # Set colors
                if (row + col) % 2 == 0:
                    button.configure(bg="#808080")  # Dark gray squares
                else:
                    button.configure(bg="#86A666")  # Green squares

                # Set piece text
                if self.board[row][col]:
                    color, piece = self.board[row][col]
                    button.configure(text=piece_symbols[(color, piece)])
                    if color == "white":
                        button.configure(fg="#E8E8E8")  # Lighter white for better visibility
                    else:
                        button.configure(fg="#000000")  # Black pieces stay black

            self.buttons.append(button_row)

    def clear_highlights(self):
        for r, c in self.highlighted:
            self.buttons[r][c].configure(
                bg="#808080" if (r + c) % 2 == 0 else "#86A666")
        self.highlighted = []

    def show_valid_moves(self, row, col):
        self.clear_highlights()
        piece = self.board[row][col]
        if not piece:
            return

        color, piece_type = piece

        # Check all possible squares
        for new_row in range(8):
            for new_col in range(8):
                if self.is_valid_move(row, col, new_row, new_col):
                    self.buttons[new_row][new_col].configure(bg="#90EE90")  # Light green
                    self.highlighted.append((new_row, new_col))

    def get_all_valid_moves(self, color):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] and self.board[row][col][0] == color:
                    for new_row in range(8):
                        for new_col in range(8):
                            if self.is_valid_move(row, col, new_row, new_col):
                                # Try the move
                                temp_piece = self.board[new_row][new_col]
                                self.board[new_row][new_col] = self.board[row][col]
                                self.board[row][col] = None

                                # Check if move puts own king in check
                                in_check = self.is_check(color)

                                # Undo move
                                self.board[row][col] = self.board[new_row][new_col]
                                self.board[new_row][new_col] = temp_piece

                                if not in_check:
                                    valid_moves.append((row, col, new_row, new_col))
        return valid_moves

    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                if self.board[row][col] and self.board[row][col] == (color, "king"):
                    return row, col
        return None

    def is_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos:
            return False

        opponent = "black" if color == "white" else "white"
        king_row, king_col = king_pos

        # Check all opponent pieces
        for row in range(8):
            for col in range(8):
                if self.board[row][col] and self.board[row][col][0] == opponent:
                    if self.is_valid_move(row, col, king_row, king_col):
                        return True
        return False

    def is_checkmate(self, color):
        # Get king position
        king_pos = self.find_king(color)
        if not king_pos:
            return False

        # If not in check, it's not checkmate
        if not self.is_check(color):
            return False

        # Check if king has any valid moves
        king_row, king_col = king_pos
        for new_row in range(max(0, king_row - 1), min(8, king_row + 2)):
            for new_col in range(max(0, king_col - 1), min(8, king_col + 2)):
                if self.is_valid_move(king_row, king_col, new_row, new_col):
                    # Try the move
                    temp_piece = self.board[new_row][new_col]
                    self.board[new_row][new_col] = self.board[king_row][king_col]
                    self.board[king_row][king_col] = None

                    # Check if move gets out of check
                    still_in_check = self.is_check(color)

                    # Undo move
                    self.board[king_row][king_col] = self.board[new_row][new_col]
                    self.board[new_row][new_col] = temp_piece

                    if not still_in_check:
                        return False

        # Check if any other piece can block check or capture attacking piece
        valid_moves = self.get_all_valid_moves(color)
        return len(valid_moves) == 0

    def check_only_kings(self):
        pieces_count = {"white": [], "black": []}
        for row in range(8):
            for col in range(8):
                if self.board[row][col]:
                    color, piece = self.board[row][col]
                    pieces_count[color].append(piece)

        # Check if either side has only a king left
        if (len(pieces_count["white"]) == 1 and pieces_count["white"][0] == "king") or \
                (len(pieces_count["black"]) == 1 and pieces_count["black"][0] == "king"):
            return True
        return False

    def evaluate_position(self):
        piece_values = {
            "pawn": 1,
            "knight": 3,
            "bishop": 3,
            "rook": 5,
            "queen": 9,
            "king": 0
        }

        score = 0
        for row in range(8):
            for col in range(8):
                if self.board[row][col]:
                    color, piece = self.board[row][col]
                    value = piece_values[piece]
                    if color == "black":
                        score += value
                    else:
                        score -= value
        return score

    def make_ai_move(self):
        if self.game_over:
            return

        valid_moves = self.get_all_valid_moves("black")
        if valid_moves:
            # Evaluate each move
            best_moves = []
            best_score = float('-inf')

            # Adjust evaluation based on difficulty
            difficulty_bonus = {
                "başlangıç": 0.1,  # Makes more random moves
                "orta": 0.3,  # Default bonus values
                "zor": 0.5  # Makes more strategic moves
            }

            bonus = difficulty_bonus[self.difficulty.get()]

            for move in valid_moves:
                old_row, old_col, new_row, new_col = move

                # Try move
                temp_piece = self.board[new_row][new_col]
                self.board[new_row][new_col] = self.board[old_row][old_col]
                self.board[old_row][old_col] = None

                # Evaluate position
                score = self.evaluate_position()

                # Add bonus based on difficulty
                # Checking opponent
                if self.is_check("white"):
                    score += bonus * 5
                # Controlling center squares
                if 2 <= new_row <= 5 and 2 <= new_col <= 5:
                    score += bonus * 3
                # Capturing pieces
                if temp_piece:
                    score += bonus * 2

                # Undo move
                self.board[old_row][old_col] = self.board[new_row][new_col]
                self.board[new_row][new_col] = temp_piece

                # Add randomness for easier difficulties
                if self.difficulty.get() == "başlangıç":
                    score += random.uniform(-1, 1)
                elif self.difficulty.get() == "orta":
                    score += random.uniform(-0.5, 0.5)

                if score > best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)

            # Choose randomly from best moves
            old_row, old_col, new_row, new_col = random.choice(best_moves)

            # Make the chosen move
            self.board[new_row][new_col] = self.board[old_row][old_col]
            self.board[old_row][old_col] = None

            # Update buttons
            self.buttons[new_row][new_col].configure(
                text=self.buttons[old_row][old_col].cget("text"),
                fg=self.buttons[old_row][old_col].cget("fg"))
            self.buttons[old_row][old_col].configure(text="")

            # Check for checkmate or only kings
            if self.is_checkmate("white"):
                messagebox.showinfo("Game Over", "Şah Mat! Siyah kazandı!")
                self.game_over = True
            elif self.check_only_kings():
                if len([p for row in self.board for p in row if p and p[0] == "white" and p[1] == "king"]) == 1:
                    messagebox.showinfo("Game Over", "Siyah kazandı! Beyaz şah tek kaldı!")
                else:
                    messagebox.showinfo("Game Over", "Beyaz kazandı! Siyah şah tek kaldı!")
                self.game_over = True
            elif self.is_check("white"):
                messagebox.showinfo("Şah", "Beyaz şah konumunda!")

            # Switch turns
            self.turn = "white"

    def button_click(self, row, col):
        if self.game_over or self.turn == "black":
            return  # Don't allow clicks during AI's turn or after game over

        if not self.selected:
            # Select piece
            if self.board[row][col] and self.board[row][col][0] == self.turn:
                self.selected = (row, col)
                self.buttons[row][col].configure(bg="#FFFF00")  # Yellow
                self.show_valid_moves(row, col)
        else:
            # Move piece
            old_row, old_col = self.selected

            if self.is_valid_move(old_row, old_col, row, col):
                # Move piece
                temp_piece = self.board[row][col]
                self.board[row][col] = self.board[old_row][old_col]
                self.board[old_row][old_col] = None

                # Check if move puts own king in check
                if self.is_check("white"):
                    # Undo move if it puts own king in check
                    self.board[old_row][old_col] = self.board[row][col]
                    self.board[row][col] = temp_piece
                    messagebox.showwarning("Geçersiz Hamle", "Bu hamle şahınızı tehlikeye atar!")
                else:
                    # Update buttons
                    self.buttons[row][col].configure(
                        text=self.buttons[old_row][old_col].cget("text"),
                        fg=self.buttons[old_row][old_col].cget("fg"))
                    self.buttons[old_row][old_col].configure(text="")

                    # Reset colors
                    self.clear_highlights()
                    self.buttons[old_row][old_col].configure(
                        bg="#808080" if (old_row + old_col) % 2 == 0 else "#86A666")

                    # Check for checkmate or only kings
                    if self.is_checkmate("black"):
                        messagebox.showinfo("Game Over", "Şah Mat! Beyaz kazandı!")
                        self.game_over = True
                    elif self.check_only_kings():
                        if len([p for row in self.board for p in row if p and p[0] == "black" and p[1] == "king"]) == 1:
                            messagebox.showinfo("Game Over", "Beyaz kazandı! Siyah şah tek kaldı!")
                        else:
                            messagebox.showinfo("Game Over", "Siyah kazandı! Beyaz şah tek kaldı!")
                        self.game_over = True
                    elif self.is_check("black"):
                        messagebox.showinfo("Şah", "Siyah şah konumunda!")

                    # Switch turns and make AI move
                    self.turn = "black"
                    self.window.after(500, self.make_ai_move)  # Add delay before AI move
            else:
                messagebox.showwarning("Geçersiz Hamle", "Bu hamle yapılamaz!")

            # Deselect
            self.selected = None
            self.buttons[old_row][old_col].configure(
                bg="#808080" if (old_row + old_col) % 2 == 0 else "#86A666")
            self.clear_highlights()

    def check_path_clear(self, old_row, old_col, new_row, new_col):
        row_step = 0 if new_row == old_row else (new_row - old_row) // abs(new_row - old_row)
        col_step = 0 if new_col == old_col else (new_col - old_col) // abs(new_col - old_col)

        current_row = old_row + row_step
        current_col = old_col + col_step

        while (current_row, current_col) != (new_row, new_col):
            if self.board[current_row][current_col] is not None:
                return False
            current_row += row_step
            current_col += col_step

        return True

    def is_valid_move(self, old_row, old_col, new_row, new_col):
        # Basic validation - can't capture your own piece
        if self.board[new_row][new_col] and \
                self.board[new_row][new_col][0] == self.board[old_row][old_col][0]:
            return False

        piece = self.board[old_row][old_col]
        if not piece:
            return False

        color, piece_type = piece

        # Add basic movement rules for each piece
        if piece_type == "pawn":
            direction = 1 if color == "black" else -1
            if old_col == new_col:  # Moving forward
                if new_row == old_row + direction:
                    return not self.board[new_row][new_col]
                if (color == "black" and old_row == 1) or (color == "white" and old_row == 6):
                    if new_row == old_row + 2 * direction:
                        return not self.board[new_row][new_col] and not self.board[old_row + direction][old_col]
            elif abs(old_col - new_col) == 1 and new_row == old_row + direction:
                return self.board[new_row][new_col] is not None
            return False

        elif piece_type == "rook":
            if (old_row == new_row) != (old_col == new_col):
                return self.check_path_clear(old_row, old_col, new_row, new_col)
            return False

        elif piece_type == "knight":
            row_diff = abs(new_row - old_row)
            col_diff = abs(new_col - old_col)
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

        elif piece_type == "bishop":
            if abs(new_row - old_row) == abs(new_col - old_col):
                return self.check_path_clear(old_row, old_col, new_row, new_col)
            return False

        elif piece_type == "queen":
            if (old_row == new_row) != (old_col == new_col) or \
                    abs(new_row - old_row) == abs(new_col - old_col):
                return self.check_path_clear(old_row, old_col, new_row, new_col)
            return False

        elif piece_type == "king":
            return abs(new_row - old_row) <= 1 and abs(new_col - old_col) <= 1

        return False

    def run(self):
        self.window.mainloop()


# Create and run the game
game = ChessGame()
game.run()
