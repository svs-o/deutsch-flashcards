# TXT parser 
import csv
from .model import Card
def load_deck(path:str):
    cards: list[Card] = []
    with open(path, 'r', encoding = 'utf-8') as f:
        reader = csv.reader(f, delimiter = ';', quotechar = '"')
        for idx, row in enumerate(reader, start = 1):
            if len(row)<4:
                raise ValueError(f"Row {idx}: is waiting for 4 fields, recieved {len(row)} -> {row}")
            term = row[0]
            forms = row[1]
            sentanse = row[2]
            translation = row[3]
            cards.append(Card(term, forms, sentanse, translation))
        return cards





