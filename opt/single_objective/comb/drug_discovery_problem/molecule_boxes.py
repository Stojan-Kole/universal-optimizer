import json
import copy
import re
from PyQt5.QtWidgets import QApplication, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QGraphicsDropShadowEffect, QWidget, QGridLayout, QScrollArea, QPushButton, QProgressBar
from PyQt5.QtGui import QImage, QPixmap, QColor, QFont
from PyQt5.QtCore import QEvent, Qt
from rdkit import Chem
from rdkit.Chem import Draw, rdMolDescriptors
from rdkit.DataStructs import FingerprintSimilarity
from opt.single_objective.comb.drug_discovery_problem.fitness import Fitness
from opt.single_objective.comb.drug_discovery_problem.individual import Individual
from opt.single_objective.comb.drug_discovery_problem.solver import genetic_algorithm
from opt.single_objective.comb.drug_discovery_problem.mutation_info import MutationInfo
from datetime import datetime
from typing import Optional

class ClickableGroupBox(QGroupBox):
    """
    A custom QGroupBox that represents a clickable molecule box for selection and deselection
    between available and selected molecules.
    """
    def __init__(self, molecule_boxes: QWidget, index: int, role: int, parent: QWidget | None = None) -> None:
        """
        Initialize the ClickableGroupBox.

        :param molecule_boxes: Reference to the MoleculeBoxes manager.
        :param index: Index of the molecule in the corresponding list (molecules or selected_molecules).
        :param role: 0 if in main molecules list, 1 if in selected molecules list.
        :param parent: Parent widget.
        """
        super().__init__(parent)
        self.molecule_boxes = molecule_boxes
        self.index = index
        self.role = role # 0 = source (unselected), 1 = selected
       
    def mousePressEvent(self, event: QEvent) -> None:
        """
        Handles the logic of moving a molecule from one list to the other on left-click.

        If the application is not currently blocking transfer,
        and the role is valid (0 or 1), the molecule is moved to the opposite list.

        :param event: Mouse event object.
        """
        if self.molecule_boxes.application.block_transfer:
            return
        if self.role not in (0, 1):
            return

        if event.button() == Qt.LeftButton:
            self.molecule_boxes.remove_boxes()
            self.molecule_boxes.remove_selected_boxes()
            if self.role == 0:
                # Move from available to selected
                self.molecule_boxes.selected_molecules.append(self.molecule_boxes.molecules.pop(self.index))
                
            elif self.role == 1:
                # Move from selected back to available
                self.molecule_boxes.molecules.append(self.molecule_boxes.selected_molecules.pop(self.index))
                
            self.molecule_boxes.load_boxes(tuple(self.molecule_boxes.application.slider_values))
            self.molecule_boxes.load_selected_boxes(tuple(self.molecule_boxes.application.slider_values))

        super().mousePressEvent(event)

    def enterEvent(self, event: QEvent) -> None:
        """
        Highlights the SMILES label when mouse hovers over the box (if not blocked).

        :param event: Enter event object.
        """
        if not self.molecule_boxes.application.block_transfer:
            self.layout().itemAt(1).widget().setStyleSheet("color: darkgreen; font-weight: bold;")

    def leaveEvent(self, event: QEvent) -> None:
        """
        Resets the SMILES label style when mouse leaves the box (if not blocked).

        :param event: Leave event object.
        """
        if not self.molecule_boxes.application.block_transfer:
            self.layout().itemAt(1).widget().setStyleSheet("color: black; font-weight: normal;")

