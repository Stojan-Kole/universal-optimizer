"""
The :mod:`~uo.algorithm.metaheuristic.simulated_annealing.sa_neighbourhood_int` contains 
class :class:`~uo.algorithm.metaheuristic.simulated_annealing.sa_neighbourhood_int.SaNeighbourhoodInt`, 
that represents Simulated Annealing neighbourhood support for integer-encoded solutions.
"""

import random
from copy import deepcopy
from uo.algorithm.metaheuristic.simulated_annealing.sa_neighbourhood import SaNeighbourhood
from uo.solution.solution import Solution
from uo.problem.problem import Problem

class SaNeighbourhoodInt(SaNeighbourhood):
    """
    Neighbourhood structure for integer solutions for Simulated Annealing.
    Generates a neighbor by flipping k random bits in the integer representation,
    similar to VNS shaking.
    """
    def __init__(self, dimension: int, k: int = 1) -> None:
        """
        :param dimension: Number of bits in the solution representation.
        :param k: Number of bits to flip in the neighbor (default 1 for SA).
        """
        self.dimension = dimension
        self.k = k

    def __copy__(self):
        return deepcopy(self)

    def copy(self):
        return self.__copy__()

    def generate_neighbor(self, solution: Solution, problem: Problem, optimizer=None) -> Solution:
        """
        Generate a neighbor by flipping k random bits in the integer representation.
        Optionally supports optimizer hooks for output/evaluation.
        """
        tries = 0
        limit = 10000

        while tries < limit:
            neighbor = solution.copy()
            positions = [random.choice(range(self.dimension)) for _ in range(self.k)]
            mask = 0
            for p in positions:
                mask |= 1 << p
            neighbor.representation ^= mask
            # Optional: check if bit count is valid (as in VNS)
            if neighbor.representation.bit_count() > self.dimension:
                tries += 1
                continue
            if optimizer is not None:
                if hasattr(optimizer, "write_output_values_if_needed"):
                    optimizer.write_output_values_if_needed("before_evaluation", "b_e")
            neighbor.evaluate(problem)
            if optimizer is not None:
                if hasattr(optimizer, "evaluation"):
                    optimizer.evaluation += 1
                if hasattr(optimizer, "write_output_values_if_needed"):
                    optimizer.write_output_values_if_needed("after_evaluation", "a_e")
            return neighbor
        # If no valid neighbor found, return a copy of the original
        return solution.copy()

    def string_rep(self, delimiter: str, indentation: int = 0, indentation_symbol: str = '', group_start: str = '{',
                  group_end: str = '}') -> str:
        """
        String representation of the SA neighbourhood instance.
        """
        return f'SaNeighbourhoodInt{group_start}dimension={self.dimension}{delimiter}k={self.k}{group_end}'

    def __str__(self) -> str:
        return self.string_rep('|')

    def __repr__(self) -> str:
        return self.string_rep('\n')

    def __format__(self, spec: str) -> str:
        return self.string_rep('|')