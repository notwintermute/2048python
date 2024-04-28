from copy import deepcopy
from random import randint


# This organizes the game grid (and score)
class Game:
    def __init__(self, spawn2=True):
        self.score = 0
        # 4x4 array of numbers
        self.board = []
        for i in range(4):
            self.board.append([])
            for j in range(4):
                self.board[i].append(0)
        # place two starting tiles randomly
        if spawn2:
            self.spawn_new_tile()
            self.spawn_new_tile()

    # generating a new tile
    def spawn_new_tile(self):
        not_placed = True
        while not_placed:  # find an empty square
            r = randint(0, 3)  # row
            c = randint(0, 3)  # column
            if self.board[r][c] == 0:
                not_placed = False
                # 10% chance of a 4
                choice = randint(1, 10)
                if choice == 10:
                    self.board[r][c] = 4
                else:
                    self.board[r][c] = 2

    # check if the game is lost
    def game_lost(self):
        # check if there's an empty tile
        # if there's an empty tile it's not lost
        # technically redundant with check_valid
        # but this saves a lot of time
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return False
        # then check if there's a valid move
        if self.check_valid("l") or self.check_valid("r") or self.check_valid("u") or self.check_valid("d"):
            return False
        # if there is no valid move then the game is lost
        return True

    # returns what the grid looks like after a move
    def future(self, move):
        # create a new grid that is a *deepcopy* of the current one
        future = Game()
        future.board = deepcopy(self.board)
        # we then attempt the move on the copy
        if move == "l":
            future.move_left()
        elif move == "r":
            future.move_right()
        elif move == "u":
            future.move_up()
        elif move == "d":
            future.move_down()
        else:
            raise Exception("Invalid move inputted to future()")
        return future

    # check if a move is valid (does anything)
    def check_valid(self, move):
        # if they're equal then the move didn't do anything
        return not (self.board == self.future(move).board)

    # Here are the movement functions
    # these are all basically the same:
    # combine the tiles and then move them to the side
    # there are some cases we have to keep in mind
    # moving left with [2, 2, 2, 0] should give [4, 2, 0, 0]
    # moving left with [2, 2, 2, 2] should give [4, 4, 0, 0]
    # we add the value of the new tiles to the score
    # this holds for every direction
    # move left
    def move_left(self):
        # combine tiles
        for i in range(4):
            for j in range(3):
                curr = self.board[i][j]
                n = 1
                while j + n <= 3:
                    if self.board[i][j + n] == 0:
                        n += 1
                    elif self.board[i][j + n] == curr:
                        self.board[i][j] *= 2
                        self.score += self.board[i][j]
                        self.board[i][j + n] = 0
                        n += 4
                    else:
                        n += 4

        # move tiles over
        for i in range(4):
            for j in range(3):
                if self.board[i][j] == 0:
                    n = 1
                    while j + n <= 3:
                        if self.board[i][j + n] == 0:
                            n += 1
                        else:
                            self.board[i][j] = self.board[i][j + n]
                            self.board[i][j + n] = 0
                            n += 4

    # move right
    def move_right(self):
        # combine tiles
        for i in range(4):
            for j in range(3, 0, -1):
                curr = self.board[i][j]
                n = 1
                while j - n >= 0:
                    if self.board[i][j - n] == 0:
                        n += 1
                    elif self.board[i][j - n] == curr:
                        self.board[i][j] *= 2
                        self.score += self.board[i][j]
                        self.board[i][j - n] = 0
                        n += 4
                    else:
                        n += 4

        # move tiles over
        for i in range(4):
            for j in range(3, 0, -1):
                if self.board[i][j] == 0:
                    n = 1
                    while j - n >= 0:
                        if self.board[i][j - n] == 0:
                            n += 1
                        else:
                            self.board[i][j] = self.board[i][j - n]
                            self.board[i][j - n] = 0
                            n += 4

    # move up
    def move_up(self):
        # combine tiles
        for i in range(3, 0, -1):
            for j in range(4):
                curr = self.board[i][j]
                n = 1
                while i - n >= 0:
                    if self.board[i - n][j] == 0:
                        n += 1
                    elif self.board[i - n][j] == curr:
                        self.board[i - n][j] *= 2
                        self.score += self.board[i - n][j]
                        self.board[i][j] = 0
                        n += 4
                    else:
                        n += 4

        # move tiles over
        for i in range(3):
            for j in range(4):
                if self.board[i][j] == 0:
                    n = 1
                    while i + n <= 3:
                        if self.board[i + n][j] == 0:
                            n += 1
                        else:
                            self.board[i][j] = self.board[i + n][j]
                            self.board[i + n][j] = 0
                            n += 4

    # move down
    def move_down(self):
        # combine tiles
        for i in range(3):
            for j in range(4):
                curr = self.board[i][j]
                n = 1
                while i + n <= 3:
                    if self.board[i + n][j] == 0:
                        n += 1
                    elif self.board[i + n][j] == curr:
                        self.board[i + n][j] *= 2
                        self.score += self.board[i + n][j]
                        self.board[i][j] = 0
                        n += 4
                    else:
                        n += 4

        # move tiles over
        for i in range(3, 0, -1):
            for j in range(4):
                if self.board[i][j] == 0:
                    n = 1
                    while i - n >= 0:
                        if self.board[i - n][j] == 0:
                            n += 1
                        else:
                            self.board[i][j] = self.board[i - n][j]
                            self.board[i - n][j] = 0
                            n += 4

    # this is the actual "play this move" function
    # do move, add new tile, display, check and print if lost
    def play(self, move, newtile=True):
        # this is important cause an invalid move
        # should not spawn a tile
        if not self.check_valid(move):
            raise Exception(f"Can not play {move}")

        if move == "l":
            self.move_left()
        elif move == "r":
            self.move_right()
        elif move == "u":
            self.move_up()
        elif move == "d":
            self.move_down()
        else:
            raise Exception("Invalid move inputted to play()")

        if newtile:
            self.spawn_new_tile()

    # return an array that is the game grid rotated 90 degrees cw
    def rotate(self):
        return list(zip(*self.board[::-1]))

    # this is how we print the grid
    def __repr__(self):
        return str(self.board[0]) + "\n" + str(self.board[1]) + "\n" + str(self.board[2]) + "\n" + str(self.board[3])

    def display(self):
        print(self)
        print(self.score)


if __name__ == '__main__':
    game = Game()
    game.play("l")
    game.display()
    if False:
        game = Game()
        move_dict = {"l": "Left", "r": "Right", "u": "Up", "d": "Down"}
        moves = ["l", "d", "r", "u"]
        k = 0
        while not game.game_lost():
            k += 1
            m = moves[k % 4]  # play l r u d repeatedly
            if game.check_valid(m):
                print(f"Moved {move_dict[m]}")
                game.play(m)
                game.display()
