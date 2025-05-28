from src.models.deck import Deck
from src.models.player import Player
from src.structures.doubly_linked_list import DoublyLinkedList

class WarGameLogic:
    def __init__(self, player1_name="Você", player2_name="Máquina"):
        self.deck = Deck(); self.player1 = Player(player1_name); self.player2 = Player(player2_name)
        self.max_rounds = 1000; self.current_round = 0
        self.game_log = DoublyLinkedList() # Log para o histórico
        self._deal_initial_cards_to_players()

    def _add_log_entry(self, entry_data):
        # Adiciona ao final da lista duplamente encadeada (cronológico)
        self.game_log.append(entry_data) 
        print(f"[LOGIC_LOG_ADD] Rodada {entry_data.get('round')}, Tipo: {entry_data.get('type')}, Vencedor: {entry_data.get('winner')}")

    def get_game_log_entries(self): 
        # O LogDisplay vai inverter para mostrar o mais recente primeiro
        return self.game_log.get_all_entries() 
    
    def _deal_initial_cards_to_players(self):
        num_cards_total = self.deck.size()
        for i in range(num_cards_total):
            card = self.deck.deal_card()
            if card:
                if i % 2 == 0: self.player1.add_card_to_hand(card)
                else: self.player2.add_card_to_hand(card)
            else: break 
    
    def get_game_state_for_ui(self): # Usado pela GameScreen para infos gerais
        return {"player1_name": self.player1.name, "player1_hand_size": self.player1.hand_size(),
                "player2_name": self.player2.name, "player2_hand_size": self.player2.hand_size(),
                "is_game_over": self.check_game_winner() is not None, 
                "current_round": self.current_round}

    def play_round(self):
        self.current_round += 1
        round_events_for_ui = [] 
        log_entry_for_history = {
            "round": self.current_round, "type": "normal_round",
            "p1_played_str": "N/A", "p2_played_str": "N/A",
            "winner_name": "N/A", "war_events_log": [] 
        }

        if self.current_round > self.max_rounds:
            end_event = self._check_max_rounds_winner_event()
            round_events_for_ui.append(end_event)
            log_entry_for_history["type"] = "limit_reached"; log_entry_for_history["winner_name"] = end_event.get("winner")
            self._add_log_entry(log_entry_for_history); return round_events_for_ui
        
        winner_check = self.check_game_winner()
        if winner_check:
            round_events_for_ui.append({"type": "GAME_OVER", **winner_check})
            log_entry_for_history["type"] = "game_over"; log_entry_for_history["winner_name"] = winner_check.get("winner")
            self._add_log_entry(log_entry_for_history); return round_events_for_ui

        card_p1 = self.player1.play_card(); card_p2 = self.player2.play_card()

        if not card_p1 or not card_p2:
            winner_check = self.check_game_winner()
            evt = {"type": "GAME_OVER", **(winner_check if winner_check else {"winner":"Erro", "reason":"Carta nula"})}
            round_events_for_ui.append(evt)
            log_entry_for_history["type"] = "game_over_on_play"; log_entry_for_history["winner_name"] = evt.get("winner")
            log_entry_for_history["p1_played_str"] = str(card_p1) if card_p1 else "SEM CARTA"
            log_entry_for_history["p2_played_str"] = str(card_p2) if card_p2 else "SEM CARTA"
            self._add_log_entry(log_entry_for_history); return round_events_for_ui

        log_entry_for_history["p1_played_str"] = str(card_p1)
        log_entry_for_history["p2_played_str"] = str(card_p2)
        round_events_for_ui.append({"type": "CARDS_PLAYED", "player1_card": str(card_p1), "player2_card": str(card_p2)})
        
        table_cards_pot = [card_p1, card_p2] 

        if card_p1.value > card_p2.value:
            self.player1.add_cards_to_hand(table_cards_pot)
            round_events_for_ui.append({"type": "ROUND_WINNER", "winner_name": self.player1.name})
            log_entry_for_history["winner_name"] = self.player1.name
        elif card_p2.value > card_p1.value:
            self.player2.add_cards_to_hand(table_cards_pot)
            round_events_for_ui.append({"type": "ROUND_WINNER", "winner_name": self.player2.name})
            log_entry_for_history["winner_name"] = self.player2.name
        else: # Guerra
            log_entry_for_history["type"] = "war_round" # Marca a rodada como uma que teve guerra
            round_events_for_ui.append({"type": "WAR_DECLARED", "card1": str(card_p1), "card2": str(card_p2)})
            
            war_winner_obj = self._handle_war_recursive(table_cards_pot, round_events_for_ui, log_entry_for_history["war_events_log"])
            
            if war_winner_obj:
                log_entry_for_history["winner_name"] = war_winner_obj.name # Vencedor final da guerra
            else:
                log_entry_for_history["winner_name"] = "Ninguém (Empate na Guerra)"
        
        self._add_log_entry(log_entry_for_history)
        
        round_events_for_ui.append({"type": "HAND_SIZES_UPDATE", 
                             "player1_hand_size": self.player1.hand_size(), 
                             "player2_hand_size": self.player2.hand_size()})
        
        winner_check_final = self.check_game_winner()
        if winner_check_final and not any(e.get("type") == "GAME_OVER" for e in round_events_for_ui):
             round_events_for_ui.append({"type": "GAME_OVER", **winner_check_final})
        return round_events_for_ui

    def _handle_war_recursive(self, current_pot, ui_events_list, war_log_list):
        """
        Processa uma fase da guerra, adiciona cartas ao pote, e decide o vencedor da fase ou recorre.
        Adiciona eventos à ui_events_list e war_log_list.
        Retorna o objeto Player vencedor da guerra inteira, ou None se for um impasse final.
        """
        war_log_list.append({"step": "Fase de Guerra", "pot_inicial_fase_str": [str(c) for c in current_pot]})

        p1_bet_cards, p2_bet_cards = [], []
        for _ in range(3): 
            if self.player1.has_cards(): p1_bet_cards.append(self.player1.play_card())
        for _ in range(3):
            if self.player2.has_cards(): p2_bet_cards.append(self.player2.play_card())
        
        p1_bet_actual = [c for c in p1_bet_cards if c]; current_pot.extend(p1_bet_actual)
        p2_bet_actual = [c for c in p2_bet_cards if c]; current_pot.extend(p2_bet_actual)
        
        ui_events_list.append({"type": "WAR_BET_CARDS", 
                               "player1_bet_count": len(p1_bet_actual), 
                               "player2_bet_count": len(p2_bet_actual)})
        war_log_list.append({"step": "Apostas da Guerra", 
                             "p1_bet_str": [str(c) for c in p1_bet_actual], 
                             "p2_bet_str": [str(c) for c in p2_bet_actual]})

        p1_reveal = self.player1.play_card() if self.player1.has_cards() else None
        p2_reveal = self.player2.play_card() if self.player2.has_cards() else None
        
        if p1_reveal: current_pot.append(p1_reveal)
        if p2_reveal: current_pot.append(p2_reveal)

        ui_events_list.append({"type": "WAR_REVEAL_CARDS", 
                               "player1_reveal_card": str(p1_reveal) if p1_reveal else "N/A",
                               "player2_reveal_card": str(p2_reveal) if p2_reveal else "N/A"})
        war_log_list.append({"step": "Revelação da Guerra", 
                             "p1_reveal_str": str(p1_reveal) if p1_reveal else "N/A", 
                             "p2_reveal_str": str(p2_reveal) if p2_reveal else "N/A"})

        if p1_reveal and p2_reveal:
            if p1_reveal.value > p2_reveal.value:
                self.player1.add_cards_to_hand(current_pot)
                ui_events_list.append({"type": "WAR_WINNER", "winner_name": self.player1.name, "cards_in_pot": len(current_pot)})
                war_log_list.append({"step": "Vencedor da Guerra (rodada)", "winner": self.player1.name, "collected_pot_size": len(current_pot)})
                return self.player1
            elif p2_reveal.value > p1_reveal.value:
                self.player2.add_cards_to_hand(current_pot)
                ui_events_list.append({"type": "WAR_WINNER", "winner_name": self.player2.name, "cards_in_pot": len(current_pot)})
                war_log_list.append({"step": "Vencedor da Guerra (rodada)", "winner": self.player2.name, "collected_pot_size": len(current_pot)})
                return self.player2
            else:
                ui_events_list.append({"type": "WAR_DECLARED_AGAIN", "card1": str(p1_reveal), "card2": str(p2_reveal)})
                war_log_list.append({"step": "Nova Guerra (Empate na Revelação)"})
                return self._handle_war_recursive(current_pot, ui_events_list, war_log_list)
        elif p1_reveal: 
            self.player1.add_cards_to_hand(current_pot)
            ui_events_list.append({"type": "WAR_WINNER_BY_WO", "winner_name": self.player1.name, "reason": f"{self.player2.name} s/ cartas.", "cards_in_pot": len(current_pot)})
            war_log_list.append({"step": "Vencedor da Guerra por WO", "winner": self.player1.name, "collected_pot_size": len(current_pot)})
            return self.player1
        elif p2_reveal: 
            self.player2.add_cards_to_hand(current_pot)
            ui_events_list.append({"type": "WAR_WINNER_BY_WO", "winner_name": self.player2.name, "reason": f"{self.player1.name} s/ cartas.", "cards_in_pot": len(current_pot)})
            war_log_list.append({"step": "Vencedor da Guerra por WO", "winner": self.player2.name, "collected_pot_size": len(current_pot)})
            return self.player2
        else: 
            ui_events_list.append({"type": "WAR_DRAW_NO_CARDS", "reason": "Ambos s/ cartas para guerra."})
            war_log_list.append({"step": "Empate na Guerra (sem cartas de revelação)", "pot_size_lost": len(current_pot)})
            return None
        
    def _check_max_rounds_winner_event(self):
        reason = f"Limite de {self.max_rounds} rodadas atingido."
        p1_size = self.player1.hand_size(); p2_size = self.player2.hand_size()
        winner_name = "Empate"
        if p1_size > p2_size: winner_name = self.player1.name
        elif p2_size > p1_size: winner_name = self.player2.name
        return {"type": "GAME_OVER", "winner": winner_name, "reason": reason}

    def check_game_winner(self):
        p1_has = self.player1.has_cards(); p2_has = self.player2.has_cards()
        if not p2_has and p1_has: return {"winner": self.player1.name, "reason": f"{self.player2.name} sem cartas."}
        if not p1_has and p2_has: return {"winner": self.player2.name, "reason": f"{self.player1.name} sem cartas."}
        if not p1_has and not p2_has: return {"winner": "Empate", "reason": "Ambos sem cartas."}
        return None