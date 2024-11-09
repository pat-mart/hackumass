import tkinter as tk
from tkinter import ttk

# Initialize the main window
root = tk.Tk()
root.title("m")
root.geometry("400x200")  # Set window size

# Functionality for Start and Stop buttons
def start_action():
    print("Start button clicked")

def stop_action():
    print("Stop button clicked")

# Functionality for dropdown menu
def option_selected(event):
    selected_option = dropdown_var.get()
    print(f"Selected option: {selected_option}")

# Start button
start_button = tk.Button(root, text="Start", command=start_action, font=("Arial", 14), width=10)
start_button.pack(pady=10)

# Stop button
stop_button = tk.Button(root, text="Stop", command=stop_action, font=("Arial", 14), width=10)
stop_button.pack(pady=10)

# Dropdown menu with options
dropdown_var = tk.StringVar()
dropdown_var.set("Select a Mode")  # Default value

# Define dropdown options
options = ["mood light", "music light"]
dropdown_menu = ttk.Combobox(root, textvariable=dropdown_var, values=options, state="readonly", font=("Arial", 12))
dropdown_menu.pack(pady=10)
dropdown_menu.bind("<<ComboboxSelected>>", option_selected)

# Run the GUI loop
root.mainloop()
