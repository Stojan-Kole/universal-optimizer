""" 
..  _py_drug_discovery_problem:

"""

import sys
import random
import json
from pathlib import Path
from typing import Optional
directory = Path(__file__).resolve()
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)
sys.path.append(directory.parent.parent.parent.parent)
sys.path.append(directory.parent.parent.parent.parent.parent)

from uo.problem.problem import Problem
from uo.utils.logger import logger

from .individual import Individual

class DrugDiscoveryProblem(Problem):
    """
    Class representing the Drug Discovery Problem.

    This class inherits from the Problem class and is used to define and solve the Drug Discovery Problem. The problem is defined by a graph and a list of source terminal pairs.
    
    Attributes:
        name (str): Name of the problem.
        is_minimization (bool): Whether the problem is a minimization problem.
        is_multi_objective (bool): Whether the problem has multiple objectives.
        __molecules (list[Individual]): List of Individuals loaded from file, representing available candidate molecules.

    Methods:
        __init__(name: str = "DrugDiscoveryProblem", is_minimization: bool = False, is_multi_objective: bool = False):
            Initializes a new instance of DrugDiscoveryProblem.
        
        __load_from_file__(file_path: str) -> list[Individual]:
            Internal method that loads molecule data from a JSON file and returns a list of Individuals.

        from_input_file(file_path: str) -> DrugDiscoveryProblem:
            Class method that loads molecules from file and returns a new DrugDiscoveryProblem instance with initial molecules.
        
        get_random_individual() -> Individual:
            Returns a randomly selected Individual from the list of initial molecules.
        
        copy() -> DrugDiscoveryProblem:
            Returns a copy of the current DrugDiscoveryProblem instance.
        
        __str__() -> str:
            String representation of the DrugDiscoveryProblem instance.

        __repr__() -> str:
            Official representation of the DrugDiscoveryProblem instance.

        __format__(spec: str) -> str:
            Formatted representation of the DrugDiscoveryProblem instance.
    
    """

    def __init__(self,
                 name: str = "DrugDiscoveryProblem", 
                 is_minimization: bool = False,
                 is_multi_objective: bool = False) -> None:
        """
        Create a new `DrugDiscoveryProblem` instance.

        :param str name: name of the problem
        :param bool is_minimization: if problem is minimization
        :param bool is_multi_objective: if problem is multi-objective
        
        """
        super().__init__(name = name,
                         is_minimization = is_minimization,
                         is_multi_objective = is_multi_objective)
        self.__molecules : list[Individual] = []

    def copy(self) -> 'DrugDiscoveryProblem':
        """
        Copy the current object

        :return:  new instance with the same properties
        :rtype: :class:`DrugDiscoveryProblem`
        """
        return DrugDiscoveryProblem(
            name = self.name,
            is_minimization = self.is_minimization,
            is_multi_objective = self.is_multi_objective
        )

    @property
    def molecules(self) -> list[Individual]:
        """
        Getter for the list of loaded molecules.

        :return: List of Individual instances
        :rtype: list[Individual]
        """
        return self.__molecules
        
    @molecules.setter
    def molecules(self, new_molecules: list[Individual]):
        """
        Setter for the list of molecules.

        :param new_molecules: New list of Individual instances to replace the current one
        :type new_molecules: list[Individual]
        """
        if not isinstance(new_molecules, list):
            raise TypeError("Expected a list of Individual instances.")
        if not all(isinstance(mol, Individual) for mol in new_molecules):
            raise ValueError("All elements must be instances of Individual.")
        self.__molecules = new_molecules
    
    @classmethod
    def __load_from_file__(cls, file_path: str) -> list[Individual]:
        """
        Reads molecule data from a JSON file and returns a list of Individuals.

        :param file_path: path to the JSON file
        :return: list of Individuals created from the file data
        :rtype: list[`Individual`]
        """
        logger.debug(f"Loading molecules from file: {file_path}")
        with open(file_path, 'r') as file:
            data = json.load(file)
        return [
            Individual(item['SMILES'], item['Description'])
            for item in data
        ]

    @classmethod
    def from_input_file(cls, file_path: str) -> "DrugDiscoveryProblem":
        """
        Additional constructor. Creates a DrugDiscoveryProblem instance from a JSON file.

        :param file_path: path to the JSON file with molecule data
        :return: initialized DrugDiscoveryProblem instance
        """
        molecules: list[Individual] = cls.__load_from_file__(file_path)

        if not molecules:
            raise ValueError(f"No molecules found in file: {file_path}")

        instance = cls()
        instance.molecules = molecules
        return instance

    def get_random_individual(self) -> Individual:
        """
        Returns a randomly selected Individual from the loaded list of molecules.

        :return: randomly selected Individual
        :rtype: Individual
        """
        if not self.__molecules:
            raise ValueError("The list of initial molecules is empty.")
        return random.choice(self.__molecules)

    def __str__(self)->str:
        """
        String representation of the target problem instance

        :return: string representation of the target problem instance
        :rtype: str
        """
        return super().__str__()

    def __repr__(self)->str:
        """
        Representation of the target problem instance

        :return: string representation of the problem instance
        :rtype: str
        """
        return super().__repr__()

    def __format__(self, spec:str)->str:
        """
        Formatted the target problem instance

        :param str spec: format specification
        :return: formatted target problem instance
        :rtype: str
        """
        return super().__format__(spec)