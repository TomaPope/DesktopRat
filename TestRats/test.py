import tkinter as tk
import tkinter.ttk as ttk

root = tk.Tk()
root.geometry('%dx%d+0+0' %(200,200))
# Style  # 68485915
style = ttk.Style()
 
COLOR_GREEN = "#26d663"
COLOR_RED = "#dd0202"

style.theme_create("yummy", parent="alt", settings={
    "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
    "TNotebook.Tab": {
    "configure": {"padding": [5, 1], "background": COLOR_GREEN},
    "map":       {"background": [("selected", COLOR_RED)],
    "expand": [("selected", [1, 1, 1, 0])] } } } )

style.theme_use("yummy")

 
# Create Notebook and Frames
Book = ttk.Notebook(root)

aFrame = ttk.Frame(Book)
Book.add(aFrame, text = 'A')
bFrame = ttk.Frame(Book) #/18855943/
Book.add(bFrame, text = 'B')
Book.pack(fill = tk.BOTH, expand = True)
  

root.mainloop()