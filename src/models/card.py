class Card:
    SUITS = ["Copas", "Ouros", "Paus", "Espadas"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Valete", "Dama", "Rei", "Ás"]
    VALUES = {rank: i for i, rank in enumerate(RANKS, 2)}

    def __init__(self, suit, rank):
        if suit not in self.SUITS:
            raise ValueError(f"Naipe inválido: {suit}")
        if rank not in self.RANKS:
            raise ValueError(f"Valor inválido: {rank}")
        self.suit = suit
        self.rank = rank
        self.value = self.VALUES[rank]

    def __str__(self):
        return f"{self.rank} de {self.suit}"

    def __repr__(self):
        return f"Card('{self.suit}', '{self.rank}')"

    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.value < other.value

    def __gt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.value > other.value