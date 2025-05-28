import random
from src.models.card import Card
from src.structures.stack import Stack # Usando sua Stack personalizada

class Deck:
    def __init__(self):
        self._pilha_cartas = Stack() # Instancia sua Stack
        card_list = [Card(s, r) for s in Card.SUITS for r in Card.RANKS]
        random.shuffle(card_list) # Embaralha a lista primeiro
        for card in card_list: # Adiciona à sua pilha
            self._pilha_cartas.push(card)

    def shuffle(self):
        """Reembaralha as cartas no baralho, usando a interface da sua Stack."""
        temp_list = []
        while not self._pilha_cartas.is_empty():
            temp_list.append(self._pilha_cartas.pop())
        random.shuffle(temp_list)
        for card in temp_list:
            self._pilha_cartas.push(card)

    def deal_card(self):
        """Remove e retorna uma carta do topo do baralho (usando sua Stack)."""
        if not self.is_empty():
            return self._pilha_cartas.pop()
        return None

    def is_empty(self):
        return self._pilha_cartas.is_empty()

    def size(self):
        return self._pilha_cartas.size()

    def __str__(self):
        return f"Baralho com {self.size()} cartas."