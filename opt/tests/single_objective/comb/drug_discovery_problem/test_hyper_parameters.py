import unittest
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
import sys

from opt_so_comb_drug_discovery_ga_exec import Application

class TestHyperParameters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv)
        cls.window = Application()
        cls.window.show()
        cls.hp = cls.window.hyper_param_layout

        cls.hp.molecule_boxes.remove_boxes = MagicMock()
        cls.hp.molecule_boxes.remove_selected_boxes = MagicMock()
        cls.hp.molecule_boxes.load_boxes = MagicMock()
        cls.hp.molecule_boxes.load_selected_boxes = MagicMock()

    def test_initial_slider_values(self):
        for i, default in enumerate(self.hp.default_values):
            slider = self.hp.h_boxes[i].itemAt(1).widget()
            self.assertEqual(slider.value(), int(default * 100), f"Slider {i} should have initial value {int(default * 100)}")

    def test_update_param_label_changes_label_and_triggers_updates(self):
        idx = 0
        slider = self.hp.h_boxes[idx].itemAt(1).widget()
        label = self.hp.h_boxes[idx].itemAt(0).widget()

        slider.setValue(73)
        expected_text = f"{self.hp.names[idx]}: 0.73"

        self.assertEqual(label.text(), expected_text)
        self.assertAlmostEqual(self.hp.application.slider_values[idx], 0.73)

        self.hp.molecule_boxes.remove_boxes.assert_called()
        self.hp.molecule_boxes.remove_selected_boxes.assert_called()
        self.hp.molecule_boxes.load_boxes.assert_called()
        self.hp.molecule_boxes.load_selected_boxes.assert_called()

    def test_reset_button_resets_all_sliders(self):
        for i in range(len(self.hp.h_boxes)):
            slider = self.hp.h_boxes[i].itemAt(1).widget()
            slider.setValue(99)

        QTest.mouseClick(self.hp.reset_button, Qt.LeftButton)

        for i, default in enumerate(self.hp.default_values):
            slider = self.hp.h_boxes[i].itemAt(1).widget()
            self.assertEqual(slider.value(), int(default * 100), f"Slider {i} should be reset to {int(default * 100)}")

    def test_get_sliders_widget_returns_qwidget(self):
        container = self.hp.get_sliders_widget()
        self.assertIsNotNone(container)
        self.assertTrue(container.layout() is not None)

    @classmethod
    def tearDownClass(cls):
        cls.window.close()
        cls.app.quit()