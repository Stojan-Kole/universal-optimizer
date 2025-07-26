import json
import copy
import re
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QGraphicsDropShadowEffect, QWidget, QGridLayout, QScrollArea, QPushButton, QProgressBar
from PyQt5.QtGui import QImage, QPixmap, QColor, QFont
from PyQt5.QtCore import QEvent, Qt
from rdkit import Chem
from rdkit.Chem import Draw, rdMolDescriptors
from rdkit.DataStructs import FingerprintSimilarity
from opt.single_objective.comb.drug_discovery_problem.fitness import Fitness
from opt.single_objective.comb.drug_discovery_problem.individual import Individual
from opt.single_objective.comb.drug_discovery_problem.solver import genetic_algorithm
from opt.single_objective.comb.drug_discovery_problem.mutationInfo import MutationInfo
from datetime import datetime

class ClickableGroupBox(QGroupBox):
    def __init__(self, molecule_boxes, index, ind, parent=None):
        super().__init__(parent)
        self.molecule_boxes = molecule_boxes
        self.index = index
        self.ind = ind
       
    def mousePressEvent(self, event):
        if self.molecule_boxes.application.block_transfer:
            return
        if self.ind != 0 and self.ind != 1:
            return
        if event.button() == Qt.LeftButton:
            self.molecule_boxes.removeBoxes()
            self.molecule_boxes.removeSelectedBoxes()
            if self.ind == 0:
                self.molecule_boxes.selected_molecules.append(self.molecule_boxes.molecules[self.index])
                self.molecule_boxes.molecules.pop(self.index)
            elif self.ind == 1:
                self.molecule_boxes.molecules.append(self.molecule_boxes.selected_molecules[self.index])
                self.molecule_boxes.selected_molecules.pop(self.index)
            self.molecule_boxes.load_boxes(tuple(self.molecule_boxes.application.slider_values))
            self.molecule_boxes.load_selected_boxes(tuple(self.molecule_boxes.application.slider_values))

        super().mousePressEvent(event)

    def enterEvent(self, event):
        if not self.molecule_boxes.application.block_transfer:
            self.layout().itemAt(1).widget().setStyleSheet("color: darkgreen; font-weight: bold;")

    def leaveEvent(self, event):
        if not self.molecule_boxes.application.block_transfer:
            self.layout().itemAt(1).widget().setStyleSheet("color: black; font-weight: normal;")

