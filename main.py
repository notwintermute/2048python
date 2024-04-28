import time

from algorithms import alphabeta_call, expectimax_call, highest_tile
from grid_2048 import Game


def run_alphabeta(depth):
    curr = time.time()
    game = Game()
    k = 1
    while not game.game_lost():
        k += 1
        if k % 100 == 0:
            print(f"Move {k}")
        m = alphabeta_call(game, depth)
        game.play(m)
    return game.score, highest_tile(game), time.time() - curr, k


def run_alphabeta_increasing(initial_depth, end_depth, margin):
    curr = time.time()
    game = Game()
    k = 1
    d = initial_depth
    while not game.game_lost():
        k += 1
        if k % 100 == 0:
            print(f"Move {k}")
        if k > margin:
            d = end_depth
        m = alphabeta_call(game, d)
        game.play(m)
    return game.score, highest_tile(game), time.time() - curr, k


def run_expectimax(depth):
    curr = time.time()
    game = Game()
    k = 1
    while not game.game_lost():
        k += 1
        if k % 100 == 0:
            print(f"Move {k}")
        m = expectimax_call(game, depth)
        game.play(m)
    return game.score, highest_tile(game), time.time() - curr, k

def run_expectimax_increasing(initial_depth, end_depth, margin):
    curr = time.time()
    game = Game()
    k = 1
    d = initial_depth
    while not game.game_lost():
        k += 1
        if k % 100 == 0:
            print(f"Move {k}")
        if k > margin:
            d = end_depth
        m = expectimax_call(game, d)
        game.play(m)
    return game.score, highest_tile(game), time.time() - curr, k
def parse_results(r):
    scores = []
    highest = []
    times = []
    moves = []
    for i in range(len(r)):
        scores.append(r[i][0])
        highest.append(r[i][1])
        times.append(r[i][2])
        moves.append(r[i][3])
    print("Scores")
    for s in scores:
        print(s, end=" ")
    print()
    print("Highest")
    for h in highest:
        print(h, end=" ")
    print()
    print("Times")
    for t in times:
        print(t, end=" ")
    print()
    print("Moves")
    for m in moves:
        print(m, end=" ")


if 1 > 0:  # Run 100
    results = []
    for x in range(100):
        print(f"Game {x + 1}")
        results.append(run_expectimax_increasing(2,3,700))
    parse_results(results)
