
import heapq
import time
from dataclasses import dataclass, field
from typing import Any

from setup.metric import SearchMetrics


def ida_star_search(problem, heuristic):
    metrics = SearchMetrics()
    start_time = time.perf_counter()

    start = problem.get_start_state()
    bound = heuristic(start, problem)

    path = [(start, [], 0)]  # (state, path, g)

    metrics.ida_iterations = 0

    while True:
        visited = set([start])
        metrics.ida_iterations += 1

        t = _ida_dfs(problem, heuristic, path, bound, visited, metrics)

        if isinstance(t, tuple):  # found solution
            solution_path, cost = t
            metrics.solution_found = True
            metrics.solution_cost = cost
            metrics.runtime_sec = time.perf_counter() - start_time
            return solution_path, metrics

        if t == float('inf'):  # no solution
            metrics.runtime_sec = time.perf_counter() - start_time
            return None, metrics

        bound = t  # increase threshold


def _ida_dfs(problem, heuristic, path, bound, visited, metrics):
    state, actions, g = path[-1]

    f = g + heuristic(state, problem)
    if f > bound:
        return f

    if problem.is_goal_state(state):
        return actions, g

    min_threshold = float('inf')

    metrics.nodes_expanded += 1

    for succ, action, cost in problem.get_successors(state):
        metrics.nodes_generated += 1

        if succ in visited:
            continue

        visited.add(succ)
        path.append((succ, actions + [action], g + cost))

        result = _ida_dfs(problem, heuristic, path, bound, visited, metrics)

        if isinstance(result, tuple):
            return result

        if result < min_threshold:
            min_threshold = result

        path.pop()
        visited.remove(succ)

    return min_threshold
