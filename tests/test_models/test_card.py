import pytest
from src.models.card import Card


def test_card_creation():
    card = Card("Copas", "Ás")
    assert card.suit == "Copas"
    assert card.rank == "Ás"
    assert card.value == 14
    assert str(card) == "Ás de Copas"
    assert repr(card) == "Card('Copas', 'Ás')"


def test_invalid_suit():
    with pytest.raises(ValueError) as excinfo:
        Card("Flores", "Ás")
    assert "Naipe inválido" in str(excinfo.value)


def test_invalid_rank():
    with pytest.raises(ValueError) as excinfo:
        Card("Copas", "Coringa")
    assert "Valor inválido" in str(excinfo.value)


def test_comparison_operators():
    card1 = Card("Copas", "5")
    card2 = Card("Espadas", "8")
    card3 = Card("Ouros", "5")

    assert card1 < card2
    assert card2 > card1
    assert card1 == card3


def test_hash_and_equality():
    card1 = Card("Paus", "10")
    card2 = Card("Paus", "10")
    card_set = set()
    card_set.add(card1)

    assert card2 in card_set  # Testa se __hash__ e __eq__ funcionam corretamente
