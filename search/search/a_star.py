
import heapq
import time
from dataclasses import dataclass, field
from typing import Any

from search.setup.metric import SearchMetrics

@dataclass(order=True)
class PrioritizedNode:
    priority: int
    tie_break: int
    state: Any = field(compare=False)
    path: list = field(compare=False)
    g: int = field(compare=False)


def a_star_search(problem, heuristic):
    metrics = SearchMetrics()
    start_time = time.perf_counter()

    start = problem.get_start_state()
    frontier = []
    counter = 0

    start_h = heuristic(start, problem)
    heapq.heappush(frontier, PrioritizedNode(start_h, counter, start, [], 0))
    counter += 1

    best_g = {start: 0}
    expanded = set()

    while frontier:

        metrics.update_peak_storage(len(frontier), len(expanded))
        node = heapq.heappop(frontier)

        if node.state in expanded:
            metrics.re_expansions += 1
            continue

        if problem.is_goal_state(node.state):
            metrics.solution_found = True
            metrics.solution_cost = node.g
            metrics.runtime_sec = time.perf_counter() - start_time
            return node.path, metrics

        expanded.add(node.state)
        metrics.nodes_expanded += 1

        for succ, action, step_cost in problem.get_successors(node.state):
            metrics.nodes_generated += 1
            new_g = node.g + step_cost

            if succ not in best_g or new_g < best_g[succ]:
                best_g[succ] = new_g
                f = new_g + heuristic(succ, problem)
                heapq.heappush(
                    frontier,
                    PrioritizedNode(f, counter, succ, node.path + [action], new_g)
                )
                counter += 1

    metrics.runtime_sec = time.perf_counter() - start_time
    return None, metrics


