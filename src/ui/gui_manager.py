import pygame
import sys
import os
from .menu_screen import MenuScreen
from .game_screen import GameScreen
from .rules_screen import RulesScreen
from game.war_game_logic import WarGameLogic
from . import constants as C
from . import card_graphics

class GUIManager:
    def __init__(self):
        pygame.init(); pygame.mixer.init(); pygame.font.init()
        self.screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        pygame.display.set_caption("Jogo de Guerra"); self.clock = pygame.time.Clock()
        if hasattr(card_graphics, 'preload_card_images'): card_graphics.preload_card_images()
        self.active_screen = None; self.game_logic_instance: WarGameLogic = None

        caminho_fonte_titulo_tema = os.path.join(C.FONT_ASSETS_PATH, C.FONT_FILENAME_THEME_TITLE) if C.FONT_FILENAME_THEME_TITLE else None
        caminho_fonte_corpo = os.path.join(C.FONT_ASSETS_PATH, C.FONT_FILENAME_BODY) if C.FONT_FILENAME_BODY else None
        
        caminho_fonte_cabecalho_regras = os.path.join(C.FONT_ASSETS_PATH, C.FONT_FILENAME_HEADER) if C.FONT_FILENAME_HEADER else caminho_fonte_titulo_tema
        caminho_fonte_secao_regras = os.path.join(C.FONT_ASSETS_PATH, C.FONT_FILENAME_SECTION_TITLE) if C.FONT_FILENAME_SECTION_TITLE else caminho_fonte_titulo_tema
        caminho_fonte_corpo_regras = caminho_fonte_corpo

        # Fontes Globais
        self.fonte_titulo_app = self._carregar_fonte_com_fallback(caminho_fonte_titulo_tema, C.FONT_SIZE_APP_TITLE, "verdana", bold=True)
        self.fonte_cabecalho_tela = self._carregar_fonte_com_fallback(caminho_fonte_titulo_tema, C.FONT_SIZE_SCREEN_HEADER, "verdana", bold=True)
        self.fonte_botao_menu = self._carregar_fonte_com_fallback(caminho_fonte_corpo, C.FONT_SIZE_MENU_BUTTON, "sans-serif", bold=True)
        self.fonte_botao_jogo = self._carregar_fonte_com_fallback(caminho_fonte_corpo, C.FONT_SIZE_GAME_ACTION_BUTTON, "sans-serif", bold=True)

        # Fontes específicas para a Tela de Regras
        self.fonte_regras_titulo_principal = self._carregar_fonte_com_fallback(caminho_fonte_cabecalho_regras, C.FONT_SIZE_SCREEN_HEADER + 4, "verdana", bold=True)
        self.fonte_regras_titulo_secao = self._carregar_fonte_com_fallback(caminho_fonte_secao_regras, C.FONT_SIZE_RULES_SECTION_TITLE + 4, "sans-serif", bold=True)
        self.fonte_regras_corpo_texto = self._carregar_fonte_com_fallback(caminho_fonte_corpo_regras, C.FONT_SIZE_RULES_BODY + 2, "sans-serif")
        self.fonte_regras_introducao = self._carregar_fonte_com_fallback(caminho_fonte_corpo_regras, C.FONT_SIZE_RULES_INTRO_TEXT, "sans-serif", bold=False, italic=True)

        # Fontes para LogDisplay e GameScreen
        self.fonte_titulo_painel_log = self._carregar_fonte_com_fallback(caminho_fonte_titulo_tema, C.FONT_SIZE_LOG_PANEL_TITLE, "sans-serif", bold=True)
        self.fonte_nome_jogador = self._carregar_fonte_com_fallback(caminho_fonte_corpo, C.FONT_SIZE_PLAYER_NAME, "sans-serif", bold=False)
        self.fonte_status_jogo = self._carregar_fonte_com_fallback(caminho_fonte_corpo, C.FONT_SIZE_GAME_STATUS, "sans-serif", bold=True)
        self.fonte_contagem_cartas = self._carregar_fonte_com_fallback(caminho_fonte_corpo, C.FONT_SIZE_HAND_COUNT, "sans-serif")

        self.mostrar_menu()

    def _carregar_fonte_com_fallback(self, caminho_fonte, tamanho, fonte_sistema_fallback="arial", bold=False, italic=False):
        target_font = None
        try:
            if caminho_fonte and os.path.exists(caminho_fonte):
                target_font = pygame.font.Font(caminho_fonte, tamanho)
            else:
                target_font = pygame.font.Font(None, tamanho)
            if target_font:
                target_font.set_bold(bold); target_font.set_italic(italic)
            return target_font
        except Exception:
            try: return pygame.font.SysFont(fonte_sistema_fallback, tamanho, bold, italic)
            except Exception: return pygame.font.Font(None, tamanho)

    def mostrar_menu(self):
        if self.active_screen and hasattr(self.active_screen, 'cleanup_before_quit'):
             self.active_screen.cleanup_before_quit()
        self.game_logic_instance = None
        self.active_screen = MenuScreen(self.screen, self, self.fonte_botao_menu)

    def iniciar_jogo_vs_maquina(self):
        if self.active_screen and hasattr(self.active_screen, 'cleanup_before_quit'):
             self.active_screen.cleanup_before_quit()
        self.game_logic_instance = WarGameLogic(player1_name="Você",player2_name="Máquina")
        self.active_screen=GameScreen(self.screen,self,self.game_logic_instance)

    def mostrar_regras(self):
        if self.active_screen and hasattr(self.active_screen, 'cleanup_before_quit'):
             self.active_screen.cleanup_before_quit()
        self.active_screen = RulesScreen(self.screen, self,
                                         self.fonte_regras_titulo_principal,
                                         self.fonte_regras_titulo_secao,
                                         self.fonte_regras_corpo_texto,
                                         self.fonte_botao_jogo,
                                         self.fonte_regras_introducao)

    def executar(self):
        rodando = True
        while rodando:
            dt = self.clock.tick(C.FPS) / 1000.0
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if self.active_screen and rodando:
                    self.active_screen.handle_event(evento)
            
            if not rodando:
                break
            
            if self.active_screen:
                self.active_screen.update(dt)
                self.active_screen.render()
            
            pygame.display.flip()
            
        if self.active_screen and hasattr(self.active_screen, 'cleanup_before_quit'):
            self.active_screen.cleanup_before_quit()
        pygame.quit()
        sys.exit()