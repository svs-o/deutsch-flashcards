# Card model and spaced repetition state (skeleton)
from dataclasses import dataclass, asdict

@dataclass
class Card:
    term: str
    forms: str
    sentence: str
    translation: str
    # spaced repetition state
    box: int = 1
    seen: int = 0
    wrong: int = 0
    last: float = 0.0

    def key(self) -> str:
        return f"{self.term}|{self.translation}"

    def to_state(self) -> dict:
        return {"box": self.box, "seen": self.seen, "wrong": self.wrong, "last": self.last}

    def load_state(self, d: dict) -> None:
        for k in ("box","seen","wrong","last"):
            if k in d:
                setattr(self, k, d[k])
