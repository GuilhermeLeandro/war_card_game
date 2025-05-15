from ..models.deck import Deck
from ..models.player import Player


class WarGame:
    def __init__(self, player1_name="Jogador 1", player2_name="Jogador 2"):
        self.deck = Deck()
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
        self._deal_cards()

    def _deal_cards(self):
        """Distribui as cartas do baralho para os jogadores."""
        half_deck = self.deck.size() // 2
        for _ in range(half_deck):
            card1 = self.deck.deal_card()
            if card1: self.player1.add_card_to_hand(card1)
            card2 = self.deck.deal_card()
            if card2: self.player2.add_card_to_hand(card2)


    def play_round(self):
        """Lógica para uma rodada do jogo."""
        if not self.player1.has_cards() or not self.player2.has_cards():
            return False  # Jogo acabou

        print(f"\n--- Nova Rodada ---")
        print(f"{self.player1.name} tem {self.player1.hand_size()} cartas.")
        print(f"{self.player2.name} tem {self.player2.hand_size()} cartas.")

        card1 = self.player1.play_card()
        card2 = self.player2.play_card()

        if not card1 or not card2:
            return False

        print(f"{self.player1.name} joga: {card1}")
        print(f"{self.player2.name} joga: {card2}")

        table_cards = [card1, card2]

        if card1.value > card2.value:
            print(f"{self.player1.name} vence a rodada!")
            self.player1.add_cards_to_hand(table_cards)
        elif card2.value > card1.value:
            print(f"{self.player2.name} vence a rodada!")
            self.player2.add_cards_to_hand(table_cards)
        else:
            print("GUERRA!")
            self._handle_war(table_cards)

        return True

    def _handle_war(self, table_cards):
        """Lida com a situação de 'Guerra'."""
        war_cards_p1 = []
        war_cards_p2 = []

        for _ in range(3):
            if self.player1.has_cards():
                c = self.player1.play_card()
                if c: war_cards_p1.append(c)
            if self.player2.has_cards():
                c = self.player2.play_card()
                if c: war_cards_p2.append(c)

        face_up_card1 = self.player1.play_card() if self.player1.has_cards() else None
        face_up_card2 = self.player2.play_card() if self.player2.has_cards() else None

        table_cards.extend(war_cards_p1)
        table_cards.extend(war_cards_p2)
        if face_up_card1: table_cards.append(face_up_card1)
        if face_up_card2: table_cards.append(face_up_card2)

        if face_up_card1 and face_up_card2:
            print(f"{self.player1.name} na guerra: {face_up_card1}")
            print(f"{self.player2.name} na guerra: {face_up_card2}")
            if face_up_card1.value > face_up_card2.value:
                print(f"{self.player1.name} vence a guerra!")
                self.player1.add_cards_to_hand(table_cards)
            elif face_up_card2.value > face_up_card1.value:
                print(f"{self.player2.name} vence a guerra!")
                self.player2.add_cards_to_hand(table_cards)
            else:
                print("GUERRA NOVAMENTE!")
                self._handle_war(table_cards)  # Guerra recursiva
        elif face_up_card1:
            print(f"{self.player1.name} vence a guerra por WO (Jogador 2 sem cartas suficientes)!")
            self.player1.add_cards_to_hand(table_cards)
        elif face_up_card2:
            print(f"{self.player2.name} vence a guerra por WO (Jogador 1 sem cartas suficientes)!")
            self.player2.add_cards_to_hand(table_cards)
        else:
            print(
                "Ambos jogadores sem cartas suficientes para a guerra. As cartas da mesa são... perdidas? (Defina regra)")

    def check_winner(self):
        if not self.player2.has_cards() and self.player1.has_cards():
            return self.player1
        if not self.player1.has_cards() and self.player2.has_cards():
            return self.player2
        if not self.player1.has_cards() and not self.player2.has_cards():
            return "Empate técnico"
        return None

    def start_game(self):
        print("Bem-vindo ao Jogo de Guerra (Batalha)!")
        round_count = 0
        max_rounds = 500  # Para evitar loops infinitos em alguns cenários de War
        while True:
            round_count += 1
            print(f"\n=== RODADA {round_count} ===")

            if not self.play_round():
                print("Não foi possível jogar a rodada, verificando vencedor...")
                break

            winner = self.check_winner()
            if winner:
                if isinstance(winner, Player):
                    print(f"\n🎉🎉🎉 {winner.name} venceu o jogo após {round_count} rodadas! 🎉🎉🎉")
                else:
                    print(f"\n🏁 O jogo terminou em {winner} após {round_count} rodadas. 🏁")
                break

            if round_count >= max_rounds:
                print(f"\n🏁 Limite de {max_rounds} rodadas atingido! Jogo empatado ou interrompido. 🏁")
                # Pode-se declarar vencedor quem tem mais cartas
                if self.player1.hand_size() > self.player2.hand_size():
                    print(f"{self.player1.name} tem mais cartas e é declarado vencedor!")
                elif self.player2.hand_size() > self.player1.hand_size():
                    print(f"{self.player2.name} tem mais cartas e é declarado vencedor!")
                else:
                    print("Empate no número de cartas!")
                break

            input_player = input("Precione \"ENTER\" para continuar ou digite \"sair\" para encerrar o jogo: ").upper()
            if input_player.lower() == "SAIR":
                print("Saindo do jogo...")
                break


