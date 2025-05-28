from src.structures.queue import Queue

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Queue() # Usando sua Queue personalizada
    def add_card_to_hand(self, card): self.hand.enqueue(card)
    def add_cards_to_hand(self, cards: list):
        for card in cards: self.hand.enqueue(card)
    def play_card(self):
        if not self.hand.is_empty(): return self.hand.dequeue()
        return None
    def has_cards(self): return not self.hand.is_empty()
    def hand_size(self): return self.hand.size()
    def __str__(self): return f"Jogador {self.name} com {self.hand_size()} cartas."