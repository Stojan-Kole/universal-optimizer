import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QDesktopWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QScrollArea, QGroupBox
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt
from rdkit import Chem
from rdkit.Chem import Draw
from opt.single_objective.comb.drug_discovery_problem.molecule_boxes import MoleculeBoxes
from opt.single_objective.comb.drug_discovery_problem.insert_molecule import NewMoleculeForm
from opt.single_objective.comb.drug_discovery_problem.hyper_parameters import HyperParameters
from opt.single_objective.comb.drug_discovery_problem.ga_parameters import GAParameters
from opt.single_objective.comb.drug_discovery_problem.individual import Individual
from opt.single_objective.comb.drug_discovery_problem.mutation_info import MutationInfo

from uo.algorithm.metaheuristic.finish_control import FinishControl

from opt.single_objective.comb.drug_discovery_problem.drug_discovery_problem import DrugDiscoveryProblem

class Application(QWidget):
    """
    Main application window for the drug discovery GUI.
    Manages layout, user input forms, molecule display, and GA parameter widgets.
    """
    def __init__(self) -> None:
        """
        Initializes the main application window for the drug discovery GUI.

        This method sets up the complete interface, including:
        - Loading the drug discovery problem with initial molecules.
        - Creating and arranging all GUI components such as:
            - Molecule display areas (catalogue, working set, best solution).
            - New molecule input form.
            - Hyperparameter sliders.
            - Genetic algorithm parameter controls.
        - Defining default genetic algorithm settings.
        - Organizing the left and right panels within the main layout.
        - Finalizing and displaying the GUI.
        """
        super().__init__()

        self.problem : DrugDiscoveryProblem = DrugDiscoveryProblem.from_input_file('opt/single_objective/comb/drug_discovery_problem/data/molecules.json')

        self.setWindowTitle('Drug Discovery')
        self.resize(800, 600)

        self.main_layout: QHBoxLayout = QHBoxLayout()
        self.left_layout: QVBoxLayout = QVBoxLayout()

        self.molecules: list[Individual] = self.problem.molecules
        self.slider_values: list[float] = [0.66, 0.46, 0.05, 0.61, 0.06, 0.65, 0.48, 0.95]

        # Allow transfering molecule boxes between scroll areas
        self.block_transfer: bool = False

        self.molecule_boxes: MoleculeBoxes = MoleculeBoxes(self)
        self.new_molecule_form: NewMoleculeForm = NewMoleculeForm(self)
        self.hyper_param_layout: HyperParameters = HyperParameters(self)
        self.ga_parameters: GAParameters = GAParameters(self)
        self.mi: MutationInfo = MutationInfo()

        self.roulette_selection: bool = False
        self.number_of_generations: int = 100
        self.tournament_size: int = 4
        self.elitism_size: int = 1
        self.mutation_probability: float = 0.05

        self.sbmt_btn: QPushButton = self.new_molecule_form.submit_button
        self.res_btn: QPushButton = self.hyper_param_layout.reset_button

        self.cnt: QWidget = QWidget()
        self.h1: QHBoxLayout = QHBoxLayout()
        self.h1.setSizeConstraint(760)

        self.h1.addWidget(self.new_molecule_form.get_form())
        self.h1.addWidget(self.hyper_param_layout.get_sliders_widget())

        self.cnt.setLayout(self.h1)
        self.cnt.setFixedWidth(765)
        self.cnt.setFixedHeight(300)

        self.left_layout.addWidget(self.molecule_boxes.get_selection_widget())
        self.left_layout.addSpacing(70)
        self.left_layout.addWidget(self.cnt)
        self.left_layout.addSpacing(30)
        self.left_layout.addWidget(self.ga_parameters.get_GA_parameters_widget())
        
        self.left_wrapper: QWidget = QWidget()
        self.left_wrapper.setLayout(self.left_layout)
        self.left_wrapper.setFixedHeight(880)
        self.main_layout.addWidget(self.left_wrapper)

        self.right_layout: QVBoxLayout = QVBoxLayout()
        self.right_layout.addWidget(self.molecule_boxes.get_precedent_scroll_area())
        self.right_layout.addWidget(self.molecule_boxes.get_second_scroll_area())
        self.right_layout.addWidget(self.molecule_boxes.get_best())

        self.right_wrapper: QWidget = QWidget()
        self.right_wrapper.setLayout(self.right_layout)
        self.right_wrapper.setFixedHeight(880)
        self.main_layout.addWidget(self.right_wrapper)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.main_layout)
        self.setFixedSize(1750, 900)

        self.show()

    def paintEvent(self, event) -> None:
        """
        Draws separator lines between left and right panels.
        """
        painter: QPainter = QPainter(self)
        painter.setPen(QPen(QColor(128, 128, 128), 2))
        painter.drawLine(10, 685, 800, 685)
        painter.drawLine(800, 20, 800, 880)
        painter.end()

    def on_submit_button_clicked(self) -> None:
        """
        Handles the submission of a new molecule entered by the user.
        """
        smiles: str = self.new_molecule_form.get_input_smiles_text()
        description: str = self.new_molecule_form.get_input_description_text()
        self.molecule_boxes.add_to_catalogue(smiles, description)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Application()
    sys.exit(app.exec_())