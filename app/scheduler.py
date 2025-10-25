# Weighted scheduler with cooldown (skeleton)
import time, random
from .model import Card

def card_weight(card: Card, now: float) -> float:
    base = 6 - card.box
    penalty = 1 + min(card.wrong, 3) * 0.5
    cooldown = 0.3 if (now - card.last) < 10 else 1.0
    return max(0.1, base * penalty * cooldown)

def choose_next(cards: list[Card]) -> Card:
    now = time.time()
    weights = [card_weight(c, now) for c in cards]
    total = sum(weights)
    if total <= 0:
        return random.choice(cards)
    r = random.random() * total
    s = 0.0
    for c, w in zip(cards, weights):
        s += w
        if r <= s:
            return c
    return cards[-1]
