
import time

from search.setup.metric import SearchMetrics

class SMANode:
    def __init__(self, state, parent, action, g, h):
        self.state = state
        self.parent = parent
        self.action = action

        self.g = g
        self.h = h
        self.f = g + h

        self.children = []
        self.forgotten_f = float('inf')

    def is_leaf(self):
        return len(self.children) == 0

    def path(self):
        actions = []
        node = self
        while node.parent is not None:
            actions.append(node.action)
            node = node.parent
        return list(reversed(actions))

def sma_star_search(problem, heuristic, memory_limit=1000, cutoff=5):
    metrics = SearchMetrics()
    start_time = time.perf_counter()

    start = problem.get_start_state()
    root = SMANode(start, None, None, 0, heuristic(start, problem))

    frontier = [root]

    while frontier:

        # cutoff
        if time.perf_counter() - start_time > cutoff:
            return None, metrics

        # select best (lowest f, deepest)
        node = min(frontier, key=lambda n: (n.f, -n.g))

        if problem.is_goal_state(node.state):
            metrics.solution_found = True
            metrics.solution_cost = node.g
            metrics.runtime_sec = time.perf_counter() - start_time
            return node.path(), metrics

        frontier.remove(node)
        metrics.nodes_expanded += 1

        successors = problem.get_successors(node.state)

        if not successors:
            node.f = float('inf')
            backup(node)
            continue

        for succ, action, cost in successors:
            metrics.nodes_generated += 1

            g_val = node.g + cost
            h_val = heuristic(succ, problem)

            child_f = max(node.f, g_val + h_val)  #pathmax

            child = SMANode(succ, node, action, g_val, h_val)
            child.f = child_f

            node.children.append(child)
            frontier.append(child)

        # memory pruning
        while len(frontier) > memory_limit:
            worst = max(frontier, key=lambda n: (n.f, -n.g))

            frontier.remove(worst)
            metrics.sma_pruned_nodes += 1

            parent = worst.parent
            if parent:
                parent.children.remove(worst)
                parent.forgotten_f = min(parent.forgotten_f, worst.f)

                if len(parent.children) == 0:
                    frontier.append(parent)

                backup(parent)

    return None, metrics

def backup(node):
    while node.parent is not None:
        parent = node.parent

        child_f_values = [child.f for child in parent.children]
        if parent.forgotten_f != float('inf'):
            child_f_values.append(parent.forgotten_f)

        parent.f = max(parent.g + parent.h, min(child_f_values))

        node = parent
