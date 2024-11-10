import json
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QHBoxLayout, QDialog
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QTimer
import arduino

from color import ColorDialog
from moodapi import *
import cv2

def load_mappings_from_file(path: str):
    if os.path.exists(path):
        with open(path, "r") as file:
            return json.loads(file.read())
   

def load_stylesheet(filename):
    with open(filename, "r") as file:
        return file.read()


class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.count = 0
        self.timer.timeout.connect(self.play)
        self.timer.start()
        
        self.mappings = load_mappings_from_file("./client/src/mappings.json")

        self.setWindowTitle("moodlight")
        self.setGeometry(100, 100, 1000, 350)
        self.device = arduino.init_connection("/dev/ttyACM0")
        layout = QVBoxLayout()

        self.lightIsOn = False

        # Start button
        start_button = QPushButton("Lights on", self)
        start_button.setFont(QFont("Arial", 14, QFont.Bold))
        start_button.clicked.connect(self.light_on)

        # Stop button
        stop_button = QPushButton("Lights off", self)
        stop_button.setFont(QFont("Arial", 14, QFont.Bold))
        stop_button.clicked.connect(self.light_off)

        button_box = QHBoxLayout()
        button_box.addWidget(start_button, alignment=Qt.AlignLeft)
        button_box.addWidget(stop_button, alignment=Qt.AlignRight)

        # Dropdown menu with options
        self.dropdown_menu = QComboBox(self)
        self.dropdown_menu.setFont(QFont("Arial", 12))
        self.dropdown_menu.addItems(["No Music", "Music"])
        self.dropdown_menu.setMinimumSize(200, 10)

        # Text for mode
        self.selected_mode_text = QLabel(f"Mode: off")
        self.selected_mode_text.setFont(QFont("Arial", 14, QFont.Bold))
        self.selected_mode_text.setStyleSheet("padding: 0px;")

        self.dropdown_menu.currentIndexChanged.connect(self.option_selected)

        # Button to open the mapping editor
        edit_button = QPushButton("Edit color mappings")
        edit_button.clicked.connect(self.open_mapping_editor)

        layout.addLayout(button_box)
        layout.addWidget(self.selected_mode_text, alignment=Qt.AlignCenter)
        layout.addWidget(self.dropdown_menu, alignment=Qt.AlignLeft)
        layout.addWidget(edit_button, alignment=Qt.AlignLeft)

        # Apply layout to the main window
        self.setLayout(layout)

    def light_on(self):
        self.lightIsOn = True
        self.selected_mode_text.setText(f"Mode: {self.dropdown_menu.currentText()}")

    def light_off(self):
        self.lightIsOn = False
        self.selected_mode_text.setText(f"Mode: off")

    def option_selected(self):
        selected_option = self.dropdown_menu.currentText()
        self.selected_mode_text.setText(f"Mode: {selected_option}")

    def update_display(self):
        # Update the label with the selected color
        emotion = self.dropdown.currentText()
        color = self.mappings.get(emotion, "Unknown")
        self.color_label.setText(f"Color: {color}")

    def open_mapping_editor(self):
        # Open the mapping editor dialog
        dialog = ColorDialog(self.mappings)
        if dialog.exec_() == QDialog.Accepted:
            dialog.save_mappings()
            dialog.save_mappings_to_file()
    
    def play(self):
        print(self.lightIsOn)
        self.count += 1
        music = False
        if (self.dropdown_menu.currentText() == "Music" and self.count % 50 == 0):
            music = True
        if (self.count % 10 == 0):
            runmood(self.lightIsOn, music, 0, self.mappings, self.device)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    control_panel = ControlPanel()

    stylesheet = load_stylesheet("./client/styles.css")
    app.setStyleSheet(stylesheet)
    control_panel.show()
    
    
    
    
    
    sys.exit(app.exec_())

    while True:
        control_panel.play()
        time.sleep(2)
