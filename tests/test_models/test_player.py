import pytest
from src.models.card import Card
from src.models.player import Player


def test_player_creation():
    player = Player("Jogador 1")
    assert player.name == "Jogador 1"
    assert player.hand_size() == 0
    assert not player.has_cards()
    assert str(player) == "Jogador Jogador 1 com 0 cartas."


def test_add_card_to_hand():
    player = Player("Jogador")
    card = Card("Copas", "Ás")

    player.add_card_to_hand(card)
    assert player.hand_size() == 1
    assert player.has_cards()


def test_add_multiple_cards_to_hand():
    player = Player("Jogador")
    cards = [Card("Copas", "Ás"), Card("Espadas", "Rei")]

    player.add_cards_to_hand(cards)
    assert player.hand_size() == 2
    assert player.has_cards()


def test_play_card():
    player = Player("Jogador")
    card1 = Card("Copas", "Ás")
    card2 = Card("Espadas", "Rei")

    player.add_cards_to_hand([card1, card2])

    played_card = player.play_card()
    assert played_card == card1
    assert player.hand_size() == 1

    played_card2 = player.play_card()
    assert played_card2 == card2
    assert player.hand_size() == 0
    assert not player.has_cards()

    # Tentar jogar sem carta retorna None
    assert player.play_card() is None
