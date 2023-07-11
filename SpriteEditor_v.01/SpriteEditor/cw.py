import tkinter as tk
from tkinter import colorchooser

def pick_color():
    color = colorchooser.askcolor(title="Pick a Color")
    if color[1]:
        print("Selected color:", color[1])

# Create the main window
window = tk.Tk()
window.title("Color Picker")

# Create a button to open the color picker dialog
button = tk.Button(window, text="Pick a Color", command=pick_color)
button.pack()

# Start the Tkinter event loop
window.mainloop()

