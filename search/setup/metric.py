from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SearchMetrics:
    nodes_expanded: int = 0
    nodes_generated: int = 0
    re_expansions: int = 0
    peak_frontier_size: int = 0
    peak_explored_size: int = 0
    peak_stored_nodes: int = 0
    solution_cost: int | None = None
    solution_found: bool = False
    runtime_sec: float = 0.0
    ida_iterations: int = 0
    sma_pruned_nodes: int = 0

    def update_peak_storage(self, frontier_size: int, explored_size: int = 0) -> None:
        self.peak_frontier_size = max(self.peak_frontier_size, frontier_size)
        self.peak_explored_size = max(self.peak_explored_size, explored_size)
        self.peak_stored_nodes = max(
            self.peak_stored_nodes,
            frontier_size + explored_size
        )