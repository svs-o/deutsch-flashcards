import random
from app.model import Card
from app.scheduler import card_weight

def test_weights_order():
    a = Card("der Hund","die Hunde","","собака"); a.box = 1
    b = Card("der Tisch","die Tische","","стол"); b.box = 5
    wa = card_weight(a, 10_000); wb = card_weight(b, 10_000)
    assert wa > wb

def test_penalty_wrong():
    a = Card("der Hund","die Hunde","","собака"); a.box = 3; a.wrong = 3
    b = Card("der Hund","die Hunde","","собака"); b.box = 3; b.wrong = 0
    wa = card_weight(a, 10_000); wb = card_weight(b, 10_000)
    assert wa > wb

def test_cooldown():
    c = Card("der Hund","die Hunde","","собака"); c.box = 3; c.last = 9.5
    w_recent = card_weight(c, 10.0)
    c.last = 0.0
    w_stale = card_weight(c, 10.0)
    assert w_recent < w_stale
