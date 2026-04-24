import random

from search.setup.eight_puzzle_benchmark import EightPuzzleState, EightPuzzleProblem, manhattan_heuristic
from search.search.a_star import a_star_search

OPPOSITE_MOVE = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT",
}


def scramble_from_goal(depth, seed=None):
    rng = random.Random(seed)
    state = EightPuzzleState((1, 2, 3, 4, 5, 6, 7, 8, 0))

    prev_move = None

    for _ in range(depth):
        legal = state.legal_moves()

        if prev_move is not None:
            opposite = OPPOSITE_MOVE[prev_move]
            legal = [m for m in legal if m != opposite]

        move = rng.choice(legal)
        state = state.result(move)
        prev_move = move

    return state


def generate_exact_depth_instances(depth, n):
    instances = []
    trial = 0

    while len(instances) < n:
        state = scramble_from_goal(depth, seed=trial)
        trial += 1

        problem = EightPuzzleProblem(state)
        _, metrics = a_star_search(problem, manhattan_heuristic)

        if metrics.solution_cost == depth:
            instances.append(state)

    return instances