class MoleculeBoxes(QWidget):
    """
    A widget that displays molecule representations in scrollable boxes,
    and allows user to select molecules for the first generation of the genetic algorithm.
    """
    def __init__(self, application: QApplication) -> None:
        """
        Initializes the MoleculeBoxes widget.

        This widget provides a scrollable interface for selecting molecules 
        to be used in the first generation of a genetic algorithm. It also displays
        the resulting molecules from the 1st and 2nd generations in separate scroll areas.

        Args:
            application: The parent application instance that holds global state.
        """
        super().__init__(application)
        self.application: QApplication = application
        self.molecules: list[Individual] = application.molecules
        self.window_width: int = application.width()
        self.boxWidth = 220
        self.columns_per_row = 3
        self.layout: QGridLayout = QGridLayout()

        self.vbox: QVBoxLayout = QVBoxLayout()

        self.selection_hbox: QHBoxLayout = QHBoxLayout()

        self.selection_label: QLabel = QLabel("Select molecules for the first generation:")
        self.selection_label.setStyleSheet("font-size: 20px; font-weight: bold; padding-bottom: 10px;")

        self.select_all_button: QPushButton = QPushButton("Select all")
        self.select_all_button.setFixedWidth(100)
        self.select_all_button.setStyleSheet("""
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
        self.select_all_button.clicked.connect(self.on_select_all_button_clicked)

        self.selection_hbox.addWidget(self.selection_label)
        self.selection_hbox.addWidget(self.select_all_button)

        self.selection_container: QWidget = QWidget()
        self.selection_container.setLayout(self.selection_hbox)

        self.scroll_area: QScrollArea = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedSize(760, 290)

        self.scroll_widget: QWidget = QWidget()
        self.scroll_widget.setLayout(self.layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.vbox.addWidget(self.selection_container)
        self.vbox.addWidget(self.scroll_area)

        self.container: QWidget = QWidget()
        self.container.setLayout(self.vbox)
        self.container.setFixedSize(760, 350)

        self.selected_molecules: list[Individual] = []
        self.new_generation_molecules: list[Individual] = []

        self.precedent_layout: QGridLayout = QGridLayout()

        self.right_hbox1: QHBoxLayout = QHBoxLayout()

        self.precedent_scroll_area: QScrollArea = QScrollArea()
        self.precedent_scroll_area.setWidgetResizable(True)
        self.precedent_scroll_area.setFixedSize(760, 290)

        self.precedent_scroll_widget: QWidget = QWidget()
        self.precedent_scroll_widget.setLayout(self.precedent_layout)
        self.precedent_scroll_area.setWidget(self.precedent_scroll_widget)

        self.precedent_label: QLabel = QLabel("1. generation")
        self.precedent_label.setFixedWidth(140)
        self.precedent_label.setStyleSheet("font-size: 20px; font-weight: bold; color: darkgreen;")

        self.right_hbox1.addWidget(self.precedent_scroll_area)
        self.right_hbox1.addSpacing(20)
        self.right_hbox1.addWidget(self.precedent_label)

        self.right_hbox1.setAlignment(Qt.AlignTop)

        self.right_cont1: QWidget = QWidget()
        self.right_cont1.setLayout(self.right_hbox1)
        self.right_cont1.setFixedSize(920, 325)
       
        self.second_layout: QGridLayout = QGridLayout()

        self.right_hb: QHBoxLayout = QHBoxLayout()

        self.second_scroll_area: QScrollArea = QScrollArea()
        self.second_scroll_area.setWidgetResizable(True)
        self.second_scroll_area.setFixedSize(760, 290)

        self.second_scroll_widget: QWidget = QWidget()
        self.second_scroll_widget.setLayout(self.second_layout)
        self.second_scroll_area.setWidget(self.second_scroll_widget)

        self.second_label: QLabel = QLabel("2. generation")
        self.second_label.setFixedWidth(140)
        self.second_label.setStyleSheet("font-size: 20px; font-weight: bold; color: darkgreen;")

        self.right_hb.addWidget(self.second_scroll_area)
        self.right_hb.addSpacing(20)
        self.right_hb.addWidget(self.second_label)

        self.right_hb.setAlignment(Qt.AlignTop)

        self.right_cont2: QWidget = QWidget()
        self.right_cont2.setLayout(self.right_hb)
        self.right_cont2.setFixedSize(920, 325)

        self.right_hbox2: QHBoxLayout = QHBoxLayout()
        self.right_cont3: QWidget = QWidget()

        self.load_boxes()
        self.load_selected_boxes()
       
    def load_boxes(self, weights: tuple[float, ...] = (0.66, 0.46, 0.05, 0.61, 0.06, 0.65, 0.48, 0.95)) -> None:
        """
        Load unselected molecule boxes into the main grid layout.

        Args:
            weights: Weights used to compute the QED score for each molecule.
        """
        self.boxes: list[ClickableGroupBox] = []
        self.molecules.sort(reverse=True)
        for index, individual in enumerate(self.molecules):
            row: int = index // self.columns_per_row
            col: int = index % self.columns_per_row
            smiles: str = individual.get_smiles()
            description: str = individual.get_description()
            individual.set_weights(weights)
            qed: float = individual.get_qed()
            self.molecule_box: ClickableGroupBox = self.create_molecule_box(smiles, description, qed, index, 0)
            self.boxes.append(self.molecule_box)
            self.layout.addWidget(self.molecule_box, row, col)

    def load_selected_boxes(self, weights: tuple[float, ...] = (0.66, 0.46, 0.05, 0.61, 0.06, 0.65, 0.48, 0.95)) -> None:
        """
        Load selected molecules into their display area.

        Args:
            weights: Weights used to compute the QED score for each selected molecule.
        """
        self.selected_boxes: list[ClickableGroupBox] = []
        self.selected_molecules.sort(reverse=True)
        for index, individual in enumerate(self.selected_molecules):
            row: int = index // self.columns_per_row
            col: int = index % self.columns_per_row
            smiles: str = individual.get_smiles()
            description: str = individual.get_description()
            individual.set_weights(weights)
            qed: float = individual.get_qed()
            self.selectedMoleculeBox: ClickableGroupBox = self.create_molecule_box(smiles, description, qed, index, 1)
            self.selected_boxes.append(self.selectedMoleculeBox)
            self.precedent_layout.addWidget(self.selectedMoleculeBox, row, col)

    def load_new_generation(self, weights: tuple[float, ...] = (0.66, 0.46, 0.05, 0.61, 0.06, 0.65, 0.48, 0.95)) -> None:
        """
        Load boxes for the newly generated molecules.

        Also updates the current best molecule display.

        Args:
            weights: Weights used to compute the QED score for each new generation molecule.
        """
        self.new_generation_boxes: list[ClickableGroupBox] = []
        if len(self.new_generation_molecules) > 0:
            self.new_generation_molecules.sort(reverse=True)
            for index, individual in enumerate(self.new_generation_molecules):
                row: int = index // self.columns_per_row
                col: int = index % self.columns_per_row
                smiles: str = individual.get_smiles()
                description: str = individual.get_description()
                individual.set_weights(weights)
                qed: float = individual.get_qed()
                self.new_generation_molecule_box: ClickableGroupBox = self.create_molecule_box(smiles, description, qed, index, -1)
                self.new_generation_boxes.append(self.new_generation_molecule_box)
                self.second_layout.addWidget(self.new_generation_molecule_box, row, col)
           
                self.best_box.deleteLater()
                self.best_box = self.create_molecule_box(self.new_generation_molecules[0].get_smiles(), "Current best", self.new_generation_molecules[0].get_qed(), 0, -1)
                self.best_box.setAlignment(Qt.AlignCenter)
                self.right_hbox2.insertWidget(1, self.best_box)
       
    def remove_boxes(self) -> None:
        """
        Remove all unselected molecule boxes from the layout.
        """
        for box in self.boxes:
            self.layout.removeWidget(box)
            box.deleteLater()
        self.boxes = []

    def remove_selected_boxes(self) -> None:
        """
        Remove all selected molecule boxes.
        """
        for selected_box in self.selected_boxes:
            self.precedent_layout.removeWidget(selected_box)
            selected_box.deleteLater()
        self.selected_boxes = []

    def remove_new_generation_boxes(self) -> None:
        """
        Remove all new generation molecule boxes.
        """
        for new_generation_box in self.new_generation_boxes:
            self.second_layout.removeWidget(new_generation_box)
            new_generation_box.deleteLater()
        self.new_generation_boxes = []

    def get_selection_widget(self) -> QWidget:
        """
        Get the widget that contains the molecule selection interface.

        Returns:
            QWidget: Widget with selectable molecule grid.
        """
        return self.container

    def get_precedent_scroll_area(self) -> QWidget:
        """
        Get the widget displaying selected molecules.

        Returns:
            QWidget: Widget containing precedent scroll area.
        """
        return self.right_cont1

    def get_second_scroll_area(self) -> QWidget:
        """
        Get the widget displaying new generation molecules.

        Returns:
            QWidget: Widget containing scroll area for subsequent generation.
        """
        return self.right_cont2

    def get_best(self) -> QWidget:
        """
        Get the widget displaying the current best molecule.

        Returns:
            QWidget: Widget showing the best molecule of the current generation.
        """
        return self.right_cont3

    def create_molecule_box(self, smiles: str, description: str, qed: float, index: int, ind: int) -> ClickableGroupBox:
        """
        Create a styled box widget representing a molecule with its image and properties.
        """
        box: ClickableGroupBox = ClickableGroupBox(self, index, ind)
        box.setFixedWidth(230)
        box_layout: QVBoxLayout = QVBoxLayout()
        mol: Mol = Chem.MolFromSmiles(smiles)
        mol_image: PILImage = Draw.MolToImage(mol, size=(200, 200))
        qimage: QImage = QImage(mol_image.tobytes(), mol_image.width, mol_image.height, mol_image.width * 3, QImage.Format_RGB888)
        pixmap: QPixmap = QPixmap(qimage)
        image_label: QLabel = QLabel()
        image_label.setPixmap(pixmap)
        description_label: QLabel = QLabel(description + "\n" + "QED: " + str(round(qed, 4)))
        box_layout.addWidget(image_label)
        box_layout.addWidget(description_label)
        box.setLayout(box_layout)

        box.setStyleSheet(f"""
            QGroupBox {{
                background-color: rgb(255, 255, 255);  
                border: 2px solid green;                
                border-radius: 15px;                    
                padding: 10px;                          
            }}
        """)

        shadow_effect: QGraphicsDropShadowEffect = QGraphicsDropShadowEffect()
        shadow_effect.setOffset(5, 5)              
        shadow_effect.setBlurRadius(15)            
        shadow_effect.setColor(QColor(0, 0, 0, 160))
        box.setGraphicsEffect(shadow_effect)
        return box
   
    def on_select_all_button_clicked(self) -> None:
        """
        Move all molecules from the current list to the selected list and refresh the display.
        """
        if self.application.block_transfer:
            return
        self.remove_boxes()
        self.remove_selected_boxes()
        for i in range(len(self.molecules)):
            self.selected_molecules.append(self.molecules[i])
        self.molecules = []
        self.load_boxes(tuple(self.application.slider_values))
        self.load_selected_boxes(tuple(self.application.slider_values))

    def add_to_catalogue(self, smiles: str, description: Optional[str]) -> None:
        """
        Add a new molecule to the catalogue and save it to the JSON file.
        """
        molecule = None
        try:
            molecule = Chem.MolFromSmiles(smiles)
        except ValueError:
            return
        if molecule is None:
            return
        if not description:
            description = "Unknown"
       
        self.remove_boxes()
        self.remove_selected_boxes()
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

    def on_generate_button_clicked(self) -> None:
        """
        Generate a new generation using selected molecules and update all related UI elements.
        """
        self.save_label.setStyleSheet("color: transparent; font-style: italic;")
        self.remove_selected_boxes()
        self.selected_molecules = []
        for ind in self.new_generation_molecules:
            self.selected_molecules.append(Individual(ind.get_smiles(), ind.get_description(), tuple(self.application.slider_values)))
        self.load_selected_boxes(tuple(self.application.slider_values))
        self.remove_new_generation_boxes()

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
        label_text: str = self.second_label.text()
        self.precedent_label.setText(label_text)
        # Regular expression to match a number at the start of the string
        match = re.match(r'^\d+', label_text)
        # Check if a match was found and extract the number
        label_number: int = int(match.group(0)) + 1
        self.second_label.setText(str(label_number) + ". generation")
        self.generation_label.setText(f"Generation: {label_number}/{self.application.number_of_generations}")
        self.generation_progress.setValue(label_number)

    def on_final_button_clicked(self) -> None:
        """
        Complete the full number of generations using the 'Generate' button logic.
        """
        self.save_label.setStyleSheet("color: transparent; font-style: italic;")
        label_text = self.second_label.text()
        # Regular expression to match a number at the start of the string
        match = re.match(r'^\d+', label_text)
        # Check if a match was found and extract the number
        label_number = int(match.group(0))
        for _ in range(self.application.number_of_generations - label_number):
            self.on_generate_button_clicked()

    def on_save_button_clicked(self) -> None:
        """
        Save the best candidate molecule to a file and prompt user for additional statistics.
        """
        formatted_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('opt/single_objective/comb/drug_discovery_problem/results/best_candidate_molecules.txt', 'a') as candidates_file:
            candidates_file.write(f"SMILES: {self.new_generation_molecules[0].get_smiles()}\nQED: {round(self.new_generation_molecules[0].get_qed(), 4)}\nDate created: {formatted_time}\nParameter weights:")
            for value in list(self.new_generation_molecules[0].get_weights()):
                candidates_file.write(f"{value} ")
            candidates_file.write("\n-------------------------------------------\n")
        self.save_label.setStyleSheet("color: green; font-style: italic;")

        # Create a QMessageBox
        msg_box: QMessageBox = QMessageBox(self)
        # Set the icon for the dialog
        msg_box.setIcon(QMessageBox.Question)
        # Set the window title
        msg_box.setWindowTitle("Population diversity")
        # Set the message in the dialog
        msg_box.setText("Do you want to calculate Tanimoto similarity coefficient for current generation?")
        # Add Yes and No buttons
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # Show the message box and capture the response
        if msg_box.exec_() == QMessageBox.Yes:
            self.tanimoto() 
        
        # Create a QMessageBox
        msg_box_avg: QMessageBox = QMessageBox(self)
        # Set the icon for the dialog
        msg_box_avg.setIcon(QMessageBox.Question)
        # Set the window title
        msg_box_avg.setWindowTitle("Average QED coefficient")
        # Set the message in the dialog
        msg_box_avg.setText("Do you want to average QED coefficient for current generation?")
        # Add Yes and No buttons
        msg_box_avg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # Show the message box and capture the response
        if msg_box_avg.exec_() == QMessageBox.Yes:
            self.calculate_average_qed()

    def tanimoto(self) -> None:
        """
        Calculate pairwise Tanimoto similarity coefficients between molecules in the
        current new generation and save the results to a file.
        """
        smiles_list: list[str] = [s.get_smiles() for s in self.new_generation_molecules]
        mols: list[Mol] = [Chem.MolFromSmiles(s) for s in smiles_list]
        fingerprints: list[ExplicitBitVect] = [rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, 2, nBits = 2048) for mol in mols]
        # Calculate pairwise Tanimoto similarity
        similarities: list[float] = []
        for i in range(len(fingerprints)):
            for j in range(i+1, len(fingerprints)):
                similarity: float = FingerprintSimilarity(fingerprints[i], fingerprints[j])
                similarities.append(similarity)
        with open('opt/single_objective/comb/drug_discovery_problem/results/tanimoto.txt', 'a') as tanimoto_file:
            tanimoto_file.write("[")
            for sim in similarities:
                tanimoto_file.write(f"{sim}, ")
            tanimoto_file.write("]\n------------------------------------\n")

    def calculate_average_qed(self) -> None:
        """
        Calculate the average QED coefficient for the current new generation of molecules
        and append the result with a timestamp to a file.
        """
        formatted_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        coeff_list: list[float] = [s.get_qed() for s in self.new_generation_molecules]
        avg_qed = sum(coeff_list) / len(coeff_list)
        with open('opt/single_objective/comb/drug_discovery_problem/results/averageQED.txt', 'a') as tanimoto_file:
            tanimoto_file.write(f"{avg_qed}\n{formatted_time}\n------------------------------------\n")

    def on_restart_button_clicked(self) -> None:
        """
        Reset the entire optimization process to the initial state.
        This method is typically called when the 'Restart' button is clicked.
        It clears molecule displays, resets all controls and progress indicators,
        and prepares the interface for a fresh run.
        """
        self.save_label.setStyleSheet("color: transparent; font-style: italic;")
        self.generation_label.setText(f"Generation: 1/{self.application.number_of_generations}")
        self.generation_progress.setValue(1)
        self.individual_label.setText(f"Individual: 0/{len(self.selected_molecules)}")
        self.individual_progress.setValue(0)
        self.remove_boxes()
        self.remove_selected_boxes()
        self.remove_new_generation_boxes()
        self.molecules = self.application.problem.molecules
        self.load_boxes(self.application.slider_values)
        self.application.molecules = []
        self.selected_molecules = []
        self.new_generation_molecules = []
        self.best_box.deleteLater()
        self.generate_button.setDisabled(True)
        self.generate_button.setStyleSheet("Color: #757575;")
        self.final_button.setDisabled(True)
        self.final_button.setStyleSheet("Color: #757575;")
        self.save_button.setDisabled(True)
        self.save_button.setStyleSheet("Color: #757575;")
        self.restart_button.setDisabled(True)
        self.restart_button.setStyleSheet("Color: #757575;")
        self.load_new_generation()
        self.precedent_label.setText("1. generation")
        self.second_label.setText("2. generation")
        self.application.ga_parameters.launch_button.setDisabled(False)
        self.application.ga_parameters.launch_button.setStyleSheet("""
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
        self.application.ga_parameters.roulette_check_box.setDisabled(False)
        self.application.ga_parameters.roulette_check_box.setStyleSheet("""
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
        self.application.ga_parameters.generation_spin.setDisabled(False)
        self.application.ga_parameters.tournament_spin.setDisabled(False)
        self.application.ga_parameters.elitism_spin.setDisabled(False)
        self.application.ga_parameters.mutation_line_edit.setDisabled(False)
        self.application.sbmt_btn.setDisabled(False)
        self.application.res_btn.setDisabled(False)
        self.application.block_transfer = False
        while self.right_hbox2.count():
            item = self.right_hbox2.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()