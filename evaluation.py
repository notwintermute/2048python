from math import log2


# eval function

# following monotonicity code taken from 6502 on StackOverflow
# https://stackoverflow.com/questions/4983258/check-list-monotonicity
def non_decreasing(L):
    return all(x <= y for x, y in zip(L, L[1:]))


def non_increasing(L):
    return all(x >= y for x, y in zip(L, L[1:]))


def monotonic(L):
    return non_decreasing(L) or non_increasing(L)


# Eval Function
def evaluation(active_game):
    # lost game check
    if active_game.game_lost():
        return -100000

    grid = active_game.board
    # raw game score
    score = log2(active_game.score + 1)

    # highest tile
    highest = 0
    for i in range(4):
        for j in range(4):
            if grid[i][j] > highest:
                highest = grid[i][j]

    # monotonicity
    monotonicity_hor = 0  # horizontal monotonicity
    monotonicity_ver = 0  # vertical monotonicity
    monotonicity_snake = 0  # "snake" shape
    # horizontal
    for i in range(4):
        if monotonic(grid[i]):
            monotonicity_hor += 1
    # vertical
    rotated = active_game.rotate()
    for i in range(4):
        if monotonic(rotated[i]):
            monotonicity_ver += 1
    # snake
    snakes = [grid[0] + grid[1][::-1] + grid[2] + grid[3][::-1],
              rotated[0] + rotated[1][::-1] + rotated[2] + rotated[3][::-1],
              grid[0][::-1] + grid[1] + grid[2][::-1] + grid[3],
              rotated[0][::-1] + rotated[1] + rotated[2][::-1] + rotated[3]]
    for i in range(4):
        if monotonic(snakes[i]):
            monotonicity_snake += 1

    # empty tiles (this encourages merges)
    empty = 0
    for i in range(4):
        for j in range(4):
            if active_game.board[i][j] == 0:
                empty += 1

    # collect results in an array
    resultant_eval = [score, highest, 3 ** monotonicity_hor, 3 ** monotonicity_ver, 4 ** monotonicity_snake, 12 * empty]
    return sum(resultant_eval)


if __name__ == "__main__":
    from grid_2048 import Game

    game = Game()
    game.board = [[0, 2, 4, 8],
                  [0, 2, 4, 8],
                  [0, 2, 4, 8],
                  [0, 2, 4, 8]]
    # noinspection PyTypeChecker
    print("Test 1 :", evaluation(game))
    game.board = [[8, 4, 2, 0],
                  [8, 4, 2, 0],
                  [8, 4, 2, 0],
                  [8, 4, 2, 0]]
    # noinspection PyTypeChecker
    print("Test 2 :", evaluation(game))
