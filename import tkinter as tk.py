import tkinter as tk
from tkinter import messagebox
from queue import Queue, PriorityQueue
import time

# Helper Functions
def is_valid(board, row, col, num):
    """Check if placing num at board[row][col] is valid."""
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
        if board[box_row + i // 3][box_col + i % 3] == num:
            return False
    return True

def find_empty_cell(board):
    """Find the next empty cell on the Sudoku board."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

def update_gui(board, elapsed_time, delay=0.05):
    """Update the GUI with the current board state."""
    for row in range(9):
        for col in range(9):
            entries[row][col].delete(0, tk.END)
            if board[row][col] != 0:
                entries[row][col].insert(0, str(board[row][col]))
    time_label.config(text=f"Elapsed Time: {elapsed_time:.2f} seconds")
    root.update()
    time.sleep(delay)

# BFS Solver
def bfs_solver(board):
    queue = Queue()
    queue.put(board)
    start_time = time.time()
    while not queue.empty():
        current_board = queue.get()
        elapsed_time = time.time() - start_time
        update_gui(current_board, elapsed_time)  # Show each step
        empty_cell = find_empty_cell(current_board)
        if not empty_cell:
            return current_board
        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = [row[:] for row in current_board]
                new_board[row][col] = num
                queue.put(new_board)
    return None

# DFS Solver
def dfs_solver(board):
    stack = [board]
    start_time = time.time()
    while stack:
        current_board = stack.pop()
        elapsed_time = time.time() - start_time
        update_gui(current_board, elapsed_time)  # Show each step
        empty_cell = find_empty_cell(current_board)
        if not empty_cell:
            return current_board
        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = [row[:] for row in current_board]
                new_board[row][col] = num
                stack.append(new_board)
    return None

# UCS Solver
def ucs_solver(board):
    pq = PriorityQueue()
    pq.put((0, board))
    start_time = time.time()
    while not pq.empty():
        cost, current_board = pq.get()
        elapsed_time = time.time() - start_time
        update_gui(current_board, elapsed_time)  # Show each step
        empty_cell = find_empty_cell(current_board)
        if not empty_cell:
            return current_board
        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = [row[:] for row in current_board]
                new_board[row][col] = num
                pq.put((cost + 1, new_board))
    return None

def reset():
    """Clear all entries."""
    for row in range(9):
        for col in range(9):
            entries[row][col].delete(0, tk.END)
            if default_board[row][col] != 0:
                entries[row][col].insert(0, str(default_board[row][col]))
    time_label.config(text="Elapsed Time: 0.00 seconds")

def load_board():
    """Load the board from the GUI entries."""
    board = []
    for row in range(9):
        current_row = []
        for col in range(9):
            value = entries[row][col].get()
            current_row.append(int(value) if value.isdigit() else 0)
        board.append(current_row)
    return board

def solve_with_algorithm(algorithm):
    """Solve the Sudoku puzzle with the selected algorithm."""
    board = load_board()
    solved_board = algorithm(board)
    if solved_board:
        update_gui(solved_board, time.time() - time.struct_time, delay=0)  # Final update without delay
        messagebox.showinfo("Success", f"Sudoku solved using {algorithm._name_}!")
    else:
        messagebox.showerror("Error", "No solution exists!")

# Default Sudoku Puzzle
default_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# GUI Setup
root = tk.Tk()
root.title("Sudoku Solver with Timing")
root.geometry("600x700")
root.configure(bg='#2e3b4e')  # Set a dark background for the window

entries = [[None for _ in range(9)] for _ in range(9)]

# Create a grid of Entry widgets
for row in range(9):
    for col in range(9):
        entry = tk.Entry(root, width=4, font=('Arial', 18), justify='center', bg='white', fg='black', bd=2, relief="solid")
        entry.grid(row=row, column=col, padx=2, pady=2, ipady=10)
        entries[row][col] = entry
        if default_board[row][col] != 0:
            entry.insert(0, str(default_board[row][col]))

# Elapsed Time Label
time_label = tk.Label(root, text="Elapsed Time: 0.00 seconds", font=('Arial', 14), fg='white', bg='#2e3b4e')
time_label.grid(row=9, column=0, columnspan=9, pady=15)

# Buttons for Algorithms
button_frame = tk.Frame(root, bg='#2e3b4e')
button_frame.grid(row=10, column=0, columnspan=9, pady=10)

# Set button colors
button_color = "#4CAF50"  # Green button color
button_hover_color = "#45a049"  # Slightly darker green on hover

def on_enter(button):
    button['background'] = button_hover_color

def on_leave(button):
    button['background'] = button_color

# Create buttons for BFS, DFS, and UCS with hover effect
bfs_button = tk.Button(button_frame, text="Solve with BFS", font=('Arial', 12), bg=button_color, fg='white',
                       command=lambda: solve_with_algorithm(bfs_solver))
bfs_button.grid(row=0, column=0, padx=5)
bfs_button.bind("<Enter>", lambda e: on_enter(bfs_button))
bfs_button.bind("<Leave>", lambda e: on_leave(bfs_button))

dfs_button = tk.Button(button_frame, text="Solve with DFS", font=('Arial', 12), bg=button_color, fg='white',
                       command=lambda: solve_with_algorithm(dfs_solver))
dfs_button.grid(row=0, column=1, padx=5)
dfs_button.bind("<Enter>", lambda e: on_enter(dfs_button))
dfs_button.bind("<Leave>", lambda e: on_leave(dfs_button))

ucs_button = tk.Button(button_frame, text="Solve with UCS", font=('Arial', 12), bg=button_color, fg='white',
                       command=lambda: solve_with_algorithm(ucs_solver))
ucs_button.grid(row=0, column=2, padx=5)
ucs_button.bind("<Enter>", lambda e: on_enter(ucs_button))
ucs_button.bind("<Leave>", lambda e: on_leave(ucs_button))

# Run the GUI
root.mainloop()