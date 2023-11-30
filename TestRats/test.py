import tkinter as tk
from tkinter import colorchooser

def pick_color():
    color = colorchooser.askcolor(title="Choose a color")
    if color[1]:  # Check if a color was chosen (not canceled)
        color_label.config(text=f"Selected Color: {color[1]}", bg=color[1])

# Create the main window
root = tk.Tk()
root.title("Color Picker")

# Create a button to launch the color picker dialog
color_button = tk.Button(root, text="Pick a Color", command=pick_color)
color_button.pack(pady=10)

# Create a label to display the selected color
color_label = tk.Label(root, text="Selected Color: None", padx=10, pady=5)
color_label.pack()

# Start the Tkinter event loop
root.mainloop()
