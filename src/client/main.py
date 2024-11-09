import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window properties
        self.setWindowTitle("Raspberry Pi Control Panel")
        self.setGeometry(100, 100, 400, 200)

        # Initialize layout
        layout = QVBoxLayout()

        # Start button
        start_button = QPushButton("Start", self)
        start_button.setFont(QFont("Arial", 14, QFont.Bold))
        start_button.clicked.connect(self.start_action)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)

        # Stop button
        stop_button = QPushButton("Stop", self)
        stop_button.setFont(QFont("Arial", 14, QFont.Bold))
        stop_button.clicked.connect(self.stop_action)
        layout.addWidget(stop_button, alignment=Qt.AlignCenter)

        # Dropdown menu with options
        self.dropdown_menu = QComboBox(self)
        self.dropdown_menu.setFont(QFont("Arial", 12))
        self.dropdown_menu.addItems(["Option 1", "Option 2", "Option 3"])
        self.dropdown_menu.setMinimumSize(200, 10)
        self.dropdown_menu.currentIndexChanged.connect(self.option_selected)
        layout.addWidget(self.dropdown_menu, alignment=Qt.AlignCenter)

        # Apply layout to the main window
        self.setLayout(layout)

    def reload_state(self):
        pass

    def start_action(self):
        print("Start button clicked")

    def stop_action(self):
        print("Stop button clicked")

    def option_selected(self):
        selected_option = self.dropdown_menu.currentText()
        print(f"Selected option: {selected_option}")

def load_stylesheet(filename):
    with open(filename, "r") as file:
        return file.read()

# Run the application
app = QApplication(sys.argv)
control_panel = ControlPanel()

print(os.listdir())

stylesheet = load_stylesheet("src/client/styles.qss")
app.setStyleSheet(stylesheet)

control_panel.show()
sys.exit(app.exec_())
