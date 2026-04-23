from abc import ABC, abstractmethod
from typing import Any, Iterable, Tuple


class SearchProblem(ABC):
    @abstractmethod
    def get_start_state(self) -> Any:
        pass

    @abstractmethod
    def is_goal_state(self, state: Any) -> bool:
        pass

    @abstractmethod
    def get_successors(self, state: Any) -> Iterable[Tuple[Any, str, int]]:
        """
        Returns iterable of:
        (successor_state, action, step_cost)
        """
        pass

    @abstractmethod
    def get_cost_of_actions(self, actions) -> int:
        pass