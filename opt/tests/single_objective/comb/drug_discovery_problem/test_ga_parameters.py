import unittest
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from opt.single_objective.comb.drug_discovery_problem.ga_parameters import GAParameters
from opt_so_comb_drug_discovery_ga_exec import Application


class TestGAParameters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the QApplication and Application."""
        cls.app = QApplication(sys.argv)
        cls.window = Application()

    def setUp(self):
        """Get a fresh instance of GAParameters for each test."""
        self.ga_params = self.window.ga_parameters
        self.molecule_boxes = self.window.molecule_boxes

    def test_initial_values(self):
        """Ensure default GA parameters are correctly set."""
        self.assertEqual(self.ga_params.generation_spin.value(), 100)
        self.assertEqual(self.ga_params.tournament_spin.value(), 7)
        self.assertEqual(self.ga_params.elitism_spin.value(), 2)
        self.assertEqual(self.ga_params.mutation_line_edit.text(), "0.05")
        self.assertFalse(self.ga_params.roulette_check_box.isChecked())

    def test_set_parameters(self):
        """Simulate setting new GA parameter values."""
        # Change parameters manually
        self.ga_params.generation_spin.setValue(150)
        self.ga_params.tournament_spin.setValue(5)
        self.ga_params.elitism_spin.setValue(4)
        self.ga_params.mutation_line_edit.setText("0.1")
        self.ga_params.roulette_check_box.setChecked(True)

        # Check if values changed as expected
        self.assertEqual(self.ga_params.generation_spin.value(), 150)
        self.assertEqual(self.ga_params.tournament_spin.value(), 5)
        self.assertEqual(self.ga_params.elitism_spin.value(), 4)
        self.assertEqual(self.ga_params.mutation_line_edit.text(), "0.1")
        self.assertTrue(self.ga_params.roulette_check_box.isChecked())

    def test_launch_button_click_updates_ui_state(self):
        self.ga_params.generation_spin.setValue(10)
        self.ga_params.tournament_spin.setValue(3)
        self.ga_params.elitism_spin.setValue(2)
        self.ga_params.mutation_line_edit.setText("0.1")
        self.ga_params.roulette_check_box.setChecked(True)

        QTest.mouseClick(self.ga_params.launch_button, Qt.LeftButton)

        self.assertFalse(self.ga_params.launch_button.isEnabled(), "Launch button should be disabled")
        self.assertFalse(self.ga_params.roulette_check_box.isEnabled(), "Checkbox should be disabled")
        self.assertFalse(self.ga_params.generation_spin.isEnabled(), "Generation spin should be disabled")
        self.assertFalse(self.ga_params.tournament_spin.isEnabled(), "Tournament spin should be disabled")
        self.assertFalse(self.ga_params.elitism_spin.isEnabled(), "Elitism spin should be disabled")
        self.assertFalse(self.ga_params.mutation_line_edit.isEnabled(), "Mutation input should be disabled")

        self.assertEqual(self.window.number_of_generations, 10)
        self.assertEqual(self.window.tournament_size, 3)
        self.assertEqual(self.window.elitism_size, 2)
        self.assertAlmostEqual(self.window.mutation_probability, 0.1)
        self.assertTrue(self.window.roulette_selection)

        self.assertIsNotNone(self.molecule_boxes.generation_label.text())
        self.assertIn("Generation:", self.molecule_boxes.generation_label.text())
        self.assertIn("Individual:", self.molecule_boxes.individual_label.text())

        self.assertTrue(self.molecule_boxes.generate_button.isEnabled())
        self.assertTrue(self.molecule_boxes.final_button.isEnabled())
        self.assertTrue(self.molecule_boxes.save_button.isEnabled())
        self.assertTrue(self.molecule_boxes.restart_button.isEnabled())

        self.assertTrue(self.window.block_transfer, "Optimization should be marked as active")

    @classmethod
    def tearDownClass(cls):
        """Close the application once after all tests."""
        cls.window.close()
        cls.app.quit()