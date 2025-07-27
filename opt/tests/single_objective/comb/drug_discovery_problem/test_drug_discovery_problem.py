import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile
import json
import os

from opt.single_objective.comb.drug_discovery_problem.drug_discovery_problem import DrugDiscoveryProblem
from opt.single_objective.comb.drug_discovery_problem.individual import Individual

MOCK_DATA = [
    {"SMILES": "CCO", "Description": "Ethanol"},
    {"SMILES": "CC(=O)O", "Description": "Acetic acid"}
]

class TestDrugDiscoveryProblem(unittest.TestCase):

    def setUp(self):
        """Create a temporary JSON file with molecule data."""
        self.temp_file = NamedTemporaryFile(mode="w+", delete=False, suffix=".json")
        json.dump(MOCK_DATA, self.temp_file)
        self.temp_file.close()

    def tearDown(self):
        """Remove the temporary file after test."""
        os.unlink(self.temp_file.name)

    def test_init_default(self):
        problem = DrugDiscoveryProblem()
        self.assertEqual(problem.name, "DrugDiscoveryProblem")
        self.assertFalse(problem.is_minimization)
        self.assertFalse(problem.is_multi_objective)
        self.assertEqual(problem.molecules, [])

    def test_molecules_setter_and_getter_valid(self):
        problem = DrugDiscoveryProblem()
        new_mols = [Individual("CCO", "ethanol")]
        problem.molecules = new_mols
        self.assertEqual(problem.molecules, new_mols)

    def test_molecules_setter_invalid_type(self):
        problem = DrugDiscoveryProblem()
        with self.assertRaises(TypeError):
            problem.molecules = "not a list"

    def test_molecules_setter_invalid_element(self):
        problem = DrugDiscoveryProblem()
        with self.assertRaises(ValueError):
            problem.molecules = ["invalid"]

    def test_load_from_file(self):
        molecules = DrugDiscoveryProblem.__load_from_file__(self.temp_file.name)
        self.assertIsInstance(molecules, list)
        self.assertTrue(all(isinstance(m, Individual) for m in molecules))
        self.assertEqual(molecules[0].get_description(), "Ethanol")

    def test_from_input_file_success(self):
        problem = DrugDiscoveryProblem.from_input_file(self.temp_file.name)
        self.assertIsInstance(problem, DrugDiscoveryProblem)
        self.assertEqual(len(problem.molecules), 2)

    def test_from_input_file_empty(self):
        # Overwrite the file with empty list
        with open(self.temp_file.name, 'w') as f:
            json.dump([], f)
        with self.assertRaises(ValueError):
            DrugDiscoveryProblem.from_input_file(self.temp_file.name)

    def test_get_random_individual(self):
        problem = DrugDiscoveryProblem.from_input_file(self.temp_file.name)
        random_individual = problem.get_random_individual()
        self.assertIsInstance(random_individual, Individual)

    def test_get_random_individual_empty(self):
        problem = DrugDiscoveryProblem()
        with self.assertRaises(ValueError):
            problem.get_random_individual()

    def test_copy_method(self):
        problem = DrugDiscoveryProblem(name="P1", is_minimization=True, is_multi_objective=True)
        new_problem = problem.copy()
        self.assertIsInstance(new_problem, DrugDiscoveryProblem)
        self.assertEqual(new_problem.name, "P1")
        self.assertTrue(new_problem.is_minimization)
        self.assertTrue(new_problem.is_multi_objective)

    def test_str_repr_format(self):
        problem = DrugDiscoveryProblem()
        self.assertIsInstance(str(problem), str)
        self.assertIsInstance(repr(problem), str)
        self.assertIsInstance(format(problem, ""), str)