import time
import tkinter as tk
from tkinter import messagebox, filedialog
from .deck import load_deck
from .scheduler import choose_next
from .model import Card

ART_COLORS = {"die": "#7c0000", "der": "#0034a6", "das": "#00a43c"}

def split_article(line: str):
    s = line.strip()
    if s == None:
        return None, s
    parts = line.split(None, 1)
    if parts[0].lower in ART_COLORS and len(parts) > 1:
        return parts[0].lower, parts[1]
    else:
        return None, s 



class App(tk.Tk):
    def __init__(self, deck_path: str):
        super().__init__()
        self.title("Deutsch Flashcards")
        self.geometry("760x500"); self.configure(bg="#f7f7f9")
        self.deck_path = deck_path
        self.cards = load_deck(deck_path)
        self.current: Card | None = None
        self.show_translation = False

        self.card_frame = tk.Frame(self, bg="white", bd=0, highlightthickness=1, highlightbackground="#000000")
        self.card_frame.place(relx=0.5, rely=0.4, anchor="center", width=660, height=310)

        top = tk.Frame(self.card_frame, bg="white"); top.pack(pady=(70, 10))
        self.article_label = tk.Label(top, text="", bg="white", font=("Segoe UI", 26, "bold"))
        self.word_label = tk.Label(top, text="", bg="white", font=("Segoe UI", 26, "bold"), wraplength=600, justify="center")
        self.article_label.pack(side="left", padx=(0,8)); self.word_label.pack(side="left")

        self.forms_label = tk.Label(self.card_frame, text="", bg="white", fg="#6b7280", font=("Segoe UI", 15), wraplength=600, justify="center")
        self.forms_label.pack(pady=(0, 10))

        self.hint_label = tk.Label(self.card_frame, text="", bg="white", fg="#000000", font=("Segoe UI", 20), wraplength=600, justify="center")
        self.hint_label.pack(pady=(0, 8))

        translation_frame = tk.Frame(self.card_frame, bg="red"); top.pack(pady=(70, 10))
        self.translation_label = tk.Label(translation_frame, text="", bg="white", fg="#111827", font=("Segoe UI", 26, "bold"), wraplength=600, justify="center")
        self.translation_label.pack(side="left"); 

        btns = tk.Frame(self, bg="#f7f7f9"); btns.pack(side="bottom", pady=18)
        tk.Button(btns, text="Don't know (1)", width=16, command=self.on_dont_know).grid(row=0, column=0, padx=8)
        tk.Button(btns, text="Hint (2)", width=16, command=self.on_hint).grid(row=0, column=1, padx=8)
        tk.Button(btns, text="Know (3)", width=16, command=self.on_know).grid(row=0, column=2, padx=8)

        self.bind("<space>", lambda e: self.toggle_translation())
        self.bind("1", lambda e: self.on_dont_know())
        self.bind("2", lambda e: self.on_hint())
        self.bind("3", lambda e: self.on_know())

        self.next_card()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def render(self):
        if not self.current: return
        c = self.current
        article, core = split_article(c.term)
        if article:
            from .ui import ART_COLORS
            self.article_label.config(text=article, fg=ART_COLORS[article]); self.article_label.pack(side="left", padx=(0,8))
            self.word_label.config(text=core)
        else:
            self.article_label.config(text=""); self.article_label.pack_forget()
            self.word_label.config(text=c.term)
        self.forms_label.config(text=c.forms)
        self.translation_label.config(text=c.translation if self.show_translation else "")

    def toggle_translation(self):
        self.show_translation = not self.show_translation
        self.render()

    def reveal_and_schedule_next(self):
        self.show_translation = True; self.render()
        self.after(2000, self.next_card)

    def on_dont_know(self):
        c = self.current; 
        if not c: return
        c.box = 1; c.seen += 1; c.wrong += 1; c.last = time.time()
        self.hint_label.config(text=""); self.reveal_and_schedule_next()

    def on_hint(self):
        c = self.current; 
        if not c: return
        c.box = max(1, c.box - 1); c.seen += 1; c.last = time.time()
        self.hint_label.config(text=c.sentence); self.reveal_and_schedule_next()

    def on_know(self):
        c = self.current; 
        if not c: return
        c.box = min(5, c.box + 1); c.seen += 1; c.last = time.time()
        self.hint_label.config(text=""); self.reveal_and_schedule_next()

    def next_card(self):
        if not self.cards:
            messagebox.showinfo("Пусто", "В колоде нет карточек.")
            return
        from .scheduler import choose_next
        self.current = choose_next(self.cards)
        self.show_translation = False; self.hint_label.config(text=""); self.render()
