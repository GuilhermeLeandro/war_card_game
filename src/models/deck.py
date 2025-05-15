import random
from .card import Card
# from ..structures.stack import Stack

class Deck:
    def __init__(self):
        self._cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
        self.shuffle()

    def shuffle(self):
        """Embaralha as cartas no baralho."""
        random.shuffle(self._cards)

    def deal_card(self):
        """Remove e retorna uma carta do topo do baralho (comportamento de pilha)."""
        if not self.is_empty():
            return self._cards.pop()
        return None

    def is_empty(self):
        return len(self._cards) == 0

    def size(self):
        return len(self._cards)

    def __str__(self):
        return f"Deck com {self.size()} cartas."