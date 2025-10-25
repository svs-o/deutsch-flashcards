# TXT parser (skeleton)
import csv
from .model import Card

def load_deck(path: str) -> list[Card]:
    cards: list[Card] = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';', quotechar='"')
        for idx, row in enumerate(reader, start=1):
            if not row or all(not c.strip() for c in row):
                continue
            if len(row) < 4:
                raise ValueError(f"Строка {idx}: ожидается 4 поля, получено {len(row)} -> {row}")
            term, forms, sentence, translation = row[:4]
            cards.append(Card(term.strip(), forms.strip(), sentence.strip(), translation.strip()))
    return cards
