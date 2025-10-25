# Entry point
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from .ui import App

def main():
    if len(sys.argv) < 2:
        root = tk.Tk(); root.withdraw()
        messagebox.showinfo("Открыть колоду", "Выберите текстовый файл (UTF-8).")
        path = filedialog.askopenfilename(filetypes=[("Text files","*.txt"),("All files","*.*")])
        if not path:
            return
        root.destroy()
        deck_path = path
    else:
        deck_path = sys.argv[1]
    App(deck_path).mainloop()

if __name__ == "__main__":
    main()
