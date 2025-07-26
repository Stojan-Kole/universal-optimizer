from rdkit import Chem
from typing import Tuple
from opt.single_objective.comb.drug_discovery_problem.fitness import Fitness

class Individual:
    """
    Represents a molecular individual characterized by its SMILES string,
    weights for property importance, and computed QED fitness value.
    """
    def __init__(self, smiles: str, description: str, weights: Tuple[float, ...] = (0.66, 0.46, 0.05, 0.61, 0.06, 0.65, 0.48, 0.95)):
        """
        Initializes an individual with SMILES, description, and property weights.

        :param smiles: The SMILES representation of the molecule
        :param description: A human-readable label or description
        :param weights: Weights for molecular properties used in QED calculation
        """
        self.__smiles: str = smiles
        self.__description: str = description
        self.__weights: Tuple[float, ...] = weights
        self._calculate_fitness()

    def _calculate_fitness(self) -> None:
        """
        Computes and stores the QED fitness value based on the current SMILES and weights.
        """
        fit = Fitness(Chem.MolFromSmiles(self.__smiles), self.__weights)
        self.__qed = fit.qed()

    def __lt__(self, other: "Individual") -> bool:
        """
        Enables comparison of individuals based on QED fitness value (for sorting).

        :param other: Another individual to compare with
        :return: True if self has lower QED than other
        :rtype: bool
        """
        return self.__qed < other.get_qed()

    def get_smiles(self) -> str:
        """
        Returns the SMILES string of the molecule.
        """
        return self.__smiles

    def get_description(self) -> str:
        """
        Returns the description of the molecule.
        """
        return self.__description

    def get_weights(self) -> Tuple[float, ...]:
        """
        Returns the weights used for fitness evaluation.
        """
        return self.__weights

    def get_qed(self) -> float:
        """
        Returns the QED fitness value.
        """
        return self.__qed

    def set_weights(self, weights: Tuple[float, ...]) -> None:
        """
        Updates the weights and recalculates fitness.

        :param weights: New weights for fitness evaluation
        """
        self.__weights = weights
        self._calculate_fitness()

    def set_description(self, description: str) -> None:
        """
        Updates the description of the molecule.

        :param description: New description string
        """
        self.__description = description

    def set_smiles(self, smiles: str) -> None:
        """
        Updates the SMILES string.

        :param smiles: New SMILES representation
        """
        self.__smiles = smiles

    def is_valid_smiles(self) -> bool:
        """
        Checks whether the current SMILES string can be parsed into a valid molecule.

        :return: True if valid, False otherwise
        :rtype: bool
        """
        # Use context manager to suppress output during RDKit validation
        with suppress_rdkit_warnings():
            mol = Chem.MolFromSmiles(self.__smiles)
        return mol is not None

    def __str__(self) -> str:
        """
        Returns a string representation of the individual.
        """
        return f"DrugDiscoverySolution:\n\tSMILES={self.__smiles}\n\tQED={self.__qed:.3f}\n"