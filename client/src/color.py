import json

from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHBoxLayout, QPushButton, QTableWidget, QVBoxLayout

mapping_file = "./client/src/mappings.json"

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
        self.table.horizontalHeader().setStretchLastSection(True)

        # Populate the table with initial values
        for row, (emotion, color) in enumerate(self.mappings.items()):
            emotion_item = QTableWidgetItem(emotion)
            color_item = QTableWidgetItem(color)
            self.table.setItem(row, 0, emotion_item)
            self.table.setItem(row, 1, color_item)

        layout.addWidget(self.table)

        # Buttons to save or cancel changes
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        save_button.clicked.connect(self.save_mappings)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)


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