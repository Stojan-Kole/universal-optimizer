from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QWidget, QPushButton
from PyQt5.QtCore import Qt

from opt.single_objective.comb.drug_discovery_problem.molecule_boxes import MoleculeBoxes

class HyperParameters:    
    """
    GUI widget for adjusting hyperparameter weights via sliders.

    :param application: Reference to the main QApplication object 
    """
    def __init__(self, application: QApplication) -> None:
        """
        Initializes the layout, labels, sliders, and reset button for hyperparameter adjustment.

        :param application: Main application object containing shared state
        :type application: QApplication
        """
        self.application: QApplication = application
        self.molecule_boxes: MoleculeBoxes = application.molecule_boxes
        self.names: list[str] = ['MW', 'ALOGP', 'HBA', 'HBD', 'PSA', 'ROTB', 'AROM', 'ALERTS']
        self.default_values: list[float] = [0.66, 0.46, 0.05, 0.61, 0.06, 0.65, 0.48, 0.95]
        self.h_boxes: list[QHBoxLayout] = []
        self.layout: QVBoxLayout = QVBoxLayout()
        self.label: QLabel = QLabel("Adjust hyperparameter's weights", application)
        self.label.setStyleSheet("font-size: 17px; font-weight: bold; border: none; margin-top: 5px;")

        self.reset_button: QPushButton = QPushButton("Reset to defaults", application)
        self.reset_button.clicked.connect(self.on_reset_button_clicked)
        self.reset_button.setFixedWidth(120)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #6495ED;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0047AB;
            }
        """)
        self.header_layout: QHBoxLayout = QHBoxLayout()
        self.header_layout.addWidget(self.label)
        self.header_layout.addWidget(self.reset_button)

        self.layout.addLayout(self.header_layout)
        self.layout.addSpacing(20)

        for i, (name, default) in enumerate(zip(self.names, self.default_values)):
            self.h_box: QHBoxLayout = QHBoxLayout()

            self.param_label: QLabel = QLabel(name + ": " + str(default), application)

            self.param_slider: QSlider = QSlider(Qt.Horizontal, application)
            self.param_slider.setRange(0, 100)
            self.param_slider.setTickInterval(1) 
            self.param_slider.setFixedWidth(350)
            self.param_slider.setValue(int(default * 100))
            self.param_slider.valueChanged.connect(lambda value, idx = i: self.update_param_label(idx))
            self.param_slider.setStyleSheet("""
                border: none;               
            """)

            self.h_box.addWidget(self.param_label)
            self.h_box.addWidget(self.param_slider)
            self.h_boxes.append(self.h_box)
            self.layout.addLayout(self.h_box)

        self.container: QWidget = QWidget()
        self.container.setLayout(self.layout)
        self.container.setStyleSheet("padding-top: 0px;")
            
    def update_param_label(self, idx: int) -> None:
        """
        Updates the label for a hyperparameter based on the slider value.
        Also triggers updates of molecule boxes based on new weights.

        :param index: Index of the slider and label to update
        :type index: int
        """
        value: float = self.h_boxes[idx].itemAt(1).widget().value()
        name: str = self.names[idx]
        label: QLabel = self.h_boxes[idx].itemAt(0).widget()
        label.setText(f"{name}: {value/100}")
        self.application.slider_values[idx] = value/100
        self.molecule_boxes.remove_boxes()
        self.molecule_boxes.remove_selected_boxes()
        slider_values: list[float] = []
        for box in self.h_boxes:
            slider_values.append(box.itemAt(1).widget().value())
        self.molecule_boxes.load_boxes(tuple([value/100 for value in slider_values]))
        self.molecule_boxes.load_selected_boxes(tuple([value/100 for value in slider_values]))

    def on_reset_button_clicked(self) -> None:
        """
        Resets all sliders to their default values and updates the display.
        """
        for i in range(len(self.names)):
            self.h_boxes[i].itemAt(1).widget().setValue(int(self.default_values[i] * 100))

    def get_sliders_widget(self) -> QWidget:
        """
        Returns the QWidget containing the full layout for sliders.

        :return: The widget containing sliders and labels
        :rtype: QWidget
        """
        return self.container