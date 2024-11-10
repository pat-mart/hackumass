import json
import re

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHBoxLayout, QPushButton, QTableWidget, QVBoxLayout

mapping_file = "./client/src/mappings.json"

emotions = ["CALM", "CONFUSED", "HAPPY", "ANGRY", "SURPRISED", "DISGUSTED", "SAD", "FEAR"]


def cubic_interpolate(y0, y1, y2, y3, t):
    a = (-y0 + 3 * y1 - 3 * y2 + y3) / 2
    b = (y0 - 5 * y1 + 4 * y2 - y3) / 2
    c = (-y0 + y2) / 2
    d = y1

    return a * t ** 3 + b * t ** 2 + c * t + d

def transition_colors_cubic(color_start, color_end, duration=1.0, fps=60):
    frames = int(duration * fps)
    r1, g1, b1 = color_start
    r2, g2, b2 = color_end

    interpolated_colors = []
    for i in range(frames):
        t = i / (frames - 1)
        r = round(cubic_interpolate(r1, r1, r2, r2, t))
        g = round(cubic_interpolate(g1, g1, g2, g2, t))
        b = round(cubic_interpolate(b1, b1, b2, b2, t))
        interpolated_colors.append((r, g, b))

    return interpolated_colors


class ColorDialog(QDialog):
    def __init__(self, mappings):
        super().__init__()
        self.setWindowTitle("Edit Emotion-Color Mappings")
        self.resize(400, 300)
        self.mappings = mappings
        self.setStyleSheet("./client/styles.css")

        # Layout for dialog
        layout = QVBoxLayout()

        # Create a table for emotion-color mappings
        self.table = QTableWidget(len(self.mappings), 2)
        self.table.setHorizontalHeaderLabels(["Emotion", "Color"])
        self.table.setStyleSheet("color: black;")
        self.table.horizontalHeader().setStretchLastSection(True)

        self.valid_hex_regex = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")

        # Populate the table with initial values
        for row, (emotion, color) in enumerate(self.mappings.items()):
            emotion_item = QTableWidgetItem(emotion)
            color_item = QTableWidgetItem(color)

            self.table.setItem(row, 0, emotion_item)
            self.table.setItem(row, 1, color_item)

        self.table.itemClicked.connect(self.set_background_colors)
        layout.addWidget(self.table)

        # Buttons to save or cancel changes
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        save_button.clicked.connect(self.save_mappings)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        self.set_background_colors()

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def set_background_colors(self):
        for row, (emotion, color) in enumerate(self.mappings.items()):
            if self.valid_hex_regex.search(color):
                self.table.item(row, 1).setBackground(QColor(color))

    def save_mappings(self):
        # Update mappings based on table content
        updated_mappings = {}
        for row in range(self.table.rowCount()):
            emotion = self.table.item(row, 0).text()
            color = self.table.item(row, 1).text()
            updated_mappings[emotion] = color
        self.mappings.clear()
        self.mappings.update(updated_mappings)
        self.accept()  # Close the dialog and return to main window

    def save_mappings_to_file(self):

        # Write mappings to a JSON file
        with open(mapping_file, "w") as file:
            json.dump(self.mappings, file, indent=4)