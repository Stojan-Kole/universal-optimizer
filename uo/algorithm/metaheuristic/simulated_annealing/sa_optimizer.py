"""
..  _py_sa_optimizer:

The :mod:`~uo.algorithm.metaheuristic.simulated_annealing.simulated_annealing` contains class :class:`~.uo.metaheuristic.simulated_annealing.simulated_annealing.SaOptimizer`, that represents implements algorithm :ref:`SA<Algorithm_Simulated_Annealing>`.
"""

from pathlib import Path

directory = Path(__file__).resolve()

import sys
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)

from dataclasses import dataclass

from typing import Optional

from uo.problem.problem import Problem
from uo.solution.solution import Solution

from uo.algorithm.output_control import OutputControl
from uo.algorithm.metaheuristic.finish_control import FinishControl
from uo.algorithm.metaheuristic.additional_statistics_control import AdditionalStatisticsControl
from uo.algorithm.metaheuristic.simulated_annealing.sa_temperature import SaTemperature

from uo.algorithm.metaheuristic.single_solution_metaheuristic import SingleSolutionMetaheuristic

from uo.algorithm.metaheuristic.simulated_annealing.sa_neighbourhood import SaNeighbourhood

import random
import math

@dataclass
class SaOptimizerConstructionParameters:
    """
        Instance of the class :class:`~uo.algorithm.metaheuristic.simulated_annealing_constructor_parameters.
        SaOptimizerConstructionParameters` represents constructor parameters for SA algorithm.
    """
    sa_neighbourhood: SaNeighbourhood = None
    sa_temperature: SaTemperature = None
    finish_control: Optional[FinishControl] = None
    problem: Problem = None
    solution_template: Optional[Solution] = None
    output_control: Optional[OutputControl] = None
    random_seed: Optional[int] = None
    additional_statistics_control: Optional[AdditionalStatisticsControl] = None

class SaOptimizer(SingleSolutionMetaheuristic):
    """
    Instance of the class :class:`~uo.algorithm.metaheuristic.simulated_annealing.SaOptimizer` encapsulate 
    :ref:`Algorithm_Simulated_Annealing` optimization algorithm.
    """
    def __init__(self,
            sa_neighbourhood: SaNeighbourhood,
            sa_temperature: SaTemperature,
            finish_control: FinishControl, 
            problem: Problem, 
            solution_template: Optional[Solution],
            output_control: Optional[OutputControl] = None, 
            random_seed: Optional[int] = None, 
            additional_statistics_control: Optional[AdditionalStatisticsControl] = None
        ) -> None:
        """
        Create new instance of class :class:`~uo.algorithm.metaheuristic.simulated_annealing.SaOptimizer`. 
        That instance implements :ref:`SA<Algorithm_Simulated_Annealing>` algorithm. 

        :param `SaNeighbourhood` sa_neighbourhood: neighbourhood structure for generating neighbors
        :param `SaTemperature` sa_temperature: placeholder for temperature method, specific for simulated annealing
        :param `FinishControl` finish_control: structure that control finish criteria for metaheuristic execution
        :param int random_seed: random seed for metaheuristic execution
        :param `AdditionalStatisticsControl` additional_statistics_control: structure that controls additional 
        statistics obtained during population-based metaheuristic execution        
        :param `OutputControl` output_control: structure that controls output
        :param `Problem` problem: problem to be solved
        :param `Solution` solution_template: initial solution of the problem 
        """
        super().__init__(name="sa",
                finish_control=finish_control, 
                random_seed=random_seed, 
                additional_statistics_control=additional_statistics_control, 
                output_control=output_control, 
                problem=problem,
                solution_template=solution_template)
        if not isinstance(sa_temperature, SaTemperature):
            raise TypeError('Parameter \'sa_temperature\' must be \'SaTemperature\'.')
        if not isinstance(sa_neighbourhood, SaNeighbourhood):
            raise TypeError('Parameter \'sa_neighbourhood\' must be \'SaNeighbourhood\'.')
        
        self.__sa_temperature: SaTemperature = sa_temperature
        self.__sa_neighbourhood: SaNeighbourhood = sa_neighbourhood

    @classmethod
    def from_construction_tuple(cls, construction_tuple: SaOptimizerConstructionParameters):
        """
        Additional constructor, that creates new instance of class :class:`~uo.algorithm.metaheuristic.simulated_annealing.SaOptimizer`. 

        :param `SaOptimizerConstructionParameters` construction_tuple: tuple with all constructor parameters
        """
        return cls(
            construction_tuple.sa_neighbourhood,
            construction_tuple.sa_temperature,
            construction_tuple.finish_control,
            construction_tuple.problem,
            construction_tuple.solution_template,
            construction_tuple.output_control,
            construction_tuple.random_seed,
            construction_tuple.additional_statistics_control
        )

    def init(self) -> None:
        """
        Initialization of the SA algorithm
        """
        self.current_solution = self.solution_template.copy()
        self.current_solution.copy_from(self.solution_template)
        self.current_solution.init_random(self.problem)
        self.evaluation = 1
        self.current_solution.evaluate(self.problem)
        self.best_solution = self.current_solution
        self.iteration = 0

    def main_loop_iteration(self) -> None:
        """
        One iteration within main loop of the SA algorithm
        """
        current_temperature = self.__sa_temperature.calculate(self.iteration)
        self.iteration += 1

        # Generate a new feasible neighbor solution
        neighbor_solution = self.__sa_neighbourhood.generate_neighbor(self.current_solution, self.problem, optimizer=self)

        # Compare solutions
        delta = neighbor_solution.value - self.current_solution.value

        # If new solution is better, accept it
        if neighbor_solution.is_better_than(self.current_solution):
            self.current_solution = neighbor_solution
            if neighbor_solution.is_better_than(self.best_solution):
                self.best_solution = neighbor_solution
        else:
            # If new solution is worse, accept with probability
            if random.random() < current_temperature:
                self.current_solution = neighbor_solution

        self.evaluation += 1

    def string_rep(self, delimiter: str, indentation: int = 0, indentation_symbol: str = '', group_start: str = '{',
                  group_end: str = '}') -> str:
        """
        String representation of the SA Optimizer instance.
        """
        s = delimiter
        for _ in range(0, indentation):
            s += indentation_symbol  
        s += group_start
        s = super().string_rep(delimiter, indentation, indentation_symbol, '', '')
        s += delimiter
        if self.current_solution is not None:
            s += 'current_solution=' + self.current_solution.string_rep(delimiter, indentation + 1, 
                    indentation_symbol, group_start, group_end) + delimiter
        else:
            s += 'current_solution=None' + delimiter
        for _ in range(0, indentation):
            s += indentation_symbol  
        s += '__sa_temperature=' + str(self.__sa_temperature) + delimiter
        for _ in range(0, indentation):
            s += indentation_symbol  
        s += '__sa_neighbourhood=' + str(self.__sa_neighbourhood) + delimiter
        for _ in range(0, indentation):
            s += indentation_symbol  
        s += group_end 
        return s

    def __str__(self) -> str:
        s = self.string_rep('|')
        return s

    def __repr__(self) -> str:
        s = self.string_rep('\n')
        return s

    def __format__(self, spec: str) -> str:
        return self.string_rep('\n', 0, '', '{', '}')

