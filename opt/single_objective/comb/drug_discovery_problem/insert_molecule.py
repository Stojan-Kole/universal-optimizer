from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QLineEdit, QWidget
from PyQt5.QtCore import Qt

class NewMoleculeForm:
    """
    GUI component for adding a custom molecule via SMILES input and description.
    """
    def __init__(self, application: QApplication) -> None:
        """
        Initializes the form with input fields for SMILES and description,
        and a submit button.

        :param application: The parent application
        """
        self.custom_molecule_title: QLabel = QLabel("Or, add your own molecule:", application)
        self.custom_molecule_title.setStyleSheet("font-size: 17px; font-weight: bold; border: none;")
        self.input_smiles: QLineEdit = QLineEdit(application)
        self.input_smiles.setPlaceholderText("Enter SMILES format...")
        self.input_smiles.setFixedWidth(250)
        self.input_description: QLineEdit = QLineEdit(application)
        self.input_description.setPlaceholderText("Enter name of the molecule...")
        self.input_description.setFixedWidth(250)
        self.submit_button: QPushButton = QPushButton("Add to catalogue", application)
        self.submit_button.clicked.connect(application.on_submit_button_clicked)
        self.submit_button.setFixedWidth(250)
        self.input_smiles.setStyleSheet("""
            QLineEdit {
                border: 2px solid #A0A0A0;
                border-radius: 5px;
                padding: 5px;
                margin-bottom: 10px;
            }
        """)
        self.input_description.setStyleSheet("""
            QLineEdit {
                border: 2px solid #A0A0A0;
                border-radius: 5px;
                padding: 5px;
                margin-bottom: 10px;
            }
        """)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.input_vlayout: QVBoxLayout = QVBoxLayout()
        self.input_vlayout.addWidget(self.custom_molecule_title)
        self.input_vlayout.addWidget(self.input_smiles)
        self.input_vlayout.addWidget(self.input_description)
        self.input_vlayout.addWidget(self.submit_button)
        self.container: QWidget = QWidget()
        self.container.setLayout(self.input_vlayout)
        self.container.setFixedSize(270, 200)

    def get_form(self) -> QWidget:
        """
        Returns the QWidget container holding the form.

        :return: QWidget with the input layout
        :rtype: QWidget
        """
        return self.container

    def get_input_smiles_text(self) -> str:
        """
        Returns the current text from the SMILES input field.

        :return: SMILES string entered by the user
        :rtype: str
        """
        return self.input_smiles.text()

    def get_input_description_text(self) -> str:
        """
        Returns the current text from the molecule description input field.

        :return: Description string entered by the user
        :rtype: str
        """
        return self.input_description.text()