class MoleculeBoxes(QWidget):
    def __init__(self, application):
        super().__init__(application)
        self.application = application
        self.molecules = application.molecules
        self.windowWidth = application.width()
        self.boxWidth = 220
        self.columnsPerRow = 3
        self.layout = QGridLayout()

        self.vbox = QVBoxLayout()

        self.selectionHBox = QHBoxLayout()

        self.selectionLabel = QLabel("Select molecules for the first generation:")
        self.selectionLabel.setStyleSheet("font-size: 20px; font-weight: bold; padding-bottom: 10px;")

        self.selectAllButton = QPushButton("Select all")
        self.selectAllButton.setFixedWidth(100)
        self.selectAllButton.setStyleSheet("""
            QPushButton {
                background-color: #696969;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)
        self.selectAllButton.clicked.connect(self.onSelectAllButtonClicked)

        self.selectionHBox.addWidget(self.selectionLabel)
        self.selectionHBox.addWidget(self.selectAllButton)

        self.selectionContainer = QWidget()
        self.selectionContainer.setLayout(self.selectionHBox)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedSize(760, 290)

        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.layout)
        self.scrollArea.setWidget(self.scrollWidget)

        self.vbox.addWidget(self.selectionContainer)
        self.vbox.addWidget(self.scrollArea)

        self.container = QWidget()
        self.container.setLayout(self.vbox)
        self.container.setFixedSize(760, 350)

        self.selected_molecules = []
        self.new_generation_molecules = []

        self.precedentLayout = QGridLayout()

        self.rightHBox1 = QHBoxLayout()

        self.precedentScrollArea = QScrollArea()
        self.precedentScrollArea.setWidgetResizable(True)
        self.precedentScrollArea.setFixedSize(760, 290)

        self.precedentScrollWidget = QWidget()
        self.precedentScrollWidget.setLayout(self.precedentLayout)
        self.precedentScrollArea.setWidget(self.precedentScrollWidget)

        self.precedentLabel = QLabel("1. generation")
        self.precedentLabel.setFixedWidth(140)
        self.precedentLabel.setStyleSheet("font-size: 20px; font-weight: bold; color: darkgreen;")

        self.rightHBox1.addWidget(self.precedentScrollArea)
        self.rightHBox1.addSpacing(20)
        self.rightHBox1.addWidget(self.precedentLabel)

        self.rightHBox1.setAlignment(Qt.AlignTop)

        self.rightCont1 = QWidget()
        self.rightCont1.setLayout(self.rightHBox1)
        self.rightCont1.setFixedSize(920, 325)
       
        self.secondLayout = QGridLayout()

        self.rightHB = QHBoxLayout()

        self.secondScrollArea = QScrollArea()
        self.secondScrollArea.setWidgetResizable(True)
        self.secondScrollArea.setFixedSize(760, 290)

        self.secondScrollWidget = QWidget()
        self.secondScrollWidget.setLayout(self.secondLayout)
        self.secondScrollArea.setWidget(self.secondScrollWidget)

        self.secondLabel = QLabel("2. generation")
        self.secondLabel.setFixedWidth(140)
        self.secondLabel.setStyleSheet("font-size: 20px; font-weight: bold; color: darkgreen;")

        self.rightHB.addWidget(self.secondScrollArea)
        self.rightHB.addSpacing(20)
        self.rightHB.addWidget(self.secondLabel)

        self.rightHB.setAlignment(Qt.AlignTop)

        self.rightCont2 = QWidget()
        self.rightCont2.setLayout(self.rightHB)
        self.rightCont2.setFixedSize(920, 325)

        self.right_hbox2 = QHBoxLayout()
        self.right_cont3 = QWidget()

        self.load_boxes()
        self.load_selected_boxes()
       
    def load_boxes(self, weights = (0.66, 0.46, 0.05, 0.61, 0.06, 0.65, 0.48, 0.95)):
        self.boxes = []
        self.molecules.sort(reverse=True)
        for index, individual in enumerate(self.molecules):
            row = index // 3
            col = index % 3
            smiles = individual.get_smiles()
            description = individual.get_description()
            individual.set_weights(weights)
            qed = individual.get_qed()
            self.moleculeBox = self.createMoleculeBox(smiles, description, qed, index, 0)
            self.boxes.append(self.moleculeBox)
            self.layout.addWidget(self.moleculeBox, row, col)

    def load_selected_boxes(self, weights = (0.66, 0.46, 0.05, 0.61, 0.06, 0.65, 0.48, 0.95)):
        self.selectedBoxes = []
        self.selected_molecules.sort(reverse=True)
        for index, individual in enumerate(self.selected_molecules):
            row = index // 3
            col = index % 3
            smiles = individual.get_smiles()
            description = individual.get_description()
            individual.set_weights(weights)
            qed = individual.get_qed()
            self.selectedMoleculeBox = self.createMoleculeBox(smiles, description, qed, index, 1)
            self.selectedBoxes.append(self.selectedMoleculeBox)
            self.precedentLayout.addWidget(self.selectedMoleculeBox, row, col)

    def load_new_generation(self, weights = (0.66, 0.46, 0.05, 0.61, 0.06, 0.65, 0.48, 0.95)):
        self.newGenerationBoxes = []
        if len(self.new_generation_molecules) > 0:
            self.new_generation_molecules.sort(reverse=True)
            for index, individual in enumerate(self.new_generation_molecules):
                row = index // self.columnsPerRow
                col = index % self.columnsPerRow
                smiles = individual.get_smiles()
                description = individual.get_description()
                individual.set_weights(weights)
                qed = individual.get_qed()
                self.newGenerationMoleculeBox = self.createMoleculeBox(smiles, description, qed, index, -1)
                self.newGenerationBoxes.append(self.newGenerationMoleculeBox)
                self.secondLayout.addWidget(self.newGenerationMoleculeBox, row, col)
           
                self.bestBox.deleteLater()
                self.bestBox = self.createMoleculeBox(self.new_generation_molecules[0].get_smiles(), "Current best", self.new_generation_molecules[0].get_qed(), 0, -1)
                self.bestBox.setAlignment(Qt.AlignCenter)
                self.right_hbox2.insertWidget(1, self.bestBox)
       
    def removeBoxes(self):
        for box in self.boxes:
            self.layout.removeWidget(box)
            box.deleteLater()
        self.boxes = []

    def removeSelectedBoxes(self):
        for selectedBox in self.selectedBoxes:
            self.precedentLayout.removeWidget(selectedBox)
            selectedBox.deleteLater()
        self.selectedBoxes = []

    def removeNewGenerationBoxes(self):
        for newGenerationBox in self.newGenerationBoxes:
            self.secondLayout.removeWidget(newGenerationBox)
            newGenerationBox.deleteLater()
        self.newGenerationBoxes = []

    def getSelectionWidget(self):
        return self.container

    def getPrecedentScrollArea(self):
        return self.rightCont1

    def getSecondScrollArea(self):
        return self.rightCont2

    def getBest(self):
        return self.right_cont3

    def createMoleculeBox(self, smiles, description, qed, index, ind):
        box = ClickableGroupBox(self, index, ind)
        box.setFixedWidth(230)
        boxLayout = QVBoxLayout()
        mol = Chem.MolFromSmiles(smiles)
        molImage = Draw.MolToImage(mol, size=(200, 200))
        qimage = QImage(molImage.tobytes(), molImage.width, molImage.height, molImage.width * 3, QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        imageLabel = QLabel()
        imageLabel.setPixmap(pixmap)
        descriptionLabel = QLabel(description + "\n" + "QED: " + str(round(qed, 4)))
        boxLayout.addWidget(imageLabel)
        boxLayout.addWidget(descriptionLabel)
        box.setLayout(boxLayout)

        box.setStyleSheet(f"""
            QGroupBox {{
                background-color: rgb(255, 255, 255);  
                border: 2px solid green;                
                border-radius: 15px;                    
                padding: 10px;                          
            }}
        """)

        shadowEffect = QGraphicsDropShadowEffect()
        shadowEffect.setOffset(5, 5)              
        shadowEffect.setBlurRadius(15)            
        shadowEffect.setColor(QColor(0, 0, 0, 160))
        box.setGraphicsEffect(shadowEffect)
        return box
   
    def onSelectAllButtonClicked(self):
        if self.application.block_transfer:
            return
        self.removeBoxes()
        self.removeSelectedBoxes()
        for i in range(len(self.molecules)):
            self.selected_molecules.append(self.molecules[i])
            # self.molecules.pop(i)
        self.molecules = []
        self.load_boxes(tuple(self.application.slider_values))
        self.load_selected_boxes(tuple(self.application.slider_values))

    def add_to_catalogue(self, smiles, description):
        molecule = None
        try:
            molecule = Chem.MolFromSmiles(smiles)
        except ValueError:
            return
        if molecule is None:
            return
        if not description:
            description = "Unknown"
       
        self.removeBoxes()
        self.removeSelectedBoxes()
        self.molecules.append(Individual(smiles, description, self.application.slider_values))
        with open('opt/single_objective/comb/drug_discovery_problem/data/molecules.json', 'r') as file:
            data = json.load(file)
        data.append({
            "SMILES": smiles,
            "Description": description
        })
        with open('opt/single_objective/comb/drug_discovery_problem/data/molecules.json', 'w') as file:
            json.dump(data, file, indent = 4)
        self.load_boxes()
        self.load_selected_boxes()

    def on_generate_button_clicked(self):
        self.save_label.setStyleSheet("color: transparent; font-style: italic;")
        self.removeSelectedBoxes()
        self.selected_molecules = []
        for ind in self.new_generation_molecules:
            self.selected_molecules.append(Individual(ind.get_smiles(), ind.get_description(), tuple(self.application.slider_values)))
        self.load_selected_boxes(tuple(self.application.slider_values))
        self.removeNewGenerationBoxes()

        self.new_generation_molecules = genetic_algorithm(
            self.selected_molecules,
            True,
            self.application.number_of_generations,
            self.application.roulette_selection,
            self.application.tournament_size,
            self.application.elitism_size,
            self.application.mutation_probability,
            self.application.mi,
            self.individual_label,
            self.individual_progress
        )

        self.load_new_generation(tuple(self.application.slider_values))
        labelText = self.secondLabel.text()
        self.precedentLabel.setText(labelText)
        # Regular expression to match a number at the start of the string
        match = re.match(r'^\d+', labelText)
        # Check if a match was found and extract the number
        labelNumber = int(match.group(0)) + 1
        self.secondLabel.setText(str(labelNumber) + ". generation")
        self.generation_label.setText(f"Generation: {labelNumber}/{self.application.number_of_generations}")
        self.generation_progress.setValue(labelNumber)

    def on_final_button_clicked(self):
        self.save_label.setStyleSheet("color: transparent; font-style: italic;")
        labelText = self.secondLabel.text()
        # Regular expression to match a number at the start of the string
        match = re.match(r'^\d+', labelText)
        # Check if a match was found and extract the number
        labelNumber = int(match.group(0))
        for _ in range(self.application.number_of_generations - labelNumber):
            self.on_generate_button_clicked()

    def on_save_button_clicked(self):
        formattedDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('opt/single_objective/comb/drug_discovery_problem/results/best_candidate_molecules.txt', 'a') as candidatesFile:
            candidatesFile.write(f"SMILES: {self.new_generation_molecules[0].get_smiles()}\nQED: {round(self.new_generation_molecules[0].get_qed(), 4)}\nDate created: {formattedDatetime}\nParameter weights:")
            for value in list(self.new_generation_molecules[0].getWeights()):
                candidatesFile.write(f"{value} ")
            candidatesFile.write("\n-------------------------------------------\n")
        self.save_label.setStyleSheet("color: green; font-style: italic;")

        # Create a QMessageBox
        msgBox = QMessageBox(self)
        # Set the icon for the dialog
        msgBox.setIcon(QMessageBox.Question)
        # Set the window title
        msgBox.setWindowTitle("Population diversity")
        # Set the message in the dialog
        msgBox.setText("Do you want to calculate Tanimoto similarity coefficient for current generation?")
        # Add Yes and No buttons
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # Show the message box and capture the response
        response = msgBox.exec_()
        if response == QMessageBox.Yes:
            self.tanimoto() 
        
        # Create a QMessageBox
        msgBoxAvg = QMessageBox(self)
        # Set the icon for the dialog
        msgBoxAvg.setIcon(QMessageBox.Question)
        # Set the window title
        msgBoxAvg.setWindowTitle("Average QED coefficient")
        # Set the message in the dialog
        msgBoxAvg.setText("Do you want to average QED coefficient for current generation?")
        # Add Yes and No buttons
        msgBoxAvg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # Show the message box and capture the response
        responseAvg = msgBoxAvg.exec_()
        if responseAvg == QMessageBox.Yes:
            self.calculateAverageQED()

    def tanimoto(self):
        smilesList = [s.get_smiles() for s in self.new_generation_molecules]
        mols = [Chem.MolFromSmiles(s) for s in smilesList]
        fingerprints = [rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, 2, nBits = 2048) for mol in mols]
        # Calculate pairwise Tanimoto similarity
        similarities = []
        for i in range(len(fingerprints)):
            for j in range(i+1, len(fingerprints)):
                similarity = FingerprintSimilarity(fingerprints[i], fingerprints[j])
                similarities.append(similarity)
        with open('opt/single_objective/comb/drug_discovery_problem/results/tanimoto.txt', 'a') as tanimotoFile:
            tanimotoFile.write("[")
            for sim in similarities:
                tanimotoFile.write(f"{sim}, ")
            tanimotoFile.write("]\n------------------------------------\n")

    def calculateAverageQED(self):
        formattedDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        coeffList = [s.get_qed() for s in self.new_generation_molecules]
        avgQED = sum(coeffList) / len(coeffList)
        with open('opt/single_objective/comb/drug_discovery_problem/results/averageQED.txt', 'a') as tanimotoFile:
            tanimotoFile.write(f"{avgQED}\n{formattedDatetime}\n------------------------------------\n")

    def on_restart_button_clicked(self):
        self.save_label.setStyleSheet("color: transparent; font-style: italic;")
        self.generation_label.setText(f"Generation: 1/{self.application.number_of_generations}")
        self.generation_progress.setValue(1)
        self.individual_label.setText(f"Individual: 0/{len(self.selected_molecules)}")
        self.individual_progress.setValue(0)
        self.removeBoxes()
        self.removeSelectedBoxes()
        self.removeNewGenerationBoxes()
        self.molecules = self.application.problem.molecules
        self.load_boxes(self.application.slider_values)
        self.application.molecules = []
        self.selected_molecules = []
        self.new_generation_molecules = []
        self.bestBox.deleteLater()
        self.generate_button.setDisabled(True)
        self.generate_button.setStyleSheet("Color: #757575;")
        self.final_button.setDisabled(True)
        self.final_button.setStyleSheet("Color: #757575;")
        self.save_button.setDisabled(True)
        self.save_button.setStyleSheet("Color: #757575;")
        self.restart_button.setDisabled(True)
        self.restart_button.setStyleSheet("Color: #757575;")
        self.load_new_generation()
        self.precedentLabel.setText("1. generation")
        self.secondLabel.setText("2. generation")
        self.application.gaParameters.launch_button.setDisabled(False)
        self.application.gaParameters.launch_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.application.gaParameters.roulette_check_box.setDisabled(False)
        self.application.gaParameters.roulette_check_box.setStyleSheet("""
            QCheckBox {
                text-decoration: none;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #777;
                border-radius: 5px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: lightgray;
                border: 2px solid gray;
            }
            QCheckBox::indicator:unchecked {
                background-color: white;
                border: 2px solid gray;
            }
        """)
        self.application.gaParameters.generation_spin.setDisabled(False)
        self.application.gaParameters.tournament_spin.setDisabled(False)
        self.application.gaParameters.elitism_spin.setDisabled(False)
        self.application.gaParameters.mutation_line_edit.setDisabled(False)
        self.application.sbmt_btn.setDisabled(False)
        self.application.res_btn.setDisabled(False)
        self.application.block_transfer = False
        while self.right_hbox2.count():
            item = self.right_hbox2.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()