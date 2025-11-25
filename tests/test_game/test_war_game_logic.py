import unittest
from src.game.war_game_logic import WarGameLogic


class TestWarGameLogic(unittest.TestCase):
    def setUp(self):
        self.game = WarGameLogic()

    def test_initial_game_state(self):
        """Testa se o estado inicial do jogo está correto."""
        state = self.game.get_game_state_for_ui()
        self.assertEqual(state['player1_hand_size'], 26)
        self.assertEqual(state['player2_hand_size'], 26)
        self.assertFalse(state['is_game_over'])
        self.assertEqual(state['current_round'], 0)

    def test_play_single_round_updates_round_and_hand_size(self):
        """Testa se jogar uma rodada atualiza a rodada e muda o tamanhos das mãos."""
        self.game.play_round()
        state = self.game.get_game_state_for_ui()
        self.assertEqual(state['current_round'], 1)
        total_cards = state['player1_hand_size'] + state['player2_hand_size']
        self.assertEqual(total_cards, 52)  # Nenhuma carta desaparece

    def test_game_log_is_updated_after_round(self):
        """Testa se o log do jogo é atualizado após uma rodada."""
        self.game.play_round()
        log = self.game.get_game_log_entries()
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]['round'], 1)

    def test_game_can_reach_end(self):
        """Testa se o jogo chega até o fim sem erros."""
        while not self.game.get_game_state_for_ui()['is_game_over']:
            self.game.play_round()
        state = self.game.get_game_state_for_ui()
        self.assertTrue(state['is_game_over'])
        self.assertGreaterEqual(state['current_round'], 1)

    def test_max_round_limit_works(self):
        """Testa se o limite de rodadas funciona corretamente."""
        self.game.max_rounds = 5  # Força limite baixo para testar
        for _ in range(10):  # tenta mais que o limite
            self.game.play_round()
        self.assertLessEqual(self.game.get_game_state_for_ui()['current_round'], 5)
        log = self.game.get_game_log_entries()
        last_log = log[-1]
        self.assertEqual(last_log['type'], 'limit_reached')

    def test_check_game_winner_no_winner_initially(self):
        """Testa se no início não há vencedor."""
        winner = self.game.check_game_winner()
        self.assertIsNone(winner)


if __name__ == '__main__':
    unittest.main()
