import random

class Player:
    def __init__(self, name):
        self.name = name

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['O' for _ in range(size)] for _ in range(size)]

    def display(self, hide_ships=False):
        print("  " + " ".join([str(i) for i in range(self.size)]))
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                if self.grid[i][j] == 'S' and hide_ships:
                    row += 'O '
                else:
                    row += self.grid[i][j] + ' '
            print(str(i) + " " + row)

    def place_ship(self, ship_size, row, col, orientation):
        if orientation == 'h':
            for i in range(ship_size):
                self.grid[row][col + i] = 'S'
        else:
            for i in range(ship_size):
                self.grid[row + i][col] = 'S'

    def check_collision(self, row, col, ship_size, orientation):
        if orientation == 'h':
            for i in range(ship_size):
                if self.grid[row][col + i] == 'S':
                    return True
        else:
            for i in range(ship_size):
                if self.grid[row + i][col] == 'S':
                    return True
        return False

class Game:
    def __init__(self, size=10, num_ships=5):
        self.size = size
        self.num_ships = num_ships
        self.player_board = Board(size)
        self.computer_board = Board(size)
        self.player = Player("Player")
        self.computer = Player("Computer")
        self.ships = [5, 4, 3, 3, 2]

    def start(self):
        print("Welcome to Battleship!")
        self.player.name = input("Enter your name: ")

        print("\n{}'s turn to place ships:".format(self.player.name))
        self.place_all_ships(self.player_board)

        self.place_all_ships_randomly(self.computer_board)

        self.play()

    def place_all_ships(self, board):
        for ship_size in self.ships:
            print("\nPlacing ship of size:", ship_size)
            board.display()
            while True:
                try:
                    orientation = input("Enter orientation (h for horizontal, v for vertical): ").lower()
                    if orientation not in ['h', 'v']:
                        raise ValueError("Invalid orientation! Please enter 'h' or 'v'.")
                    row = int(input("Enter row (0-{}): ".format(self.size - 1)))
                    col = int(input("Enter column (0-{}): ".format(self.size - 1)))
                    if not (0 <= row < self.size) or not (0 <= col < self.size):
                        raise ValueError("Invalid position! Please enter valid coordinates.")
                    if orientation == 'h' and col + ship_size > self.size:
                        raise ValueError("Invalid position! Ship doesn't fit horizontally.")
                    if orientation == 'v' and row + ship_size > self.size:
                        raise ValueError("Invalid position! Ship doesn't fit vertically.")
                    if board.check_collision(row, col, ship_size, orientation):
                        raise ValueError("Invalid position! Ships overlap.")
                    board.place_ship(ship_size, row, col, orientation)
                    break
                except ValueError as e:
                    print(e)
            board.display()

    def place_all_ships_randomly(self, board):
        for ship_size in self.ships:
            while True:
                orientation = random.choice(['h', 'v'])
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 1)
                if orientation == 'h' and col + ship_size <= self.size:
                    if not board.check_collision(row, col, ship_size, orientation):
                        break
                elif orientation == 'v' and row + ship_size <= self.size:
                    if not board.check_collision(row, col, ship_size, orientation):
                        break
            board.place_ship(ship_size, row, col, orientation)

    def player_turn(self):
        print("\n{}'s turn:".format(self.player.name))
        self.computer_board.display(hide_ships=True)
        while True:
            try:
                guess_row = int(input("Enter row to attack (0-{}): ".format(self.size - 1)))
                guess_col = int(input("Enter column to attack (0-{}): ".format(self.size - 1)))
                if not (0 <= guess_row < self.size) or not (0 <= guess_col < self.size):
                    raise ValueError("Invalid guess! Please enter valid coordinates.")
                if self.computer_board.grid[guess_row][guess_col] in ['X', '*']:
                    print("You've already attacked this position! Guess again.")
                    continue
                break
            except ValueError as e:
                print(e)
        if self.computer_board.grid[guess_row][guess_col] == 'S':
            print("Hit!")
            self.computer_board.grid[guess_row][guess_col] = 'X'
        else:
            print("Miss!")
            self.computer_board.grid[guess_row][guess_col] = '*'

    def computer_turn(self):
        print("\nComputer's turn:")
        while True:
            guess_row = random.randint(0, self.size - 1)
            guess_col = random.randint(0, self.size - 1)
            if self.player_board.grid[guess_row][guess_col] in ['X', '*']:
                continue
            break

        if self.player_board.grid[guess_row][guess_col] == 'S':
            print("Computer hit at ({}, {})!".format(guess_row, guess_col))
            self.player_board.grid[guess_row][guess_col] = 'X'
        else:
            print("Computer missed at ({}, {})!".format(guess_row, guess_col))
            self.player_board.grid[guess_row][guess_col] = '*'

    def check_winner(self):
        if all('S' not in row for row in self.computer_board.grid):
            return self.player.name
        elif all('S' not in row for row in self.player_board.grid):
            return self.computer.name
        else:
            return None

    def play(self):
        while True:
            self.player_turn()
            winner = self.check_winner()
            if winner:
                print("\nCongratulations {}! You've won!".format(winner))
                break

            self.computer_turn()
            winner = self.check_winner()
            if winner:
                print("\n{} has won! Better luck next time.".format(winner))
                break

if __name__ == "__main__":
    game = Game()
    game.start()
