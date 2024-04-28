from copy import deepcopy
from evaluation import evaluation
import statistics
import time


def highest_tile(state):
    grid = state.board
    high = 0
    for i in range(4):
        for j in range(4):
            if grid[i][j] > high:
                high = grid[i][j]
    return high


# returns possible states after a move as a list of 2d lists
def possible_responses(state):
    poss = []
    for i in range(4):
        for j in range(4):
            if state.board[i][j] == 0:
                newstate_2 = deepcopy(state)
                newstate_4 = deepcopy(state)
                newstate_2.board[i][j] = 2
                newstate_4.board[i][j] = 4
                poss.append(newstate_2)
                # poss.append(newstate_4)

    return poss


def possible_moves(state):
    moves = ["l", "d", "r", "u"]
    return [move for move in moves if state.check_valid(move)]


def minimax(state, depth, waiting_for_move=True):
    if depth < 1 or state.game_lost():
        return evaluation(state)

    if waiting_for_move:
        value = -1000000000
        valid = possible_moves(state)
        for move in valid:
            future = state.future(move)
            value = max(value, minimax(future, depth - 1, False))

    else:
        value = 1000000000
        possible = possible_responses(state)
        for poss in possible:
            value = min(value, minimax(poss, depth - 1))

    return value


def alphabeta(state, depth, alpha, beta, waiting_for_move=True):
    if depth == 0 or state.game_lost():
        return evaluation(state)

    if waiting_for_move:
        value = -1000000000
        valid = possible_moves(state)
        for move in valid:
            future = state.future(move)
            value = max(value, alphabeta(future, depth - 1, alpha, beta, False))
            if value > beta:
                return value
            alpha = max(alpha, value)
    else:
        value = 1000000000
        for i in range(4):
            for j in range(4):
                if state.board[i][j] == 0:
                    newstate_2 = deepcopy(state)
                    # newstate_4 = deepcopy(state)
                    newstate_2.board[i][j] = 2
                    # if newstate_2.game_lost():
                    # return value
                    # newstate_4.board[i][j] = 4
                    value = min(value, alphabeta(newstate_2, depth - 1, alpha, beta))
                    if value < alpha:
                        return value
                    beta = min(beta, value)

    return value


def expectimax(state, depth, waiting_for_move=True):
    if depth == 0 or state.game_lost():
        return evaluation(state)
    if waiting_for_move:
        value = -1000000000
        valid = possible_moves(state)
        for move in valid:
            future = state.future(move)
            value = max(value, expectimax(future, depth - 1, False))
        return value
    else:
        expectedvalue = 0
        for i in range(4):
            for j in range(4):
                if state.board[i][j] == 0:
                    newstate_2 = deepcopy(state)
                    newstate_4 = deepcopy(state)
                    newstate_2.board[i][j] = 2
                    newstate_4.board[i][j] = 4
                    expectedvalue += expectimax(newstate_2, depth - 1) * 0.9
                    expectedvalue += expectimax(newstate_4, depth - 1) * 0.1
        return expectedvalue


def minimax_call(state, depth):
    valid = possible_moves(state)
    evals = []
    for index, move in enumerate(valid):
        future = state.future(move)
        evals.append(minimax(future, depth, False))
    return valid[evals.index(max(evals))]


def alphabeta_call(state, depth):
    valid = possible_moves(state)
    evals = []
    for index, move in enumerate(valid):
        future = state.future(move)
        evals.append(alphabeta(future, depth, -1000000000, 1000000000, False))
    return valid[evals.index(max(evals))]


def expectimax_call(state, depth):
    valid = possible_moves(state)
    evals = []
    for index, move in enumerate(valid):
        future = state.future(move)
        evals.append(expectimax(future, depth, False))
    return valid[evals.index(max(evals))]


if __name__ == "__main__":
    from grid_2048 import Game

    tests = [False, False, False, False, False, False, False, False, False, False, True]
    game = Game()

    if tests[0]:
        game.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        print("1. Possible Responses (Empty Grid)")
        print("Expected : 32 | Actual :", len(possible_responses(game)))

    if tests[1]:
        game.board = [[0, 0, 0, 0],
                      [0, 2, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        print("2. Possible Moves (2 in upper left center)")
        print("Expected : ['l', 'd', 'r', 'u'] | Actual :", possible_moves(game))

    if tests[2]:
        game.board = [[2, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        print("3. Possible Moves (2 in upper left corner)")
        print("Expected : ['d', 'r'] | Actual :", possible_moves(game))

    if tests[3]:
        game = Game()
        game.board = [[128, 0, 0, 0],
                      [128, 0, 0, 0],
                      [2, 0, 0, 0],
                      [0, 0, 0, 0]]
        game.score = 1220

        print("4. Minimax test with Depth 1-6")
        for x in range(4):
            print(minimax_call(game, x))

    if tests[4]:
        print("5. Alphabeta test with Depth 1-6")
        for x in range(4):
            print(alphabeta_call(game, x))

    if tests[5]:
        print("6. Ten runs with minimax Depth 1")
        scores = []
        highest = []
        for x in range(10):
            game = Game()
            k = 1
            print(f"Game {x + 1}")
            while not game.game_lost():
                if k % 100 == 0:
                    print(f"Move {k}")
                k += 1
                m = minimax_call(game, 1)
                game.play(m)
            print(game.score)
            scores.append(game.score)
            highest.append(highest_tile(game))
        print(scores)
        print(highest)

    if tests[6]:
        print("7. Ten runs with alphabeta Depth 4")
        scores = []
        highest = []
        for x in range(5):
            game = Game()
            k = 1
            print(f"Game {x + 1}")
            while not game.game_lost():
                if k % 100 == 0:
                    print(f"Move {k}")
                k += 1
                m = alphabeta_call(game, 3)
                game.play(m)
            print(game.score)
            scores.append(game.score)
            highest.append(highest_tile(game))
        print(f"Scores: {scores}\nMean: {statistics.mean(scores)}\nStdDev: {statistics.stdev(scores)}")
        print()
        print(f"Highest Tiles: {highest}\nMean: {statistics.mean(highest)}\nStdDev: {statistics.stdev(highest)}")

    if tests[7]:
        print("8. Timing Minimax")
        for d in range(4):
            times = []
            for x in range(5):
                game = Game()
                curr = time.time()
                while not game.game_lost():
                    m = minimax_call(game, d)
                    game.play(m)
                times.append(time.time() - curr)
            print(f"Depth {d}: {statistics.mean(times)} seconds")

    if tests[8]:
        print("9. Timing Alphabeta")
        for d in range(5):
            times = []
            for x in range(10):
                game = Game()
                curr = time.time()
                while not game.game_lost():
                    m = alphabeta_call(game, d)
                    game.play(m)
                times.append(time.time() - curr)
            print(f"Depth {d}: {statistics.mean(times)} seconds")

    if tests[9]:
        print("10. Comparing Single Alphabeta vs Minimax Calls with Depth 6")
        game = Game()
        curr = time.time()
        minimax_call(game, 1)
        print(f"Minimax : {(time.time() - curr) * 500 * 1000 / 60} seconds")
        curr = time.time()
        alphabeta_call(game, 4)
        print(f"Alphabeta : {(time.time() - curr) * 500 * 1000 / 60} seconds")

    if tests[10]:
        print("11. Expectimax Single Move Timing Depth 0-4")
        for d in range(5):
            times = []
            for x in range(1):
                game = Game()
                curr = time.time()
                expectimax_call(game, d)
                times.append(time.time() - curr)
            print(f"Depth {d}: {statistics.mean(times)*1000*100} seconds")
