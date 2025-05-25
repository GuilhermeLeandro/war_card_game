# src/ui/game_screen.py
import pygame
import time
import os
from structures.queue import Queue
from .base_screen import BaseScreen
from .elements import VisualCard, Button
from . import card_graphics
from . import constants as C
from game.war_game_logic import WarGameLogic
from .log_display import LogDisplay
from .ui_utils import draw_linear_gradient_rect

class GameScreen(BaseScreen):
    def __init__(self, screen, manager, game_logic_instance: WarGameLogic):
        super().__init__(screen, manager, manager.fonte_nome_jogador)
        self.status_font = manager.fonte_status_jogo
        self.hand_count_font = manager.fonte_contagem_cartas
        self.game_button_font = manager.fonte_botao_jogo
        self.screen_header_font = manager.fonte_cabecalho_tela

        self.game_logic = game_logic_instance
        
        self.status_message = ""; self.message_display_time_total = 0; self.message_start_timer = 0
        self.all_visual_cards = pygame.sprite.Group()
        self.player_played_card_sprite = pygame.sprite.GroupSingle()
        self.opponent_played_card_sprite = pygame.sprite.GroupSingle()
        self.war_bet_cards_p1_sprites = pygame.sprite.Group(); self.war_bet_cards_p2_sprites = pygame.sprite.Group()
        self.my_player_obj_name = ""; self.opponent_player_obj_name = ""
        self.player_hand_size = 0; self.opponent_hand_size = 0
        self.is_game_over = False; self.action_button = None; self.is_war_active_visual = False
        self.background_image = None
        try:
            bg_path = os.path.join(C.BACKGROUND_ASSETS_PATH, 'game_table.jpg')
            if os.path.exists(bg_path):
                 self.background_image = pygame.image.load(bg_path).convert()
                 self.background_image = pygame.transform.scale(self.background_image, (C.SCREEN_WIDTH,C.SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Erro ao carregar imagem de fundo do jogo: {e}")
            self.background_image = None

        self.event_animation_queue = Queue()
        self.is_processing_visual_event = False
        
        self.current_round_data_for_winner_animation = None
        self.flip_callback_count = 0; self.expected_flips = 0
        self.pending_card_arrivals_for_reveal = 0
        self.log_button = None
        self.log_display_panel = LogDisplay(screen, self, self.game_logic.get_game_log_entries)
        
        self._initialize_ui_for_game()

    def _initialize_ui_for_game(self):
        self.all_visual_cards.empty(); self.player_played_card_sprite.empty(); self.opponent_played_card_sprite.empty()
        self.war_bet_cards_p1_sprites.empty(); self.war_bet_cards_p2_sprites.empty()
        self.event_animation_queue.clear()
        self.is_game_over = False; self.status_message = ""
        self.action_button = None; self.current_round_data_for_winner_animation = None
        self.is_processing_visual_event = False;  self.is_war_active_visual = False
        pygame.time.set_timer(C.UI_EVENT_REVEAL_CARDS_ON_TABLE, 0)
        pygame.time.set_timer(C.UI_EVENT_ANIMATE_WINNER_COLLECTION, 0)
        pygame.time.set_timer(C.UI_EVENT_CONTINUE_GAME_SEQUENCE, 0)
        self.log_display_panel.log_entries_func = self.game_logic.get_game_log_entries
        current_game_state = self.game_logic.get_game_state_for_ui()
        self.player_hand_size = current_game_state["player1_hand_size"]; self.opponent_hand_size = current_game_state["player2_hand_size"]
        self.my_player_obj_name = current_game_state["player1_name"]; self.opponent_player_obj_name = current_game_state["player2_name"]
        self.set_status_message("Jogo Iniciado! Clique para jogar.", 2)
        self._create_action_button("Jogar Rodada", self._trigger_play_local_round, enabled=True)
        self._create_log_button()

    def _create_log_button(self):
        self.log_button = Button(
            C.LOG_BUTTON_X, C.LOG_BUTTON_Y, C.LOG_BUTTON_WIDTH, C.LOG_BUTTON_HEIGHT,
            "Histórico", self.game_button_font,
            action=self._toggle_log_display,
            color=C.GAME_BUTTON_BG_NORMAL_COLOR,
            hover_color=C.GAME_BUTTON_BG_HOVER_COLOR,
            text_color=C.GAME_BUTTON_TEXT_COLOR
        )

    def _toggle_log_display(self):
        """ Alterna a visibilidade do painel de histórico e ajusta o estado do botão de ação. """
        if self.log_display_panel.is_visible:
            self.log_display_panel.hide()

            if self.action_button and \
               not self.is_game_over and \
               not self.is_processing_visual_event and \
               self.event_animation_queue.is_empty(): 
                
                if self.action_button.text == "Jogar Rodada" and not self.action_button.is_enabled:
                    self.action_button.set_enabled(True)

        else:
            self.log_display_panel.show()
            if self.action_button:
                self.action_button.set_enabled(False)

    def _create_menu_button(self, text="Voltar ao Menu"):
        self._create_action_button(text, self.manager.mostrar_menu, enabled=True, use_font=self.game_button_font)

    def _create_action_button(self, text, action_callback, enabled=True, use_font=None):
        if self.action_button: self.action_button = None
        font_for_button = use_font if use_font else self.game_button_font
        self.action_button = Button(
            C.GAME_ACTION_BUTTON_X, C.GAME_ACTION_BUTTON_Y,
            C.GAME_ACTION_BUTTON_WIDTH, C.GAME_ACTION_BUTTON_HEIGHT,
            text, font_for_button,
            action=action_callback,
            color=C.GAME_BUTTON_BG_NORMAL_COLOR,
            hover_color=C.GAME_BUTTON_BG_HOVER_COLOR,
            text_color=C.GAME_BUTTON_TEXT_COLOR
        )
        self.action_button.set_enabled(enabled)
        
    def _trigger_play_local_round(self):
        if self.game_logic and not self.is_game_over and self.action_button and self.action_button.is_enabled:
            self.action_button.set_enabled(False)
            round_events = self.game_logic.play_round()
            self.event_animation_queue.clear()
            self.is_processing_visual_event = False
            for event_data in round_events:
                self.event_animation_queue.append(event_data)
            self._process_next_visual_event_from_queue()

    def _clear_table_cards_visuals(self):
        for card in list(self.all_visual_cards):
            if not card.is_collecting_to_winner: card.kill()
        self.player_played_card_sprite.empty(); self.opponent_played_card_sprite.empty()
        self.war_bet_cards_p1_sprites.empty(); self.war_bet_cards_p2_sprites.empty()

    def _process_next_visual_event_from_queue(self):
        if self.event_animation_queue.is_empty():
            self.is_processing_visual_event = False

            if not self.is_game_over and self.action_button and not self.log_display_panel.is_visible:
                if not self.action_button.is_enabled and self.action_button.text == "Jogar Rodada":
                    self.action_button.set_enabled(True)
            return
        if self.is_processing_visual_event: return
        
        self.is_processing_visual_event = True
        event_data = self.event_animation_queue.popleft()
        event_type = event_data.get("type")
        
        next_timer_id = C.UI_EVENT_CONTINUE_GAME_SEQUENCE
        delay = 600
        self.is_war_active_visual = False

        if event_type == "CARDS_PLAYED":
            self._clear_table_cards_visuals(); self.current_round_data_for_winner_animation=None
            my_s = event_data.get('player1_card'); opp_s = event_data.get('player2_card')
            anim_cards=[];
            if my_s: cv=VisualCard(my_s,C.PLAYER_DECK_POS.x,C.PLAYER_DECK_POS.y,is_face_up=False); cv.set_target_pos(C.PLAYER_CARD_PLAY_POS.x,C.PLAYER_CARD_PLAY_POS.y); self.player_played_card_sprite.add(cv);self.all_visual_cards.add(cv);anim_cards.append(cv)
            if opp_s: 
                cv_opp = VisualCard(opp_s,C.OPPONENT_DECK_POS.x,C.OPPONENT_DECK_POS.y,is_face_up=False)
                cv_opp.set_target_pos(C.OPPONENT_CARD_PLAY_POS.x,C.OPPONENT_CARD_PLAY_POS.y)
                self.opponent_played_card_sprite.add(cv_opp);self.all_visual_cards.add(cv_opp);anim_cards.append(cv_opp)

            self.set_status_message("Cartas em jogo...",0); self.pending_card_arrivals_for_reveal=len(anim_cards)
            if not anim_cards: self._on_card_played_animation_done(None)
            else:
                for c_card in anim_cards: c_card.on_target_reached_callback = self._on_card_played_animation_done
            return
        elif event_type=="ROUND_WINNER": self.current_round_data_for_winner_animation=event_data; self.set_status_message(f"{event_data.get('winner_name')} vence!",1.2); next_timer_id=C.UI_EVENT_ANIMATE_WINNER_COLLECTION; delay=1200
        elif event_type=="WAR_DECLARED": self.set_status_message("GUERRA!",1.5); delay=1500; self.is_war_active_visual = True
        elif event_type=="WAR_BET_CARDS":
            self.set_status_message("Apostando...",1.2); delay=1200; self.is_war_active_visual = True
            p1_b = event_data.get('player1_bet_count',0); p2_b = event_data.get('player2_bet_count',0)
            for i in range(p1_b):
                vc=VisualCard("BACK",C.PLAYER_DECK_POS.x,C.PLAYER_DECK_POS.y,is_face_up=False)
                tx=C.PLAYER_CARD_PLAY_POS.x + C.WAR_BET_PLAYER_OFFSET_X - (i*(C.CARD_WIDTH*0.15)); ty=C.PLAYER_CARD_PLAY_POS.y + C.WAR_BET_Y_OFFSET + (i*3)
                vc.set_target_pos(tx,ty); self.war_bet_cards_p1_sprites.add(vc);self.all_visual_cards.add(vc)
            for i in range(p2_b):
                vc=VisualCard("BACK",C.OPPONENT_DECK_POS.x,C.OPPONENT_DECK_POS.y,is_face_up=False)
                tx=C.OPPONENT_CARD_PLAY_POS.x + C.WAR_BET_OPPONENT_OFFSET_X + (i*(C.CARD_WIDTH*0.15)); ty=C.OPPONENT_CARD_PLAY_POS.y + C.WAR_BET_Y_OFFSET + (i*3)
                vc.set_target_pos(tx,ty); self.war_bet_cards_p2_sprites.add(vc);self.all_visual_cards.add(vc)
            next_timer_id = C.UI_EVENT_CONTINUE_GAME_SEQUENCE; delay = 1200
        elif event_type=="WAR_REVEAL_CARDS":
            self.set_status_message("Revelando Guerra!",1.0); self.current_round_data_for_winner_animation = None
            if self.player_played_card_sprite.sprite: self.player_played_card_sprite.sprite.kill()
            if self.opponent_played_card_sprite.sprite: self.opponent_played_card_sprite.sprite.kill()
            my_s = event_data.get('player1_reveal_card'); opp_s = event_data.get('player2_reveal_card')
            anim_cards=[];
            if my_s and my_s!="N/A": 
                cv=VisualCard(my_s,C.PLAYER_DECK_POS.x,C.PLAYER_DECK_POS.y,is_face_up=False)
                cv.set_target_pos(C.PLAYER_CARD_PLAY_POS.x,C.PLAYER_CARD_PLAY_POS.y)
                self.player_played_card_sprite.add(cv);self.all_visual_cards.add(cv);anim_cards.append(cv)
            if opp_s and opp_s!="N/A": 
                cv_opp = VisualCard(opp_s,C.OPPONENT_DECK_POS.x,C.OPPONENT_DECK_POS.y,is_face_up=False)
                cv_opp.set_target_pos(C.OPPONENT_CARD_PLAY_POS.x,C.OPPONENT_CARD_PLAY_POS.y)
                self.opponent_played_card_sprite.add(cv_opp);self.all_visual_cards.add(cv_opp);anim_cards.append(cv_opp)
            self.pending_card_arrivals_for_reveal=len(anim_cards); self.is_war_active_visual = True
            if not anim_cards: self._on_card_played_animation_done(None)
            else:
                for c_anim in anim_cards: c_anim.on_target_reached_callback = self._on_card_played_animation_done
            return
        elif event_type=="WAR_WINNER" or event_type=="WAR_WINNER_BY_WO": self.current_round_data_for_winner_animation=event_data; self.set_status_message(f"{event_data.get('winner_name')} VENCE A GUERRA!",1.8); next_timer_id=C.UI_EVENT_ANIMATE_WINNER_COLLECTION; delay=1800; self.is_war_active_visual = True
        elif event_type=="WAR_DECLARED_AGAIN": self.set_status_message("GUERRA DE NOVO!",1.5); delay=1500; self.is_war_active_visual = True
        elif event_type == "HAND_SIZES_UPDATE":
            self.player_hand_size=event_data.get('player1_hand_size'); self.opponent_hand_size=event_data.get('player2_hand_size')
            self.is_processing_visual_event = False; self._process_next_visual_event_from_queue(); return
        elif event_type == "GAME_OVER": self.set_status_message(f"FIM! {event_data.get('winner')} venceu. {event_data.get('reason','')}",0); self.is_game_over=True; self.action_button=None; self._create_menu_button("Fim - Menu"); self.is_processing_visual_event=False; self.event_animation_queue.clear(); return
        else: self.is_processing_visual_event=False; self._process_next_visual_event_from_queue(); return
        if next_timer_id: pygame.time.set_timer(next_timer_id,delay,True)

    def _on_card_played_animation_done(self,card_sprite):
        self.pending_card_arrivals_for_reveal-=1
        if self.pending_card_arrivals_for_reveal<=0:
            pygame.time.set_timer(C.UI_EVENT_REVEAL_CARDS_ON_TABLE,300,True)

    def handle_event(self,event):
        if self.log_display_panel.is_visible:
            if self.log_display_panel.handle_event(event): return
        if self.action_button: self.action_button.handle_event(event)
        if self.log_button: self.log_button.handle_event(event)

        if event.type==C.UI_EVENT_REVEAL_CARDS_ON_TABLE:
            pygame.time.set_timer(C.UI_EVENT_REVEAL_CARDS_ON_TABLE,0)
            self.flip_callback_count=0; self.expected_flips=0
            if self.player_played_card_sprite.sprite: self.expected_flips+=1
            if self.opponent_played_card_sprite.sprite: self.expected_flips+=1
            if self.expected_flips==0: self._check_both_flipped_and_continue(); return
            if self.player_played_card_sprite.sprite: self.player_played_card_sprite.sprite.start_flip(True,on_flip_done=self._check_both_flipped_and_continue)
            if self.opponent_played_card_sprite.sprite: self.opponent_played_card_sprite.sprite.start_flip(True,on_flip_done=self._check_both_flipped_and_continue)
        elif event.type==C.UI_EVENT_ANIMATE_WINNER_COLLECTION:
            pygame.time.set_timer(C.UI_EVENT_ANIMATE_WINNER_COLLECTION,0)
            if self.current_round_data_for_winner_animation:
                winner=self.current_round_data_for_winner_animation.get('winner_name'); e_type=self.current_round_data_for_winner_animation.get('type',"")
                is_war="WAR_WINNER" in e_type or "WAR_WINNER_BY_WO" in e_type
                if winner: self._animate_cards_to_winner(winner,war_context=is_war)
            else: pygame.time.set_timer(C.UI_EVENT_CONTINUE_GAME_SEQUENCE,100,True)
        elif event.type==C.UI_EVENT_CONTINUE_GAME_SEQUENCE:
            pygame.time.set_timer(C.UI_EVENT_CONTINUE_GAME_SEQUENCE,0)
            self.is_processing_visual_event=False; self._process_next_visual_event_from_queue()

    def _check_both_flipped_and_continue(self,card_sprite=None):
        self.flip_callback_count+=1
        if self.flip_callback_count>=self.expected_flips:
            self.flip_callback_count=0; self.expected_flips=0
            pygame.time.set_timer(C.UI_EVENT_CONTINUE_GAME_SEQUENCE,800,True)

    def _animate_cards_to_winner(self,winner_name,war_context=False):
        is_me_winner = (winner_name == self.my_player_obj_name)
        target_pos=C.PLAYER_WIN_PILE_POS if is_me_winner else C.OPPONENT_WIN_PILE_POS
        to_move=[];
        if self.player_played_card_sprite.sprite: to_move.append(self.player_played_card_sprite.sprite)
        if self.opponent_played_card_sprite.sprite: to_move.append(self.opponent_played_card_sprite.sprite)
        if war_context:
            to_move.extend(list(self.war_bet_cards_p1_sprites.sprites()))
            to_move.extend(list(self.war_bet_cards_p2_sprites.sprites()))

        if not to_move:
            pygame.time.set_timer(C.UI_EVENT_CONTINUE_GAME_SEQUENCE,100,True); return

        self.num_cards_collected_animation_done=0; self.expected_cards_to_collect_animation=len(to_move)
        self.player_played_card_sprite.empty(); self.opponent_played_card_sprite.empty()
        self.war_bet_cards_p1_sprites.empty(); self.war_bet_cards_p2_sprites.empty()

        def on_collected(card_killed):
            card_killed.kill(); self.num_cards_collected_animation_done+=1
            if self.num_cards_collected_animation_done>=self.expected_cards_to_collect_animation:
                self.current_round_data_for_winner_animation=None
                pygame.time.set_timer(C.UI_EVENT_CONTINUE_GAME_SEQUENCE,500,True)

        for i,card_v in enumerate(to_move):
            if card_v not in self.all_visual_cards: self.all_visual_cards.add(card_v)
            card_v.is_collecting_to_winner=True
            card_v.set_target_pos(target_pos.x+i*2,target_pos.y+i*2,speed=1800,on_reached=on_collected)

    def set_status_message(self,message,duration):
        self.status_message=message;self.message_display_time_total=duration;self.message_start_timer=time.time()

    def update(self,dt):
        self.all_visual_cards.update(dt)
        if self.message_display_time_total>0 and time.time()-self.message_start_timer>self.message_display_time_total: self.status_message="";self.message_display_time_total=0
        if self.log_display_panel.is_visible: self.log_display_panel.update(dt)

    def render(self):
        if self.background_image:
            self.screen.blit(self.background_image,(0,0))
        else:
            draw_linear_gradient_rect(self.screen, self.screen.get_rect(),
                                      C.SCREEN_BACKGROUND_START_COLOR, C.SCREEN_BACKGROUND_END_COLOR)

        center_table_area_rect = pygame.Rect(C.CENTER_TABLE_RECT_X, C.CENTER_TABLE_RECT_Y, C.CENTER_TABLE_RECT_WIDTH, C.CENTER_TABLE_RECT_HEIGHT)
        if len(C.TABLE_AREA_COLOR) == 4:
            table_surface = pygame.Surface(center_table_area_rect.size, pygame.SRCALPHA)
            table_surface.fill(C.TABLE_AREA_COLOR)
            self.screen.blit(table_surface, center_table_area_rect.topleft)
            pygame.draw.rect(self.screen, C.TABLE_AREA_BORDER_COLOR, center_table_area_rect, width=2, border_radius=C.UI_PANEL_BORDER_RADIUS)
        else:
            pygame.draw.rect(self.screen, C.TABLE_AREA_COLOR, center_table_area_rect, border_radius=C.UI_PANEL_BORDER_RADIUS)
            pygame.draw.rect(self.screen, C.TABLE_AREA_BORDER_COLOR, center_table_area_rect, width=2, border_radius=C.UI_PANEL_BORDER_RADIUS)

        back_img = card_graphics.get_card_surface("BACK")

        p_name_y = C.PLAYER_DECK_POS.y - self.font.get_height() - 5
        self._draw_text(self.my_player_obj_name,self.font,C.COLOR_OFF_WHITE,C.PLAYER_DECK_POS.x+C.CARD_WIDTH//2,p_name_y,center_x=True)
        if self.player_hand_size>0 or self._game_has_started_for_ui():
            if back_img: self.screen.blit(back_img,(C.PLAYER_DECK_POS.x,C.PLAYER_DECK_POS.y))
        p_count_y = C.PLAYER_DECK_POS.y+C.CARD_HEIGHT+self.hand_count_font.get_height()//2+8
        self._draw_text(f"{self.player_hand_size}",self.hand_count_font,C.COLOR_OFF_WHITE,C.PLAYER_DECK_POS.x+C.CARD_WIDTH//2,p_count_y,center_x=True)

        o_name_y = C.OPPONENT_DECK_POS.y + C.CARD_HEIGHT + 5
        self._draw_text(self.opponent_player_obj_name,self.font,C.COLOR_OFF_WHITE,C.OPPONENT_DECK_POS.x+C.CARD_WIDTH//2,o_name_y,center_x=True)
        if self.opponent_hand_size>0 or self._game_has_started_for_ui():
            if back_img: self.screen.blit(back_img,(C.OPPONENT_DECK_POS.x,C.OPPONENT_DECK_POS.y))
        o_count_y = C.OPPONENT_DECK_POS.y - self.hand_count_font.get_height() - 8
        self._draw_text(f"{self.opponent_hand_size}",self.hand_count_font,C.COLOR_OFF_WHITE,C.OPPONENT_DECK_POS.x+C.CARD_WIDTH//2,o_count_y,center_x=True)

        if self.game_logic and self.game_logic.current_round > 0 and not self.is_game_over:
            round_text = f"Rodada: {self.game_logic.current_round:02d}"
            self._draw_text(round_text, self.hand_count_font, C.COLOR_OFF_WHITE, C.SCREEN_WIDTH - 100, 25, center_x=True)

        self.all_visual_cards.draw(self.screen)
        if self.is_war_active_visual and not self.is_game_over:
            overlay = pygame.Surface((C.SCREEN_WIDTH, C.SCREEN_HEIGHT), pygame.SRCALPHA); overlay.fill((150,0,0,90)); self.screen.blit(overlay,(0,0))
            self._draw_text("GUERRA!", self.screen_header_font, C.COLOR_YELLOW_HIGHLIGHT, C.SCREEN_WIDTH//2, C.CENTER_TABLE_RECT_Y - C.CARD_HEIGHT // 2 - 20 ,center_x=True,center_y=True)

        if self.status_message:
            status_color = C.COLOR_RED_HIGHLIGHT if "GUERRA" in self.status_message.upper() or "VENCE A GUERRA" in self.status_message.upper() else C.COLOR_OFF_WHITE
            self._draw_text(self.status_message,self.status_font,status_color ,C.SCREEN_WIDTH//2,C.STATUS_MESSAGE_Y,center_x=True,center_y=True)

        if self.action_button: self.action_button.draw(self.screen)
        if self.log_button: self.log_button.draw(self.screen)
        if self.log_display_panel.is_visible: self.log_display_panel.render()

    def _game_has_started_for_ui(self):
        return self.game_logic is not None and \
               (self.player_hand_size > 0 or self.opponent_hand_size > 0 or \
                not self.event_animation_queue.is_empty() or \
                self.is_processing_visual_event or self.game_logic.current_round > 0)

    def cleanup_before_quit(self):
        pygame.time.set_timer(C.UI_EVENT_REVEAL_CARDS_ON_TABLE, 0)
        pygame.time.set_timer(C.UI_EVENT_ANIMATE_WINNER_COLLECTION, 0)
        pygame.time.set_timer(C.UI_EVENT_CONTINUE_GAME_SEQUENCE, 0)