import unittest
from PyQt5.QtWidgets import QApplication
from opt_so_comb_drug_discovery_ga_exec import Application
import sys

app = QApplication(sys.argv)

class TestApplicationInitialization(unittest.TestCase):
    def setUp(self):
        self.window = Application()

    def tearDown(self):
        self.window.close()

    def test_components_initialized(self):
        self.assertIsNotNone(self.window.problem)
        self.assertIsNotNone(self.window.molecule_boxes)
        self.assertIsNotNone(self.window.new_molecule_form)
        self.assertIsNotNone(self.window.hyper_param_layout)
        self.assertIsNotNone(self.window.ga_parameters)
        self.assertIsNotNone(self.window.mi)

    def test_layout_structure(self):
        self.assertEqual(self.window.main_layout.count(), 2)
        self.assertEqual(self.window.left_layout.count(), 5)
        self.assertEqual(self.window.right_layout.count(), 3)

    def test_submit_button_behavior(self):
        self.window.new_molecule_form.input_smiles.setText("CCO")
        self.window.new_molecule_form.input_description.setText("ethanol")
        self.window.on_submit_button_clicked()
        found = False
        for mol in self.window.molecules:
            if mol.get_smiles() == "CCO" and mol.get_description() == "ethanol":
                found = True
                break
        self.assertEqual(found, True)
