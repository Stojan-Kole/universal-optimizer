import unittest
from unittest.mock import MagicMock, patch
from opt.single_objective.comb.drug_discovery_problem.solver import (
    genetic_algorithm, selection, roulette_wheel_selection, tournament_selection,
    mutation, crossover, atom_switch_mutation, group_switch_mutation,
    insertion_mutation, deletion_mutation, is_valid_smiles
)
from opt.single_objective.comb.drug_discovery_problem.mutation_info import MutationInfo


class TestGeneticAlgorithm(unittest.TestCase):

    def setUp(self):
        self.mock_population = [self._mock_individual(qed=0.1 + i * 0.1) for i in range(10)]
        self.mock_label = MagicMock()
        self.mock_progress = MagicMock()
        self.mock_mi = MagicMock(spec=MutationInfo)

        self.mock_mi.atom_switch_map = {
            'O': [('N', 0.5), ('S', 0.375), ('P', 0.125)],
            'S': [('O', 0.67), ('N', 0.22), ('P', 0.11)],
            'N': [('P', 1.0)],
            'P': [('N', 1.0)],
        }

        self.mock_mi.group_switch_map = {
            'C=O': ['C(C(=O)O)', 'CN'],
            'CC': ['COC', 'CC(=O)C', 'CCC'],
            'C(=O)O': ['C(=O)N'],
            'C#N': ['C=O'],
        }

        self.mock_mi.insertions = [
            '(C=O)', '(C(=O)O)', '(C)', '(C(=O)N)', '(N)', '(C#N)', '(C1=CC=CC=C1)'
        ]

    def _mock_individual(self, qed=0.5):
        mock = MagicMock()
        mock.get_qed.return_value = qed
        mock.get_smiles.return_value = 'CC(=O)OC1=CC=CC=C1C(=O)O'
        return mock

    def test_selection_roulette(self):
        selected = selection(self.mock_population, roulette_selection=True, tournament_size=2)
        self.assertIn(selected, self.mock_population)

    def test_selection_tournament(self):
        selected = selection(self.mock_population, roulette_selection=False, tournament_size=3)
        self.assertIn(selected, self.mock_population)

    def test_mutation_no_effect_when_probability_zero(self):
        individual = self._mock_individual()
        mutation(individual, mutation_probability=0.0, mi=self.mock_mi)
        individual.set_smiles.assert_not_called()

    def test_atom_switch_mutation(self):
        individual = self._mock_individual()
        individual.get_smiles.return_value = "NC"
        atom_switch_mutation(individual, self.mock_mi)
        individual.set_smiles.assert_called()

    def test_group_switch_mutation(self):
        individual = self._mock_individual()
        individual.get_smiles.return_value = "ClCCl"
        group_switch_mutation(individual, self.mock_mi)
        individual.set_smiles.assert_called()

    def test_insertion_mutation_success(self):
        individual = self._mock_individual()
        individual.get_smiles.return_value = "C"
        with patch('opt.single_objective.comb.drug_discovery_problem.solver.is_valid_smiles', return_value=True):
            insertion_mutation(individual, self.mock_mi)
        individual.set_smiles.assert_called()

    def test_insertion_mutation_fallback_to_deletion(self):
        individual = self._mock_individual()
        individual.get_smiles.return_value = "C" * 10
        with patch('opt.single_objective.comb.drug_discovery_problem.solver.is_valid_smiles', side_effect=[False, True]):
            insertion_mutation(individual, self.mock_mi)
        individual.set_smiles.assert_called()

    def test_deletion_mutation_success(self):
        individual = self._mock_individual()
        individual.get_smiles.return_value = "CCCC"
        with patch('opt.single_objective.comb.drug_discovery_problem.solver.is_valid_smiles', return_value=True):
            deletion_mutation(individual, self.mock_mi)
        individual.set_smiles.assert_called()

    def test_deletion_mutation_fail(self):
        individual = self._mock_individual()
        individual.get_smiles.return_value = "C"
        with patch('opt.single_objective.comb.drug_discovery_problem.solver.is_valid_smiles', return_value=False):
            deletion_mutation(individual, self.mock_mi)
        individual.set_smiles.assert_called()

    def test_is_valid_smiles_valid(self):
        self.assertTrue(is_valid_smiles("CCO"))

    def test_is_valid_smiles_invalid(self):
        self.assertFalse(is_valid_smiles("invalid$$"))

    def test_crossover_success(self):
        p1 = self._mock_individual()
        p2 = self._mock_individual()
        p1.get_smiles.return_value = "CCCCC"
        p2.get_smiles.return_value = "COC"
        child1 = MagicMock()
        child2 = MagicMock()
        with patch('opt.single_objective.comb.drug_discovery_problem.solver.is_valid_smiles', return_value=True):
            crossover(p1, p2, child1, child2)
        child1.set_smiles.assert_called()
        child2.set_smiles.assert_called()

    def test_crossover_fail_reuse_parents(self):
        p1 = self._mock_individual()
        p2 = self._mock_individual()
        p1.get_smiles.return_value = "CNC"
        p2.get_smiles.return_value = "C=C"
        child1 = MagicMock()
        child2 = MagicMock()
        with patch('opt.single_objective.comb.drug_discovery_problem.solver.is_valid_smiles', return_value=False):
            crossover(p1, p2, child1, child2)
        child1.set_smiles.assert_called_once_with("CNC")
        child2.set_smiles.assert_called_once_with("C=C")

    def test_genetic_algorithm_runs(self):
        for ind in self.mock_population:
            ind.get_smiles.return_value = "CCO"
        result = genetic_algorithm(
            self.mock_population,
            only_one_generation=True,
            number_of_generations=5,
            roulette_selection=True,
            tournament_size=2,
            elitism_size=2,
            mutation_probability=0.5,
            mi=self.mock_mi,
            individual_label=self.mock_label,
            individual_progress=self.mock_progress
        )
        self.assertEqual(len(result), len(self.mock_population))