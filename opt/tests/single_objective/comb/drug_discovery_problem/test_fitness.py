import unittest
from rdkit import Chem
from opt.single_objective.comb.drug_discovery_problem.fitness import Fitness

class TestFitness(unittest.TestCase):

    def setUp(self):
        # Valid SMILES string for a simple molecule (aspirin)
        smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"
        self.mol = Chem.MolFromSmiles(smiles)
        self.fitness = Fitness(self.mol)

    def test_qed_returns_float(self):
        result = self.fitness.qed()
        self.assertIsInstance(result, float)

    def test_qed_value_in_range(self):
        result = self.fitness.qed()
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_custom_weights(self):
        weights = (0.5,) * 8
        fitness = Fitness(self.mol, weights=weights)
        result = fitness.qed()
        self.assertIsInstance(result, float)

    def test_invalid_molecule_raises(self):
        with self.assertRaises(ValueError):
            Fitness(None)