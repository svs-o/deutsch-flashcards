import io, csv, os, tempfile
from app.deck import load_deck

def test_load_deck_ok():
    content = '"der Hund";"die Hunde";"Satz";"собака"\n'
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8", suffix=".txt") as f:
        f.write(content); name = f.name
    cards = load_deck(name)
    os.remove(name)
    assert len(cards) == 1
    assert cards[0].term == "der Hund"

def test_load_deck_ignores_empty():
    content = '\n\n"der Hund";"die Hunde";"Satz";"собака"\n'
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8", suffix=".txt") as f:
        f.write(content); name = f.name
    cards = load_deck(name)
    os.remove(name)
    assert len(cards) == 1

def test_load_deck_bad_line():
    content = '"nur zwei";"плохо"\n'
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8", suffix=".txt") as f:
        f.write(content); name = f.name
    try:
        load_deck(name)
        raised = False
    except ValueError:
        raised = True
    finally:
        os.remove(name)
    assert raised
