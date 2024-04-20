# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import random

empty = '.'
full = 'x'
directions = (
    (0, 1),  # Right
    (0, -1), # Left
    (1, 0),  # Up
    (-1, 0), # Down
)
MIN_SIZE = 3
MAX_SIZE = 5

def print_board():
    board, ships = generate_board(10, 4)
    for row in board:
        print(' '.join(row))

def generate_board(board_size, n_ships):
    board = [[empty] * board_size for _ in range(board_size)]
    ships = []
    while len(ships) < n_ships:
        row = random.randint(0, board_size - 1)
        col = random.randint(0, board_size - 1)
        direction = random.choice(directions)
        ship_size = random.randint(MIN_SIZE, MAX_SIZE)
        ship = generate_ship(board, row, col, ship_size, direction)
        if ship:
            ships.append(ship)
            for r, c in ship:
                board[r][c] = full
    return (board, ships)

def generate_ship(board, row, col, ship_size, direction):
    r = row
    c = col
    dr, dc = direction
    cells = []
    for _ in range(ship_size):
        if is_empty(board, r, c):
            cells.append((r, c))
            r += dr
            c += dc
        else:
            return None
    return cells

def is_empty(board, row, col):
    try:
        return min(row, col) >= 0 and board[row][col] == empty
    except IndexError:
        pass
    return False

if __name__ == "__main__":
    print_board()
