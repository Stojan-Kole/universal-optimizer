import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QDesktopWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QScrollArea, QGroupBox
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt
from rdkit import Chem
from rdkit.Chem import Draw
from opt.single_objective.comb.drug_discovery_problem.molecule_boxes import MoleculeBoxes
from opt.single_objective.comb.drug_discovery_problem.insertMolecule import NewMoleculeForm
from opt.single_objective.comb.drug_discovery_problem.hyperParameters import HyperParameters
from opt.single_objective.comb.drug_discovery_problem.ga_parameters import GAParameters
from opt.single_objective.comb.drug_discovery_problem.individual import Individual
from opt.single_objective.comb.drug_discovery_problem.mutationInfo import MutationInfo

from uo.algorithm.metaheuristic.finish_control import FinishControl

from opt.single_objective.comb.drug_discovery_problem.drug_discovery_problem import DrugDiscoveryProblem
from opt.single_objective.comb.drug_discovery_problem.drug_discovery_problem_solution import DrugDiscoveryProblemSolution


class Application(QWidget):
    def __init__(self):
        super().__init__()

        self.problem : DrugDiscoveryProblem = DrugDiscoveryProblem.from_input_file('opt/single_objective/comb/drug_discovery_problem/data/molecules.json')

        self.setWindowTitle('Drug Discovery')
        self.resize(800, 600)

        self.mainLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()

        self.molecules = self.problem.molecules
        self.slider_values = [0.66, 0.46, 0.05, 0.61, 0.06, 0.65, 0.48, 0.95]

        # Allow transfering molecule boxes between scroll areas
        self.block_transfer = False

        self.molecule_boxes: MoleculeBoxes = MoleculeBoxes(self)
        self.newMoleculeForm = NewMoleculeForm(self)
        self.hyperParamLayout = HyperParameters(self)
        self.gaParameters = GAParameters(self)

        self.mi = MutationInfo()
        self.roulette_selection = False
        self.number_of_generations = 100
        self.tournament_size = 4
        self.elitism_size = 1
        self.mutation_probability = 0.05

        self.sbmt_btn = self.newMoleculeForm.submitButton
        self.res_btn = self.hyperParamLayout.resetButton

        self.cnt = QWidget()
        self.h1 = QHBoxLayout()
        self.h1.setSizeConstraint(760)

        self.h1.addWidget(self.newMoleculeForm.getForm())
        self.h1.addWidget(self.hyperParamLayout.getSlidersWidget())

        self.cnt.setLayout(self.h1)
        self.cnt.setFixedWidth(765)
        self.cnt.setFixedHeight(300)

        self.leftLayout.addWidget(self.molecule_boxes.getSelectionWidget())
        self.leftLayout.addSpacing(70)
        self.leftLayout.addWidget(self.cnt)
        self.leftLayout.addSpacing(30)
        self.leftLayout.addWidget(self.gaParameters.getGAParametersWidget())
        
        self.leftWrapper = QWidget()
        self.leftWrapper.setLayout(self.leftLayout)
        self.leftWrapper.setFixedHeight(880)
        self.mainLayout.addWidget(self.leftWrapper)

        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.molecule_boxes.getPrecedentScrollArea())
        self.rightLayout.addWidget(self.molecule_boxes.getSecondScrollArea())
        self.rightLayout.addWidget(self.molecule_boxes.getBest())

        self.rightWrapper = QWidget()
        self.rightWrapper.setLayout(self.rightLayout)
        self.rightWrapper.setFixedHeight(880)
        self.mainLayout.addWidget(self.rightWrapper)
        self.mainLayout.setAlignment(Qt.AlignTop)

        self.setLayout(self.mainLayout)
        self.setFixedSize(1750, 900)

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(QColor(128, 128, 128), 2))
        painter.drawLine(10, 685, 800, 685)
        painter.drawLine(800, 20, 800, 880)
        painter.end()

    def onSubmitButtonClicked(self):
        smiles = self.newMoleculeForm.getInputSmilesText()
        description = self.newMoleculeForm.getInputDescriptionText()
        self.molecule_boxes.addToCatalogue(smiles, description)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Application()
    sys.exit(app.exec_())