from setup.benchmark_problem import SearchProblem


class EightPuzzleState:
    def __init__(self, tiles):
        """
        tiles: tuple of length 9, using 0 for blank
        goal: (1,2,3,4,5,6,7,8,0)
        """
        self.tiles = tuple(tiles)
        self.blank_idx = self.tiles.index(0)

    def is_goal(self):
        return self.tiles == (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def legal_moves(self):
        row, col = divmod(self.blank_idx, 3)
        moves = []

        if row > 0:
            moves.append("UP")
        if row < 2:
            moves.append("DOWN")
        if col > 0:
            moves.append("LEFT")
        if col < 2:
            moves.append("RIGHT")

        return moves

    def result(self, move):
        row, col = divmod(self.blank_idx, 3)

        if move == "UP":
            new_row, new_col = row - 1, col
        elif move == "DOWN":
            new_row, new_col = row + 1, col
        elif move == "LEFT":
            new_row, new_col = row, col - 1
        elif move == "RIGHT":
            new_row, new_col = row, col + 1
        else:
            raise ValueError(f"Illegal move: {move}")

        new_blank_idx = new_row * 3 + new_col
        new_tiles = list(self.tiles)
        new_tiles[self.blank_idx], new_tiles[new_blank_idx] = (
            new_tiles[new_blank_idx],
            new_tiles[self.blank_idx],
        )
        return EightPuzzleState(tuple(new_tiles))

    def __hash__(self):
        return hash(self.tiles)

    def __eq__(self, other):
        return isinstance(other, EightPuzzleState) and self.tiles == other.tiles

    def __repr__(self):
        return f"EightPuzzleState({self.tiles})"


class EightPuzzleProblem(SearchProblem):
    def __init__(self, start_state):
        self.start_state = start_state

    def get_start_state(self):
        return self.start_state

    def is_goal_state(self, state):
        return state.is_goal()

    def get_successors(self, state):
        successors = []
        for move in state.legal_moves():
            successors.append((state.result(move), move, 1))
        return successors

    def get_cost_of_actions(self, actions):
        return len(actions)


def manhattan_heuristic(state, problem=None):
    total = 0
    for idx, tile in enumerate(state.tiles):
        if tile == 0:
            continue
        goal_idx = tile - 1
        r1, c1 = divmod(idx, 3)
        r2, c2 = divmod(goal_idx, 3)
        total += abs(r1 - r2) + abs(c1 - c2)
    return total


def misplaced_tiles_heuristic(state, problem=None):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    return sum(
        1
        for i, tile in enumerate(state.tiles)
        if tile != 0 and tile != goal[i]
    )

def state_to_base9_fraction(state):
    """
    Convert state into a small fractional number in base 9
    Example from paper:
    (1 0 3 4 5 6 7 8 2) -> 0.103456782 (base 9)
    """
    frac = 0.0
    base = 9
    for i, tile in enumerate(state.tiles):
        frac += tile / (base ** (i + 1))
    return frac

def perturbed_manhattan_heuristic(state, problem=None):
    h = manhattan_heuristic(state, problem)

    if h == 0:
        return 0  # goal state

    eps = state_to_base9_fraction(state)
    b = 9

    perturb = (1 - eps * (h ** 2)) / (h * (b + 1))

    return h + perturb