import pygame
from . import constants as C
from .elements import Button
from . import card_graphics

class LogDisplay:
    def __init__(self, screen, game_screen_ref, log_entries_func):
        self.screen = screen
        self.game_screen = game_screen_ref
        self.log_entries_func = log_entries_func
        
        self.main_log_card_scale = 0.50
        self.main_log_card_w = int(C.CARD_WIDTH * self.main_log_card_scale)
        self.main_log_card_h = int(C.CARD_HEIGHT * self.main_log_card_scale)
        
        self.war_detail_card_scale = 0.40
        self.war_detail_card_w = int(C.CARD_WIDTH * self.war_detail_card_scale)
        self.war_detail_card_h = int(C.CARD_HEIGHT * self.war_detail_card_scale)

        self.is_visible = False
        
        gui_manager = self.game_screen.manager
        self.detail_font = gui_manager.fonte_contagem_cartas
        
        self.entry_summary_font = gui_manager.fonte_nome_jogador
        self.round_title_font = gui_manager.fonte_status_jogo
        self.panel_title_font = gui_manager.fonte_titulo_painel_log

        self.panel_rect = pygame.Rect(C.LOG_PANEL_X, C.LOG_PANEL_Y, C.LOG_PANEL_WIDTH, C.LOG_PANEL_HEIGHT)
        self.log_content_surface = None
        self.scroll_y = 0
        self.max_scroll = 0
        
        close_btn_size = 30
        self.close_button = Button(
            self.panel_rect.right - close_btn_size - 10, self.panel_rect.top + 10,
            close_btn_size, close_btn_size, "X",
            gui_manager.fonte_botao_jogo,
            action=self.game_screen._toggle_log_display,
            color=(180,50,50), hover_color=(220,80,80),
            text_color=C.COLOR_WHITE
        )
        self.all_log_entries_cache = []

    def _prepare_log_content(self):
        self.all_log_entries_cache = list(self.log_entries_func())
        if not self.all_log_entries_cache:
            bg_color_tuple = C.LOG_PANEL_BG_COLOR[:3] if len(C.LOG_PANEL_BG_COLOR) == 4 else C.LOG_PANEL_BG_COLOR
            self.log_content_surface = pygame.Surface((self.panel_rect.width - 40, 50))
            self.log_content_surface.fill(bg_color_tuple)
            text_surf = self.entry_summary_font.render("Nenhuma jogada registrada ainda.", True, C.LOG_TEXT_COLOR)
            self.log_content_surface.blit(text_surf, (10,10)); self.max_scroll = 0; self.scroll_y = 0
            return

        padding = 20; line_spacing = 8; entry_spacing = 30
        text_start_x_for_outcome = padding + self.main_log_card_w * 2 + C.CARD_SPACING * 2

        temp_surface_height_estimate = len(self.all_log_entries_cache) * (self.main_log_card_h + self.round_title_font.get_height() + 5 * (self.detail_font.get_height() + self.war_detail_card_h + line_spacing) + entry_spacing) + padding * 2
        content_width = int(self.panel_rect.width - 40 - C.LOG_SCROLL_BAR_WIDTH)

        temp_drawing_surface = pygame.Surface((content_width, temp_surface_height_estimate), pygame.SRCALPHA)
        temp_drawing_surface.fill((0,0,0,0))

        current_y = padding
        for i, entry in enumerate(self.all_log_entries_cache):
            if i > 0:
                pygame.draw.line(temp_drawing_surface, (70,70,90, 150),
                                 (padding // 2, current_y - entry_spacing // 2),
                                 (content_width - padding // 2, current_y - entry_spacing // 2), 1)

            round_text = f"Rodada {entry.get('round', '?')}"
            ts_round = self.round_title_font.render(round_text, True, C.COLOR_YELLOW_HIGHLIGHT)
            temp_drawing_surface.blit(ts_round, (padding, current_y));
            current_y_for_main_content = current_y + ts_round.get_height() + line_spacing

            p1_played_str = entry.get("p1_played_str", "N/A")
            p2_played_str = entry.get("p2_played_str", "N/A")
            cards_y_pos = current_y_for_main_content

            if p1_played_str != "N/A":
                p1_s = pygame.transform.smoothscale(card_graphics.get_card_surface(p1_played_str), (self.main_log_card_w, self.main_log_card_h))
                temp_drawing_surface.blit(p1_s, (padding, cards_y_pos))
            if p2_played_str != "N/A":
                p2_s = pygame.transform.smoothscale(card_graphics.get_card_surface(p2_played_str), (self.main_log_card_w, self.main_log_card_h))
                temp_drawing_surface.blit(p2_s, (padding + self.main_log_card_w + C.CARD_SPACING, cards_y_pos))

            winner = entry.get("winner_name", "N/A"); entry_type = entry.get("type", "")
            result_line1 = ""; result_line2 = f"Vencedor: {winner}"
            if entry_type == "war_round": result_line1 = "GUERRA!"

            result_text_y_centered = cards_y_pos + self.main_log_card_h // 2
            y_offset_for_result = 0
            if result_line1:
                res_s1 = self.entry_summary_font.render(result_line1, True, C.COLOR_RED_HIGHLIGHT)
                res_r1 = res_s1.get_rect(left=text_start_x_for_outcome, centery=result_text_y_centered - res_s1.get_height()//2 -1)
                temp_drawing_surface.blit(res_s1, res_r1); y_offset_for_result = res_s1.get_height()//2 +1
            res_s2 = self.entry_summary_font.render(result_line2, True, C.LOG_TEXT_COLOR)
            res_r2 = res_s2.get_rect(left=text_start_x_for_outcome, centery=result_text_y_centered + y_offset_for_result)
            temp_drawing_surface.blit(res_s2, res_r2)
            current_y = cards_y_pos + self.main_log_card_h + line_spacing

            if entry.get("war_events_log"):
                war_indent = padding + 10
                war_title_surf = self.detail_font.render("Detalhes da Guerra:", True, C.COLOR_YELLOW_HIGHLIGHT)
                temp_drawing_surface.blit(war_title_surf, (war_indent, current_y))
                current_y += war_title_surf.get_height() + line_spacing
                detail_text_indent = war_indent + 10

                for we in entry["war_events_log"]:
                    step = we.get("step", "Passo"); detail_line_y_start = current_y
                    text_for_step_prefix = f"  • {step}: "
                    text_for_step_suffix = ""
                    text_color = C.LOG_TEXT_COLOR

                    if step == "Fase de Guerra":
                        pot_str_list = we.get('pot_inicial_fase_str', [])
                        pot_display = ", ".join(pot_str_list[:min(len(pot_str_list), 3)]) + ("..." if len(pot_str_list) > 3 else "")
                        text_for_step_suffix = f"Pote Inicial: [{pot_display}]"
                        text_color = (190,190,190)
                    elif step == "Apostas da Guerra":
                        p1_b_s = we.get('p1_bet_str',[]); p2_b_s = we.get('p2_bet_str',[])
                        text_for_step_suffix = f"P1 apostou {len(p1_b_s)}, P2 apostou {len(p2_b_s)}"
                    elif step == "Revelação da Guerra":
                        text_for_step_suffix = ""
                    elif "Vencedor da Guerra" in step:
                        winner_text = we.get('winner', 'N/A')
                        reason_text = f" ({we.get('reason')})" if 'reason' in we and we.get('reason') else ""
                        text_for_step_suffix = f"{winner_text}{reason_text}"
                        text_color = C.COLOR_YELLOW_HIGHLIGHT
                    elif "Nova Guerra" in step:
                        text_for_step_suffix = "Empate! Nova Guerra."
                        text_color = C.COLOR_RED_HIGHLIGHT
                    elif "Empate na Guerra" in step:
                        text_for_step_suffix = f"Empate (sem revelação). Pote de {we.get('pot_size_lost',0)} perdido."
                    else:
                        text_for_step_suffix = f"{str(we)[:60]}"

                    step_text_full = text_for_step_prefix + text_for_step_suffix
                    ts_step = self.detail_font.render(step_text_full,True,text_color)
                    temp_drawing_surface.blit(ts_step,(detail_text_indent, detail_line_y_start))

                    current_step_visual_height = ts_step.get_height()
                    cards_y_visual = detail_line_y_start + ts_step.get_height() + 3
                    cards_x_curr = detail_text_indent + 20

                    if step == "Apostas da Guerra":
                        p1_b_list = we.get('p1_bet_str',[]); p2_b_list = we.get('p2_bet_str',[])
                        for _ in p1_b_list: img=pygame.transform.smoothscale(card_graphics.get_card_surface("BACK"),(self.war_detail_card_w,self.war_detail_card_h)); temp_drawing_surface.blit(img,(cards_x_curr,cards_y_visual)); cards_x_curr+=self.war_detail_card_w+3
                        if p1_b_list and p2_b_list: vs_s=self.detail_font.render("vs",True,C.LOG_TEXT_COLOR); temp_drawing_surface.blit(vs_s,(cards_x_curr,cards_y_visual+self.war_detail_card_h//2-vs_s.get_height()//2)); cards_x_curr+=vs_s.get_width()+3
                        for _ in p2_b_list: img=pygame.transform.smoothscale(card_graphics.get_card_surface("BACK"),(self.war_detail_card_w,self.war_detail_card_h)); temp_drawing_surface.blit(img,(cards_x_curr,cards_y_visual)); cards_x_curr+=self.war_detail_card_w+3
                        if p1_b_list or p2_b_list: current_step_visual_height += self.war_detail_card_h + 3

                    elif step == "Revelação da Guerra":
                        p1_r = we.get('p1_reveal_str','N/A'); p2_r = we.get('p2_reveal_str','N/A')
                        if p1_r!="N/A": s1=pygame.transform.smoothscale(card_graphics.get_card_surface(p1_r),(self.war_detail_card_w,self.war_detail_card_h)); temp_drawing_surface.blit(s1,(cards_x_curr,cards_y_visual)); cards_x_curr+=self.war_detail_card_w+3
                        if p1_r!="N/A" and p2_r!="N/A": vs_r=self.detail_font.render("vs",True,C.LOG_TEXT_COLOR); temp_drawing_surface.blit(vs_r,(cards_x_curr,cards_y_visual+self.war_detail_card_h//2-vs_r.get_height()//2)); cards_x_curr+=vs_r.get_width()+3
                        if p2_r!="N/A": s2=pygame.transform.smoothscale(card_graphics.get_card_surface(p2_r),(self.war_detail_card_w,self.war_detail_card_h)); temp_drawing_surface.blit(s2,(cards_x_curr,cards_y_visual))
                        if p1_r != "N/A" or p2_r != "N/A": current_step_visual_height += self.war_detail_card_h + 3

                    current_y += current_step_visual_height + line_spacing // 2
            current_y += entry_spacing

        actual_content_height = current_y
        self.log_content_surface = pygame.Surface((content_width, actual_content_height), pygame.SRCALPHA)
        self.log_content_surface.fill((0,0,0,0))
        self.log_content_surface.blit(temp_drawing_surface, (0,0))

        title_h = self.panel_title_font.get_height()
        header_footer_padding = title_h + 30 + 40
        content_area_h_available = self.panel_rect.height - header_footer_padding
        self.max_scroll = max(0, self.log_content_surface.get_height() - content_area_h_available)

        if self.scroll_y > self.max_scroll: self.scroll_y = self.max_scroll
        if self.scroll_y < 0: self.scroll_y = 0

    def show(self):
        self._prepare_log_content()
        self.is_visible = True
        self.scroll_y = self.max_scroll
    def hide(self): self.is_visible = False

    def handle_event(self, event):
        if not self.is_visible: return False
        try:
            if self.close_button.handle_event(event): return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                content_top_y = self.panel_rect.top + self.panel_title_font.get_height() + 30
                content_bottom_y = self.panel_rect.bottom - 40
                effective_content_width = self.panel_rect.width - 40 - (C.LOG_SCROLL_BAR_WIDTH if self.max_scroll > 0 else 0)
                scroll_area_check = pygame.Rect(
                    self.panel_rect.left + 20,
                    content_top_y,
                    effective_content_width,
                    content_bottom_y - content_top_y
                )
                if scroll_area_check.collidepoint(event.pos):
                    if event.button == 4: self.scroll_y = max(0, self.scroll_y - 60)
                    elif event.button == 5: self.scroll_y = min(self.max_scroll, self.scroll_y + 60)
                    return True
        except Exception as e: print(f"Erro em LogDisplay.handle_event: {e}")
        return False

    def update(self, dt): pass

    def render(self):
        if not self.is_visible: return
        panel_surf = pygame.Surface(self.panel_rect.size, pygame.SRCALPHA); panel_surf.fill(C.LOG_PANEL_BG_COLOR)
        self.screen.blit(panel_surf, self.panel_rect.topleft)
        pygame.draw.rect(self.screen, C.LOG_PANEL_BORDER_COLOR, self.panel_rect, 3, border_radius=12)

        title_surf = self.panel_title_font.render("Histórico de Jogadas", True, C.COLOR_WHITE)
        self.screen.blit(title_surf, title_surf.get_rect(centerx=self.panel_rect.centerx, y=self.panel_rect.top + 15))

        content_render_area_rect = pygame.Rect(
            self.panel_rect.left + 20, self.panel_rect.top + title_surf.get_height() + 30,
            self.panel_rect.width - 40 - (C.LOG_SCROLL_BAR_WIDTH if self.max_scroll > 0 else 0),
            self.panel_rect.height - (title_surf.get_height() + 30) - 40)

        if self.log_content_surface:
            try:
                target_surface_for_log_content = self.screen.subsurface(content_render_area_rect)
                log_bg_rgb = C.LOG_PANEL_BG_COLOR[:3]
                target_surface_for_log_content.fill(log_bg_rgb)
                target_surface_for_log_content.blit(self.log_content_surface, (0, -self.scroll_y))
            except ValueError as e:
                 print(f"Erro ao criar subsuperfície para LogDisplay: {e}, rect: {content_render_area_rect}")
                 pass

        if self.max_scroll > 0:
            scrollbar_bg_rect = pygame.Rect(content_render_area_rect.right + 5, content_render_area_rect.top, C.LOG_SCROLL_BAR_WIDTH - 10, content_render_area_rect.height)
            pygame.draw.rect(self.screen, (50,50,80, 150), scrollbar_bg_rect, border_radius=5)
            content_total_h = self.log_content_surface.get_height() if self.log_content_surface else content_render_area_rect.height
            if content_total_h > 0 and content_render_area_rect.height < content_total_h :
                visible_h_ratio = content_render_area_rect.height / content_total_h
                handle_height = max(20, content_render_area_rect.height * visible_h_ratio)
                scroll_ratio = self.scroll_y / self.max_scroll if self.max_scroll > 0 else 0
                handle_y = content_render_area_rect.top + (content_render_area_rect.height - handle_height) * scroll_ratio
                scrollbar_handle_rect = pygame.Rect(scrollbar_bg_rect.left, handle_y, scrollbar_bg_rect.width, handle_height)
                pygame.draw.rect(self.screen, (100,100,150, 200), scrollbar_handle_rect, border_radius=5)
        self.close_button.draw(self.screen)