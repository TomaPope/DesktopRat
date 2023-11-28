import tkinter as tk
from tkinter import ttk

class StyledNotebookApp:
    def __init__(self):
        master = tk.Tk()
        
        self.master = master
        self.master.title("Styled Notebook App")

        # Create a styled notebook
        self.notebook_style = ttk.Style()
        self.notebook_style.configure("TNotebook", background="#638")
        self.notebook_style.configure("TNotebook.Tab", background="#263", padding=[10, 5], font=('Helvetica', 10))

        self.notebook = ttk.Notebook(self.master, style="TNotebook")

        # Create tabs for the notebook
        tab1 = tk.Frame(self.notebook, background="#ececec")
        tab2 = tk.Frame(self.notebook, background="#ececec")

        self.notebook.add(tab1, text="Tab 1")
        self.notebook.add(tab2, text="Tab 2")

        # Pack the notebook
        self.notebook.pack(expand=1, fill="both")
        master.geometry("600x400")
        master.mainloop()

StyledNotebookApp()
