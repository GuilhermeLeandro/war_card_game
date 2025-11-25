import pytest
from src.models.deck import Deck
from src.models.card import Card


def test_deck_creation():
    deck = Deck()
    assert deck.size() == 52
    assert not deck.is_empty()
    assert str(deck) == "Baralho com 52 cartas."


def test_deal_card_reduces_deck_size():
    deck = Deck()
    initial_size = deck.size()
    card = deck.deal_card()

    assert isinstance(card, Card)
    assert deck.size() == initial_size - 1


def test_deal_all_cards_then_empty():
    deck = Deck()
    dealt_cards = []

    while not deck.is_empty():
        dealt_cards.append(deck.deal_card())

    assert len(dealt_cards) == 52
    assert deck.is_empty()

    # Tentativa de pegar mais uma carta deve retornar None
    assert deck.deal_card() is None


def test_shuffle_changes_order():
    deck1 = Deck()
    deck2 = Deck()

    # Força os dois decks a ficarem na mesma ordem
    deck2._pilha_cartas = deck1._pilha_cartas.copy()

    deck1.shuffle()

    # Existe a chance mínima de embaralhar e sair igual, então o ideal seria comparar conteúdo, não ordem
    assert deck1.size() == 52
    assert deck2.size() == 52

    # Checa se a ordem provavelmente mudou
    deck1_cards = [deck1.deal_card() for _ in range(deck1.size())]
    deck2_cards = [deck2.deal_card() for _ in range(deck2.size())]

    # Confirma que ambos têm as mesmas cartas, mas provavelmente em ordem diferente
    assert set(deck1_cards) == set(deck2_cards)
    assert deck1_cards != deck2_cards
