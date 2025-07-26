""" 
..  _py_drug_discovery_problem_solution:

The :mod:`~opt.single_objective.comb.drug_discovery_problem.drug_discovery_problem_solution` contains class :class:`~opt.single_objective.comb.drug_discovery_problem.drug_discovery_problem_solution.DrugDiscoveryProblemSolution`, that represents solution of the :ref:`Problem_Drug_Discovery`.
"""
import sys
from pathlib import Path
from typing import Optional
directory = Path(__file__).resolve()
sys.path.append(directory)
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent.parent)
sys.path.append(directory.parent.parent.parent.parent)
sys.path.append(directory.parent.parent.parent.parent.parent)

from rdkit import DataStructs
from rdkit.Chem import AllChem

from uo.problem.problem import Problem
from uo.solution.quality_of_solution import QualityOfSolution
from uo.solution.solution import Solution

from uo.utils.logger import logger

from .individual import Individual

class DrugDiscoveryProblemSolution(Solution[Individual, str]):

    def __init__(self,
                 random_seed: Optional[int] = None,
                 fitness_value: Optional[float] = None,
                 fitness_values: Optional[list[float]] = None,
                 objective_value: Optional[float] = None,
                 objective_values: Optional[list[float]] = None,
                 is_feasible: bool = True,
                 evaluation_cache_is_used: bool = False,
                 evaluation_cache_max_size: Optional[int] = None,
                 distance_calculation_cache_is_used: bool = False,
                 distance_calculation_cache_max_size: Optional[int] = None
                 ) -> None:
        """
        Create new `DrugDiscoveryProblemSolution` instance
        """
        super().__init__(random_seed,
                         fitness_value,
                         fitness_values,
                         objective_value,
                         objective_values,
                         is_feasible,
                         evaluation_cache_is_used,
                         evaluation_cache_max_size,
                         distance_calculation_cache_is_used,
                         distance_calculation_cache_max_size)
        self.representation: Optional[Individual] = None
    

    def copy(self):
        """
        Copy of the `DrugDiscoveryProblemSolution`

        :return: new `DrugDiscoveryProblemSolution` instance with the same properties
        :rtype: DrugDiscoveryProblemSolution
        """
        copy_sol = DrugDiscoverySolution(
            random_seed = self.random_seed,
            fitness_value = self.fitness_value,
            fitness_values = self.fitness_values.copy() if self.fitness_values else None,
            objective_value = self.objective_value,
            objective_values = self.objective_values.copy() if self.objective_values else None,
            is_feasible = self.is_feasible,
            evaluation_cache_is_used = self.evaluation_cache_cs is not None,
            evaluation_cache_max_size = self.evaluation_cache_cs.max_cache_size if self.evaluation_cache_cs else None,
            distance_calculation_cache_is_used = self.representation_distance_cache_cs is not None,
            distance_calculation_cache_max_size = self.representation_distance_cache_cs.max_cache_size if self.representation_distance_cache_cs else None
        )
        if self.representation is not None:
            # Deep copy individual
            copy_sol.representation = Individual(
                self.representation.getSmiles(),
                self.representation.getDescription(),
                self.representation.getWeights()
            )
        return copy_sol

    def copy_from(self, original: "DrugDiscoverySolution") -> None:
        """
        Copy all data from the original target solution
        """
        super().copy_from(original)
        if original.representation is not None:
            self.representation = Individual(
                original.representation.getSmiles(),
                original.representation.getDescription(),
                original.representation.getWeights()
            )
        else:
            self.representation = None

    def argument(self, representation: Individual) -> str:
        """
        Argument of the target solution

        :param representation: internal representation of the solution
        :type representation: `Individual`
        :return: argument of the solution 
        :rtype: str
        """
        return str(representation)

    def init_random(self, problem: Problem) -> None:
        """
        Random initialization of the solution

        :param `Problem` problem: problem which is solved by solution
        """
        self.representation = problem.get_random_individual()
        self.evaluate(problem)

    def native_representation(self, representation_str: str) -> Individual:
        """
        Obtain `Individual` representation from string representation of the solution of the Drug Discovery problem 

        :param str representation_str: solution's representation as string
        :return: solution's native representation as Individual
        :rtype: `Individual`
        """
        return Individual(representation_str, representation_str)

    def init_from(self, representation: Individual, problem: Problem) -> None:
        """
        Initialization of the solution, by setting its native representation 

        :param `Individual` representation: representation that will be ste to solution
        :param `Problem` problem: problem which is solved by solution
        """
        if not isinstance(representation, Individual):
            raise TypeError('Parameter \'representation\' must have type \'Individual\'.')
        self.representation = representation
        self.evaluate(problem)

    def calculate_quality_directly(self, representation: Individual, problem: Problem) -> QualityOfSolution:
        """
        Fitness calculation of the target solution

        :param `Individual` representation: native representation of the solution for which objective value, fitness and feasibility are calculated
        :param `Problem` problem: problem that is solved
        :return: objective value, fitness value and feasibility of the solution instance 
        :rtype: `QualityOfSolution`
        """

        fitness = representation.getQED()
        objective = fitness  # maximization problem -> objective can be equal to fitness
        is_feasible = representation.isValidSmiles()
        return QualityOfSolution(objective_value=objective, fitness_value=fitness, is_feasible=is_feasible)

    def representation_distance_directly(self, representation_1: Individual, representation_2: Individual) -> float:
        """
        Directly calculate distance between two solutions determined by their native representations
        In this case, Tanimoto distance between the molecules is used.

        :param `Individual` representation_1: native representation for the first solution
        :param `Individual` representation_2: native representation for the second solution
        :return: distance 
        :rtype: float
        """

        mol1 = Chem.MolFromSmiles(representation_1.getSmiles())
        mol2 = Chem.MolFromSmiles(representation_2.getSmiles())

        # If some of these molecules are invalid, their distance is set to infinity
        if mol1 is None or mol2 is None:
            return float('inf')

        fp1 = AllChem.GetMorganFingerprintAsBitVect(mol1, 2)
        fp2 = AllChem.GetMorganFingerprintAsBitVect(mol2, 2)

        similarity = DataStructs.TanimotoSimilarity(fp1, fp2)
        distance = 1.0 - similarity
        return distance

    def __str__(self) -> str:
        """
        String representation of the target solution instance

        :return: string representation of the target solution instance
        :rtype: str
        """
        return self.string_rep(
            delimiter = "\n", 
            indentation = 0, 
            indentation_symbol = "  ", 
            group_start = "{", 
            group_end = "}"
        )

    def __repr__(self) -> str:
        """
        Representation of the target solution instance

        :return: string representation of the target solution instance
        :rtype: str
        """
        return self.string_rep(
            delimiter = ", ",
            indentation = 0,
            indentation_symbol = "",
            group_start = "{",
            group_end = "}"
        )

    def __format__(self, spec: str) -> str:
        """
        Formatted the target solution instance

        :param spec: str -- format specification
        :return: formatted target solution instance
        :rtype: str
        """
        if spec == "full":
            return self.string_rep(
                delimiter = "\n",
                indentation = 0,
                indentation_symbol = "  ",
                group_start = "{",
                group_end = "}"
            )
        elif spec == "compact":
            return self.string_rep(
                delimiter = ", ",
                indentation = 0,
                indentation_symbol = "",
                group_start = "{",
                group_end = "}"
            )
        elif spec == "flat":
            return self.string_rep(
                delimiter = " | ",
                indentation = 0,
                indentation_symbol = "",
                group_start = "[",
                group_end = "]"
            )
        else:
            return str(self)