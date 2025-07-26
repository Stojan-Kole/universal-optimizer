from rdkit import Chem
from rdkit.Chem import QED
from rdkit.Chem.rdchem import Mol

class Fitness:
    """
    A class used to compute the QED fitness score for a given RDKit molecule.

    Attributes:
        molecule (Mol): RDKit molecule object.
        weights (tuple[float]): Optional weights used in the QED calculation.
    """
    def __init__(self, molecule: Mol, weights: tuple[float, ...] = (0.66, 0.46, 0.05, 0.61, 0.06, 0.65, 0.48, 0.95)):
        """
        Initialize the Fitness object with a molecule and optional QED weights.

        Args:
            molecule (Mol): RDKit molecule.
            weights (tuple[float, ...], optional): Weights for QED calculation. Defaults to pre-defined values.
        """
        if molecule is None:
            raise ValueError("Molecule cannot be None")
        self.molecule = molecule
        self.weights = weights

    def qed(self) -> float:
        """
        Compute the QED (Quantitative Estimate of Drug-likeness) for the molecule.

        Returns:
            float: QED value.
        """
        return QED.qed(self.molecule, self.weights)