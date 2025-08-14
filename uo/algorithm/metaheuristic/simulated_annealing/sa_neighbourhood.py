""" 
The :mod:`~uo.algorithm.metaheuristic.simulated_annealing.sa_neighbourhood` module describes the class :class:`~uo.algorithm.metaheuristic.simulated_annealing.sa_neighbourhood.SaNeighbourhood`.
"""

from pathlib import Path
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)

from uo.solution.solution import Solution
from abc import ABC, abstractmethod

class SaNeighbourhood(ABC):
    """
    Abstract base class for Simulated Annealing neighbourhood structures.
    Subclasses must implement the generate_neighbor method.
    """
    @abstractmethod
    def generate_neighbor(self, solution: Solution, problem) -> Solution:
        """
        Generate a neighbor solution for the given solution and problem.
        Must be implemented by subclasses.
        """
        pass
