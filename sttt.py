import tkinter as tk
from tkinter import messagebox

class LocalBoard:
    def __init__(self, master, row, col):
        self.frame = tk.Frame(master, borderwidth=1, relief="solid", bg="#121212")
        self.frame.grid(row=row, column=col, padx=5, pady=5)
        self.buttons = [[tk.Button(self.frame, text="", width=5, height=2, font=("Courier", 18), command=lambda r=r, c=c: self.click(r, c), relief="raised", borderwidth=2, bg="#1f1f1f", fg="#e0e0e0") for c in range(3)] for r in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].grid(row=r, column=c, padx=2, pady=2)
        self.winner = None
        self.row = row
        self.col = col

    def click(self, r, c):
        if self.buttons[r][c]["text"] == "" and not self.winner and (next_local_board is None or (self.row, self.col) == next_local_board):
            self.buttons[r][c]["text"] = current_player
            self.buttons[r][c].config(fg="#03dac6" if current_player == "O" else "#cf6679")
            if check_winner([[self.buttons[r][c].cget("text") for c in range(3)] for r in range(3)], current_player):
                self.winner = current_player
                global_board[self.row][self.col].config(text=current_player, state="disabled")
                for br in range(3):
                    for bc in range(3):
                        self.buttons[br][bc].grid_remove()
                giant_label = tk.Label(self.frame, text=current_player, font=("Courier", 40), fg="#03dac6" if current_player == "O" else "#cf6679", bg="#121212")
                giant_label.grid(row=0, column=0, rowspan=3, columnspan=3)
            elif is_full(self):
                self.winner = "Draw"
                global_board[self.row][self.col].config(text="Draw", state="disabled")
                for br in range(3):
                    for bc in range(3):
                        self.buttons[br][bc].grid_remove()
                giant_label = tk.Label(self.frame, text="Draw", font=("Courier", 40), fg="#e0e0e0", bg="#121212")
                giant_label.grid(row=0, column=0, rowspan=3, columnspan=3)
            next_move(self.row, self.col, r, c)

    def reset(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.buttons = [[tk.Button(self.frame, text="", width=5, height=2, font=("Courier", 18), command=lambda r=r, c=c: self.click(r, c), relief="raised", borderwidth=2, bg="#1f1f1f", fg="#e0e0e0") for c in range(3)] for r in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].grid(row=r, column=c, padx=2, pady=2)
        self.winner = None

    def set_active(self, active, player=None):
        if active:
            bg = "#03dac6" if player == "O" else "#cf6679"
        else:
            bg = "#1f1f1f"
        self.frame.config(bg=bg)
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(bg=bg, fg="#121212" if self.buttons[r][c]["text"] == "O" and active else ("#121212" if self.buttons[r][c]["text"] == "X" and active else self.buttons[r][c]["fg"]))

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(row[col] == player for row in board):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(board.buttons[r][c].cget("text") != "" for r in range(3) for c in range(3))

def is_global_draw():
    for r in range(3):
        for c in range(3):
            if global_board[r][c].cget("text") == "":
                return False
    return True

def next_move(row, col, r, c):
    global current_player, next_local_board
    if check_winner([[global_board[r][c].cget("text") for c in range(3)] for r in range(3)], current_player):
        messagebox.showinfo("Super Tic-Tac-Toe", f"Player {current_player} wins the game!")
        reset_board()
        return
    elif is_full(local_boards[row][col]):
        local_boards[row][col].winner = "Draw"
        global_board[row][col].config(text="Draw", state="disabled")

    if is_global_draw():
        messagebox.showinfo("Super Tic-Tac-Toe", "The game is a draw!")
        reset_board()
        return

    if local_boards[row][col].winner or global_board[r][c].cget("text") != "":
        next_local_board = None
        for r in range(3):
            for c in range(3):
                if not local_boards[r][c].winner:
                    local_boards[r][c].set_active(True, current_player)
                    for br in range(3):
                        for bc in range(3):
                            local_boards[r][c].buttons[br][bc].config(state="normal")
                else:
                    local_boards[r][c].set_active(False)
                    for br in range(3):
                        for bc in range(3):
                            local_boards[r][c].buttons[br][bc].config(state="disabled")
    else:
        next_local_board = (r, c) if not local_boards[r][c].winner else None
        if next_local_board and local_boards[next_local_board[0]][next_local_board[1]].winner:
            next_local_board = None

        for r in range(3):
            for c in range(3):
                local_boards[r][c].set_active((r, c) == next_local_board, current_player)
                for br in range(3):
                    for bc in range(3):
                        local_boards[r][c].buttons[br][bc].config(state="normal" if (r, c) == next_local_board else "disabled")

    current_player = "O" if current_player == "X" else "X"

def reset_board():
    global current_player, next_local_board
    current_player = "X"
    next_local_board = None
    for r in range(3):
        for c in range(3):
            local_boards[r][c].reset()
            global_board[r][c].config(text="", state="normal")

root = tk.Tk()
root.title("Super Tic-Tac-Toe")

global_board = [[tk.Label(root, text="", width=10, height=5, borderwidth=1, relief="solid", bg="#1f1f1f", fg="#e0e0e0", font=("Courier", 24)) for c in range(3)] for r in range(3)]
local_boards = [[LocalBoard(root, r, c) for c in range(3)] for r in range(3)]

for r in range(3):
    for c in range(3):
        global_board[r][c].grid(row=r, column=c, padx=5, pady=5)

current_player = "X"
next_local_board = None

reset_board()
root.mainloop()