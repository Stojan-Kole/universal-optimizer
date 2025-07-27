from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QWidget, QPushButton, QLineEdit, QCheckBox, QProgressBar
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from opt.single_objective.comb.drug_discovery_problem.solver import genetic_algorithm
from opt.single_objective.comb.drug_discovery_problem.mutation_info import MutationInfo

class GAParameters:
    """
    Widget component for configuring Genetic Algorithm (GA) parameters.

    :param application: Main application instance to interact with GA controls.
    :type application: QApplication
    """
    def __init__(self, application: QApplication) -> None:
        """
        Initialize the GAParameters widget and prepare all input fields.

        :param application: Reference to the main application
        :type application: QApplication
        """
        self.application: QApplication = application
        self.main_layout: QHBoxLayout = QHBoxLayout()
        self.left_layout: QVBoxLayout = QVBoxLayout()

        self.ga_label: QLabel = QLabel("Parameters for genetic algorithm:", application)
        self.ga_label.setStyleSheet("font-size: 17px; font-weight: bold; border: none; margin-bottom: 10px;")

        self.num_gen_label: QLabel = QLabel("Number of generations: ", application)
        self.tournament_size_label: QLabel = QLabel("Tournament size: ", application)
        self.elitism_size_label: QLabel = QLabel("Elitism size: ", application)
        self.mutation_probability_label: QLabel = QLabel("Mutation probability: ", application)

        self.generation_spin: QSpinBox = QSpinBox(application)
        self.generation_spin.setMaximum(200)
        self.generation_spin.setFixedWidth(70)
        self.generation_spin.setValue(100)

        self.roulette_check_box: QCheckBox = QCheckBox("Roulette selection", application)
        self.roulette_check_box.stateChanged.connect(self.on_roulette_changed)
        self._set_checkbox_style(self.roulette_check_box)

        self.tournament_spin: QSpinBox = QSpinBox(application)
        self.tournament_spin.setMaximum(100)
        self.tournament_spin.setFixedWidth(70)
        self.tournament_spin.setValue(7)

        self.elitism_spin: QSpinBox = QSpinBox(application)
        self.elitism_spin.setMaximum(100)
        self.elitism_spin.setFixedWidth(70)
        self.elitism_spin.setValue(2)

        self.mutation_line_edit: QLineEdit = QLineEdit(application)
        self.mutation_line_edit.setFixedWidth(70)
        self.mutation_line_edit.setText("0.05")

        self.h1: QHBoxLayout = QHBoxLayout()
        self.h1.addWidget(self.num_gen_label)
        self.h1.addWidget(self.generation_spin)
        self.h1_cont: QWidget = QWidget()
        self.h1_cont.setLayout(self.h1)
        self.h1_cont.setFixedSize(300, 37)

        self.h2: QHBoxLayout = QHBoxLayout()
        self.h2.addWidget(self.tournament_size_label)
        self.h2.addWidget(self.tournament_spin)
        self.h2.addSpacing(20)
        self.h2.addWidget(self.roulette_check_box)
        self.h2_cont: QWidget = QWidget()
        self.h2_cont.setLayout(self.h2)
        self.h2_cont.setFixedSize(540, 37)

        self.h3: QHBoxLayout = QHBoxLayout()
        self.h3.addWidget(self.elitism_size_label)
        self.h3.addWidget(self.elitism_spin)
        self.h3_cont: QWidget = QWidget()
        self.h3_cont.setLayout(self.h3)
        self.h3_cont.setFixedSize(300, 37)

        self.h4: QHBoxLayout = QHBoxLayout()
        self.h4.addWidget(self.mutation_probability_label)
        self.h4.addWidget(self.mutation_line_edit)
        self.h4_cont: QWidget = QWidget()
        self.h4_cont.setLayout(self.h4)
        self.h4_cont.setFixedSize(300, 37)

        self.left_layout.addWidget(self.ga_label)
        self.left_layout.addWidget(self.h1_cont)
        self.left_layout.addWidget(self.h2_cont)
        self.left_layout.addWidget(self.h3_cont)
        self.left_layout.addWidget(self.h4_cont)
        self.left_layout.setAlignment(Qt.AlignLeft)

        self.right_layout: QVBoxLayout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignCenter)

        self.launch_button: QPushButton = QPushButton("Launch search!", application)
        self.launch_button.setFixedWidth(200)
        self._set_button_style(self.launch_button)
        self.launch_button.clicked.connect(self.on_launch_button_clicked)

        self.right_layout.addWidget(self.launch_button)

        self.left_wrapper: QWidget = QWidget()
        self.left_wrapper.setLayout(self.left_layout)

        self.right_wrapper: QWidget = QWidget()
        self.right_wrapper.setLayout(self.right_layout)
        self.right_wrapper.setFixedWidth(230)

        self.main_layout.addWidget(self.left_wrapper)
        self.main_layout.addWidget(self.right_wrapper)
        self.container: QWidget = QWidget()
        self.container.setLayout(self.main_layout)
        self.container.setFixedSize(760, 200)

    def _set_checkbox_style(self, checkbox: QCheckBox) -> None:
        """
        Apply visual styling to a selection method checkbox.

        :param checkbox: The checkbox widget to style
        :type checkbox: QCheckBox
        """
        checkbox.setStyleSheet("""
            QCheckBox { text-decoration: none; }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #777;
                border-radius: 5px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: lightgray;
                border: 2px solid green;
            }
            QCheckBox::indicator:unchecked {
                background-color: white;
                border: 2px solid #777;
            }
        """)

    def _set_button_style(self, button: QPushButton) -> None:
        """
        Apply consistent visual styling to the launch button.

        :param button: The QPushButton to style
        :type button: QPushButton
        """
        button.setStyleSheet("""
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

    def on_roulette_changed(self, state: int) -> None:
        """
        Callback function triggered when the roulette checkbox is toggled.

        Enables or disables the tournament size input field based on selection mode.

        :param state: The new state of the checkbox (Qt.Checked or Qt.Unchecked)
        :type state: int
        :rtype: None
        """
        if state == 2:
            self.tournament_spin.setDisabled(True)
        else:
            self.tournament_spin.setDisabled(False)

    def get_GA_parameters_widget(self) -> QWidget:
        """
        Returns the main widget containing all GA parameter controls.
        
        :return: QWidget with all GA parameter inputs
        :rtype: QWidget
        """
        return self.container

    def on_launch_button_clicked(self) -> None:
        """
        Handles the event when the user clicks the 'Launch' button to start the genetic algorithm.

        This method performs the following:
        1. Retrieves the selected configuration parameters from the GUI.
        2. Initializes and runs the genetic algorithm using the solver module.
        3. Loads and displays the newly generated population of molecules.
        4. Updates the GUI state to reflect that the optimization process has started:
        - Enables buttons and labels for further interaction.
        - Sets the progress and generation counter.
        - Prepares the next generation environment.

        Raises:
            ValueError: If input parameters are missing or invalid.
        """
        # molecule_boxes is a reference to the right half of the scene
        molecule_boxes: MoleculeBoxes = self.application.molecule_boxes

        molecule_boxes.generate_button: QPushButton = QPushButton("Generate next", molecule_boxes.application)
        molecule_boxes.generate_button.setFixedWidth(150)
        molecule_boxes.generate_button.clicked.connect(molecule_boxes.on_generate_button_clicked)
        molecule_boxes.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        molecule_boxes.final_button: QPushButton = QPushButton("Jump to final")
        molecule_boxes.final_button.setFixedWidth(150)
        molecule_boxes.final_button.clicked.connect(molecule_boxes.on_final_button_clicked)
        molecule_boxes.final_button.setStyleSheet("""
            QPushButton {
                background-color: #6495ED;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0047AB;
            }
        """)

        molecule_boxes.save_button: QPushButton = QPushButton("Save the best")
        molecule_boxes.save_button.setFixedWidth(150)
        molecule_boxes.save_button.clicked.connect(molecule_boxes.on_save_button_clicked)
        molecule_boxes.save_button.setStyleSheet("""
            QPushButton {
                background-color: #606060;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: black;
            }
        """)

        molecule_boxes.save_label: QLabel = QLabel("Saved!")
        molecule_boxes.save_label.setStyleSheet("color: transparent; font-style: italic;")

        molecule_boxes.save_box: QHBoxLayout = QHBoxLayout()
        molecule_boxes.save_box.addSpacing(-7)
        molecule_boxes.save_box.addWidget(molecule_boxes.save_button)
        molecule_boxes.save_box.addSpacing(10)
        molecule_boxes.save_box.addWidget(molecule_boxes.save_label)

        molecule_boxes.save_cnt: QWidget = QWidget()
        molecule_boxes.save_cnt.setLayout(molecule_boxes.save_box)
        molecule_boxes.save_cnt.setFixedWidth(350)

        molecule_boxes.restart_button: QPushButton = QPushButton("Restart analysis")
        molecule_boxes.restart_button.setFixedWidth(150)
        molecule_boxes.restart_button.clicked.connect(molecule_boxes.on_restart_button_clicked)
        molecule_boxes.restart_button.setStyleSheet("""
            QPushButton {
                background-color: #ff4040;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: red;
            }
        """)

        molecule_boxes.right_vbox3: QVBoxLayout = QVBoxLayout()
        molecule_boxes.right_vbox3.addWidget(molecule_boxes.generate_button)
        molecule_boxes.right_vbox3.addSpacing(13)
        molecule_boxes.right_vbox3.addWidget(molecule_boxes.final_button)
        molecule_boxes.right_vbox3.addWidget(molecule_boxes.save_cnt)
        molecule_boxes.right_vbox3.addWidget(molecule_boxes.restart_button)

        molecule_boxes.right_btn_cnt: QWidget = QWidget()
        molecule_boxes.right_btn_cnt.setLayout(molecule_boxes.right_vbox3)
        molecule_boxes.right_btn_cnt.setFixedSize(350, 215)

        molecule_boxes.best_box: MoleculeBox = molecule_boxes.create_molecule_box("", "To be determined", 0.0, 0, -1)
        molecule_boxes.best_box.setAlignment(Qt.AlignCenter)

        self.launch_button.setDisabled(True)
        self.launch_button.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        # Necessary parameters for genetic algorithm
        self.application.roulette_selection = self.roulette_check_box.isChecked()
        self.application.number_of_generations = self.generation_spin.value()
        self.application.tournament_size = self.tournament_spin.value()
        self.application.elitism_size = self.elitism_spin.value()
        self.application.mutation_probability = float(self.mutation_line_edit.text())

        molecule_boxes.progress_vbox: QVBoxLayout = QVBoxLayout()

        molecule_boxes.generation_label: QLabel = QLabel(f"Generation: 2/{self.application.number_of_generations}")
        molecule_boxes.generation_label.setStyleSheet("color: blue; font-style: bold;")

        molecule_boxes.generation_progress: QProgressBar = QProgressBar()
        molecule_boxes.generation_progress.setRange(0, self.application.number_of_generations)
        molecule_boxes.generation_progress.setValue(2)

        molecule_boxes.individual_label: QLabel = QLabel(f"Individual: 0/{len(molecule_boxes.selected_molecules)}")
        molecule_boxes.individual_label.setStyleSheet("color: blue; font-style: bold;")

        molecule_boxes.individual_progress: QProgressBar = QProgressBar()
        molecule_boxes.individual_progress.setRange(0, len(molecule_boxes.selected_molecules))
        molecule_boxes.individual_progress.setValue(1)

        molecule_boxes.progress_vbox.addWidget(molecule_boxes.generation_label)
        molecule_boxes.progress_vbox.addWidget(molecule_boxes.generation_progress)
        molecule_boxes.progress_vbox.addSpacing(30)
        molecule_boxes.progress_vbox.addWidget(molecule_boxes.individual_label)
        molecule_boxes.progress_vbox.addWidget(molecule_boxes.individual_progress)

        molecule_boxes.progress_cnt: QWidget = QWidget()
        molecule_boxes.progress_cnt.setLayout(molecule_boxes.progress_vbox)
        molecule_boxes.progress_cnt.setFixedSize(350, 120)

        molecule_boxes.right_hbox2.addWidget(molecule_boxes.right_btn_cnt)
        molecule_boxes.right_hbox2.addWidget(molecule_boxes.best_box)
        molecule_boxes.right_hbox2.addSpacing(50)
        molecule_boxes.right_hbox2.addWidget(molecule_boxes.progress_cnt)
        molecule_boxes.right_hbox2.setAlignment(Qt.AlignHCenter)

        molecule_boxes.right_cont3.setLayout(molecule_boxes.right_hbox2)
        molecule_boxes.right_cont3.setFixedSize(850, 270)

        self.roulette_check_box.setDisabled(True)
        self.roulette_check_box.setStyleSheet("""
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
                background-color: lightgray;
                border: 2px solid gray;
            }
        """)
        self.generation_spin.setDisabled(True)
        self.tournament_spin.setDisabled(True)
        self.elitism_spin.setDisabled(True)
        self.mutation_line_edit.setDisabled(True)

        self.application.sbmt_btn.setDisabled(True)
        self.application.res_btn.setDisabled(True)

        self.application.block_transfer = True

        molecule_boxes.new_generation_molecules = genetic_algorithm(
            molecule_boxes.selected_molecules,
            True,
            self.application.number_of_generations,
            self.application.roulette_selection,
            self.application.tournament_size,
            self.application.elitism_size,
            self.application.mutation_probability,
            self.application.mi,
            molecule_boxes.individual_label,
            molecule_boxes.individual_progress
        )

        molecule_boxes.load_new_generation(tuple(self.application.slider_values))
        
        

