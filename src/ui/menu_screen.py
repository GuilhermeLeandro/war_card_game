import pygame
import os
from .base_screen import BaseScreen
from .elements import Button
from . import constants as C
from .ui_utils import draw_linear_gradient_rect

class MenuScreen(BaseScreen):
    def __init__(self, screen, manager, font_for_buttons: pygame.font.Font):
        super().__init__(screen, manager, font_for_buttons)
        self.title_font = manager.fonte_titulo_app
        self.button_font_object = font_for_buttons

        self.buttons = []
        btn_width = 480; btn_height = 70; spacing = 30
        num_buttons = 3
        total_button_block_height = (num_buttons * btn_height) + ((num_buttons - 1) * spacing)
        
        panel_h = C.SCREEN_HEIGHT * 0.75
        panel_y_start = (C.SCREEN_HEIGHT - panel_h) // 2 + 20
        
        title_approx_height = C.FONT_SIZE_APP_TITLE * 1.5 
        buttons_area_start_y = panel_y_start + title_approx_height
        buttons_area_height = panel_h - title_approx_height - (C.UI_PANEL_BORDER_RADIUS * 2)
        
        block_start_y = buttons_area_start_y + (buttons_area_height - total_button_block_height) // 2

        button_data = [
            ("Jogar Guerra (vs. Máquina)", self.manager.iniciar_jogo_vs_maquina,
             C.MENU_BUTTON_BG_NORMAL_COLOR, C.MENU_BUTTON_BG_HOVER_COLOR),
            ("Regras do Jogo", self.manager.mostrar_regras,
             C.MENU_BUTTON_BG_NORMAL_COLOR, C.MENU_BUTTON_BG_HOVER_COLOR),
            ("Sair", self._quit_game,
             (130, 40, 40), (160, 70, 70))
        ]

        for i, (text, action, color_normal, color_hover) in enumerate(button_data):
            button_y = block_start_y + i * (btn_height + spacing)
            self.buttons.append(Button(
                C.SCREEN_WIDTH//2-btn_width//2, button_y, btn_width, btn_height, text,
                self.button_font_object,
                action=action,
                color=color_normal, hover_color=color_hover,
                text_color=C.MENU_BUTTON_TEXT_COLOR,
                border_radius=10,
                border_color=C.MENU_BUTTON_BORDER_COLOR, border_width=2
            ))
        
        self.background_image = None
        try:
            bg_path = os.path.join(C.BACKGROUND_ASSETS_PATH, 'menu_felt_background.jpg')
            if os.path.exists(bg_path):
                 self.background_image = pygame.image.load(bg_path).convert()
                 self.background_image = pygame.transform.scale(self.background_image, (C.SCREEN_WIDTH,C.SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Erro ao carregar imagem de fundo do menu: {e}")
            self.background_image = None

    def _quit_game(self): pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def handle_event(self, event):
        for button in self.buttons:
            if button.handle_event(event): return
            
    def update(self, dt): pass
    
    def render(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0,0))
        else:
            draw_linear_gradient_rect(self.screen, self.screen.get_rect(),
                                      C.SCREEN_BACKGROUND_START_COLOR, C.SCREEN_BACKGROUND_END_COLOR)

        panel_w = C.SCREEN_WIDTH * 0.65; panel_h = C.SCREEN_HEIGHT * 0.75
        panel_x = (C.SCREEN_WIDTH - panel_w) // 2; panel_y = (C.SCREEN_HEIGHT - panel_h) // 2 + 20
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        panel_surf = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        panel_surf.fill(C.MENU_PANEL_COLOR)
        pygame.draw.rect(panel_surf, C.COLOR_GOLD_ACCENT, panel_surf.get_rect(), 4, border_radius=C.UI_PANEL_BORDER_RADIUS)
        self.screen.blit(panel_surf, panel_rect.topleft)

        title_y_pos = panel_y + C.FONT_SIZE_APP_TITLE * 0.7
        self._draw_text("Jogo de Guerra", self.title_font, C.COLOR_LIGHT_GOLD_TEXT, C.SCREEN_WIDTH//2, title_y_pos, center_x=True)
        for b in self.buttons: b.draw(self.screen)