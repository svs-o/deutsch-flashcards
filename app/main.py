# Entry point
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from .ui import App

def main():
    if len(sys.argv) < 2:  #no path to the file 
        root = tk.Tk(); root.withdraw() 
        messagebox.showinfo("Open a set", "Choose a txt file")
        path = filedialog.askopenfilename(filetypes=[("Text files","*.txt"),("All files","*.*")])
        if not path:
            return
        root.destroy()
        deck_path = path
    else:
        deck_path = sys.argv[1]
    App(deck_path).mainloop()

# Run the app only if this file is executed directly, not when imported as a modul
if __name__ == "__main__":
    main()
