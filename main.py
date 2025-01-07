import tkinter as tk
import time
from collections import deque

# Define the grid
x = [
    ['R', '#', '#', '.', '.' , '#', '.', '.'],
    ['.', '.', '.', '.', '.' , '#', '.', '.'],
    ['.', '#', '.', '#', '.' , '#', '.', '.'],
    ['.', '#', '.', '#', '.' , '#', '.', '.'],
    ['.', '#', '.', '#', '.' , '.', '.', '.'],
    ['.', '#', '.', '#', '.' , '.', '#', 'C']
]

# Constants
CELL_SIZE = 50  # Size of each cell in pixels
DELAY = 0.5     # Delay between movements in seconds

# Cell colors mapping
CELL_COLORS = {
    '#': 'black',
    'R': 'green',
    'C': 'yellow',
    '.': 'white'
}

def draw_grid(canvas, grid):
    """Draw the grid on the canvas."""
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            color = CELL_COLORS.get(grid[i][j], "white")
            canvas.create_rectangle(
                j * CELL_SIZE, i * CELL_SIZE,
                (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE,
                fill=color, outline="gray"
            )

def animate_movement(canvas, path, start_i, start_j):
    """Animate the rat's movement based on the given path."""
    if not path:
        print("No path found.")
        return

    i, j = start_i, start_j  # Start position
    for move in path:
        time.sleep(DELAY)
        # Clear the previous cell
        canvas.create_rectangle(
            j * CELL_SIZE, i * CELL_SIZE,
            (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE,
            fill="white", outline="gray"
        )
        # Update position
        if move == 'R':
            j += 1
        elif move == 'D':
            i += 1
        elif move == 'L':
            j -= 1
        elif move == 'U':
            i -= 1
        # Draw the rat in the new position
        canvas.create_rectangle(
            j * CELL_SIZE, i * CELL_SIZE,
            (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE,
            fill="blue", outline="gray"
        )
        canvas.update()

def find_start():
    """Find the starting position of 'R' in the grid."""
    for i in range(len(x)):
        for j in range(len(x[i])):
            if x[i][j] == 'R':
                return i, j
    return -1, -1  # If no starting point is found

def find_path(start_i, start_j):
    """Find the shortest path from R to C using BFS."""
    if start_i == -1 or start_j == -1:
        return ""  # Invalid start

    directions = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}
    queue = deque([(start_i, start_j, "")])
    visited = set()

    while queue:
        i, j, path = queue.popleft()
        if (i, j) in visited:
            continue
        visited.add((i, j))

        # Check if we've reached the cheese
        if x[i][j] == 'C':
            return path

        # Explore neighbors
        for move, (di, dj) in directions.items():
            ni, nj = i + di, j + dj
            if 0 <= ni < len(x) and 0 <= nj < len(x[0]) and x[ni][nj] != '#' and (ni, nj) not in visited:
                queue.append((ni, nj, path + move))

    return ""  # No path found

def main():
    # Initialize the GUI
    root = tk.Tk()
    root.title("Rat and Cheese")
    canvas = tk.Canvas(root, width=len(x[0]) * CELL_SIZE, height=len(x) * CELL_SIZE)
    canvas.pack()

    # Draw the initial grid
    draw_grid(canvas, x)

    # Find the starting position of the rat
    start_i, start_j = find_start()

    # Find the path from R to C
    path = find_path(start_i, start_j)
    print(f"Path: {path}")

    # Animate the movement
    root.after(1000, animate_movement, canvas, path, start_i, start_j)

    root.mainloop()

if __name__ == "__main__":
    main()
