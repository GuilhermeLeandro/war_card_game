# src/ui/rules_screen.py
import pygame
from . import constants as C
from .base_screen import BaseScreen
from .elements import Button
from .ui_utils import draw_linear_gradient_rect
from . import card_graphics

class RulesScreen(BaseScreen):
    def __init__(self, screen, manager, fonte_titulo_principal_regras, fonte_titulo_secao_regras, fonte_corpo_regras, fonte_botao, fonte_introducao_regras):
        super().__init__(screen, manager, fonte_corpo_regras)
        self.fonte_titulo_principal_regras = fonte_titulo_principal_regras
        self.fonte_titulo_secao_regras = fonte_titulo_secao_regras
        self.fonte_introducao_regras = fonte_introducao_regras

        self.cor_fundo_painel = C.MENU_PANEL_COLOR
        self.cor_borda_painel = C.COLOR_GOLD_ACCENT
        self.cor_titulo_principal = C.RULES_MAIN_TITLE_COLOR
        self.cor_titulo_secao = C.RULES_SECTION_TITLE_COLOR 
        self.cor_texto_corpo = C.RULES_TEXT_BODY_COLOR
        self.cor_linha_divisora = C.RULES_DIVIDER_LINE_COLOR
        self.cor_fundo_tela_inicio = C.RULES_BACKGROUND_START_COLOR 
        self.cor_fundo_tela_fim = C.RULES_BACKGROUND_END_COLOR 

        self.margem_painel_x = C.RULES_PANEL_MARGIN_X
        self.margem_painel_y = C.RULES_PANEL_MARGIN_Y
        self.largura_borda_painel_attr = C.RULES_PANEL_BORDER_WIDTH
        self.padding_conteudo_painel = C.RULES_PANEL_CONTENT_PADDING

        self.padding_lateral_texto_interno = C.RULES_TEXT_SIDE_PADDING_INSIDE_PANEL
        self.largura_scrollbar = C.RULES_SCROLLBAR_WIDTH
        self.padding_scrollbar = C.RULES_SCROLLBAR_PADDING
        
        self.y_inicio_titulo_principal_no_painel = self.padding_conteudo_painel 
        self.y_inicio_texto_scroll_no_painel = self.y_inicio_titulo_principal_no_painel + self.fonte_titulo_principal_regras.get_height() + 25
        
        self.espacamento_secao = C.RULES_SECTION_SPACING_AFTER
        self.espacamento_paragrafo = C.RULES_PARAGRAPH_SPACING_AFTER
        self.espacamento_item_lista = C.RULES_LIST_ITEM_SPACING_AFTER
        self.espacamento_interno_linha = C.RULES_LINE_SPACING_INTERNAL
        self.margem_divisor_y = C.RULES_DIVIDER_MARGIN_Y

        self.escala_cartas_exemplo = C.RULES_EXAMPLE_CARD_SCALE
        self.largura_carta_exemplo = C.RULES_EXAMPLE_CARD_WIDTH
        self.altura_carta_exemplo = C.RULES_EXAMPLE_CARD_HEIGHT
        self.espacamento_x_cartas_exemplo = C.RULES_EXAMPLE_CARD_SPACING_X
        self.margem_y_cartas_exemplo = C.RULES_EXAMPLE_CARD_MARGIN_Y

        altura_botao_voltar_total = C.GAME_ACTION_BUTTON_HEIGHT + 10
        espaco_necessario_para_botao = C.RULES_BUTTON_Y_OFFSET_FROM_BOTTOM + altura_botao_voltar_total + 20

        self.rect_painel = pygame.Rect(
            self.margem_painel_x,
            self.margem_painel_y,
            C.SCREEN_WIDTH - (self.margem_painel_x * 2),
            C.SCREEN_HEIGHT - (self.margem_painel_y * 2) - espaco_necessario_para_botao
        )

        self.rect_area_conteudo_viewport = pygame.Rect(
            self.rect_painel.left + self.padding_conteudo_painel,
            self.rect_painel.top + self.y_inicio_texto_scroll_no_painel,
            self.rect_painel.width - (self.padding_conteudo_painel * 2) - self.largura_scrollbar - self.padding_scrollbar,
            self.rect_painel.height - self.y_inicio_texto_scroll_no_painel - self.padding_conteudo_painel
        )

        max_r_text = "um limite"
        if hasattr(self.manager, 'game_logic_instance') and self.manager.game_logic_instance:
            max_r_text = str(self.manager.game_logic_instance.max_rounds)

        self.linhas_texto_regras = [
            # ... (linhas_texto_regras como antes, usando self.cor_... para as cores)
            ("Bem-vindo ao clássico jogo de cartas Guerra, também conhecido como Batalha!", "introducao_corpo", self.cor_texto_corpo),
            ("", "divisor", None),
            ("Objetivo do Jogo", "titulo_secao", self.cor_titulo_secao),
            ("Ser o primeiro jogador a conquistar todas as cartas do baralho!", "corpo_texto", self.cor_texto_corpo),
            ("", "divisor", None),
            ("Preparação", "titulo_secao", self.cor_titulo_secao),
            ("1. Utiliza-se um baralho padrão de 52 cartas.", "item_lista", self.cor_texto_corpo),
            ("2. O baralho é embaralhado e dividido igualmente entre os dois jogadores (Você e a Máquina).", "item_lista", self.cor_texto_corpo),
            ("3. Cada jogador mantém sua pilha de cartas virada para baixo à sua frente.", "item_lista", self.cor_texto_corpo),
            ("", "divisor", None),
            ("Hierarquia das Cartas", "titulo_secao", self.cor_titulo_secao),
            ("A ordem das cartas, da menor para a maior, é:", "corpo_texto", self.cor_texto_corpo),
            ("", "cartas_exemplo", None),
            ("Os naipes (Copas, Ouros, Paus, Espadas) não influenciam o valor da carta em um jogo padrão de Guerra.", "corpo_texto_pequeno_recuo", self.cor_texto_corpo),
            ("", "divisor", None),
            ("Como Jogar uma Rodada", "titulo_secao", self.cor_titulo_secao),
            ("1. A cada rodada, ambos os jogadores viram simultaneamente a carta do topo de suas pilhas.", "item_lista", self.cor_texto_corpo),
            ("2. As cartas reveladas são comparadas com base na hierarquia acima.", "item_lista", self.cor_texto_corpo),
            ("3. A carta de maior valor vence a rodada.", "item_lista", self.cor_texto_corpo),
            ("4. O vencedor coleta ambas as cartas jogadas e as adiciona ao fundo de sua própria pilha.", "item_lista", self.cor_texto_corpo),
            ("", "divisor", None),
            ("Guerra (Quando há um Empate!)", "titulo_secao", self.cor_titulo_secao),
            ("1. Se as cartas jogadas na rodada tiverem o mesmo valor, uma **GUERRA** é declarada!", "item_lista_destaque", self.cor_texto_corpo),
            ("2. Para a Guerra, cada jogador coloca **três cartas** da sua pilha viradas para baixo sobre a mesa (esta é a 'aposta de guerra').", "item_lista", self.cor_texto_corpo),
            ("3. Em seguida, cada jogador vira uma **quarta carta** para cima.", "item_lista", self.cor_texto_corpo),
            ("4. A carta virada para cima de maior valor vence a Guerra. O vencedor coleta **TODAS** as cartas da mesa.", "item_lista_destaque", self.cor_texto_corpo),
            ("5. Se as cartas de revelação da Guerra também forem iguais, o processo de Guerra se repete.", "item_lista", self.cor_texto_corpo),
            ("6. Se um jogador não tiver cartas para completar a Guerra, ele perde automaticamente a Guerra.", "item_lista", self.cor_texto_corpo),
            ("", "divisor", None),
            ("Fim do Jogo", "titulo_secao", self.cor_titulo_secao),
            (f"O jogo continua até que um jogador conquiste todas as 52 cartas. Alternativamente, se um limite de **{max_r_text} rodadas** for atingido, o jogador com mais cartas nesse momento é declarado o vencedor.", "corpo_texto_destaque", self.cor_texto_corpo),
            ("", "espaco_grande_final", None)
        ]

        self.scroll_y = 0
        self.altura_conteudo_total = 0
        self.superficie_conteudo_scroll = None
        self.itens_renderizaveis = []

        self.superficies_cartas_exemplo = []
        ranks_exemplo = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Valete", "Dama", "Rei", "Ás"]
        naipe_exemplo = "Ouros"
        for rank in ranks_exemplo:
            id_carta = f"{rank} de {naipe_exemplo}"
            surf = card_graphics.get_card_surface(id_carta)
            if surf:
                surf_escalada = pygame.transform.smoothscale(surf, (self.largura_carta_exemplo, self.altura_carta_exemplo))
                self.superficies_cartas_exemplo.append(surf_escalada)

        largura_botao_voltar = 280
        self.botao_voltar = Button(
            C.SCREEN_WIDTH // 2 - (largura_botao_voltar // 2),
            C.SCREEN_HEIGHT - C.RULES_BUTTON_Y_OFFSET_FROM_BOTTOM,
            largura_botao_voltar, altura_botao_voltar_total, "Voltar ao Menu",
            fonte_botao,
            action=self.manager.mostrar_menu,
            color=C.GAME_BUTTON_BG_NORMAL_COLOR,
            hover_color=C.GAME_BUTTON_BG_HOVER_COLOR,
            text_color=C.GAME_BUTTON_TEXT_COLOR
        )
        self._preparar_conteudo_texto()

    def _preparar_conteudo_texto(self):
        self.itens_renderizaveis = []
        y_atual = 0

        largura_disponivel_conteudo = self.rect_area_conteudo_viewport.width - (self.padding_lateral_texto_interno * 2)
        recuo_base_conteudo = self.padding_lateral_texto_interno
        recuo_item_lista_conteudo = recuo_base_conteudo + 30
        recuo_sub_item_lista_conteudo = recuo_item_lista_conteudo + 25

        for texto_item, tipo_item, cor_parametro in self.linhas_texto_regras:
            fonte_usar = self.font
            recuo_x_atual = recuo_base_conteudo
            espaco_apos_item = self.espacamento_paragrafo
            cor_texto = cor_parametro
            centralizado = False
            negrito = False

            if tipo_item == "titulo_secao":
                fonte_usar = self.fonte_titulo_secao_regras
                espaco_apos_item = self.espacamento_secao
            elif tipo_item == "introducao_corpo":
                fonte_usar = self.fonte_introducao_regras
                centralizado = True
                espaco_apos_item = self.espacamento_paragrafo * 1.8
            elif tipo_item == "corpo_texto" or tipo_item == "corpo_texto_destaque" or tipo_item == "corpo_texto_pequeno_recuo":
                if tipo_item == "corpo_texto_destaque": negrito = True
                if tipo_item == "corpo_texto_pequeno_recuo": recuo_x_atual = recuo_base_conteudo + 15
            elif tipo_item == "item_lista" or tipo_item == "item_lista_destaque":
                recuo_x_atual = recuo_item_lista_conteudo
                if tipo_item == "item_lista_destaque": negrito = True
                espaco_apos_item = self.espacamento_item_lista
            elif tipo_item == "divisor":
                y_atual += self.margem_divisor_y
                self.itens_renderizaveis.append( (None, "linha_divisora", 0, y_atual) )
                y_atual += 2 
                y_atual += self.margem_divisor_y 
                continue
            elif tipo_item == "cartas_exemplo":
                self.itens_renderizaveis.append((None, "linha_cartas_exemplo", 0, y_atual))
                y_atual += self.altura_carta_exemplo + self.margem_y_cartas_exemplo * 2
                espaco_apos_item = self.espacamento_paragrafo
            elif tipo_item == "espaco_grande_final":
                y_atual += self.espacamento_paragrafo * 2.5
                continue

            estado_negrito_original = fonte_usar.get_bold()
            fonte_usar.set_bold(negrito)

            palavras = texto_item.split(' ')
            segmentos_linha_texto = []
            linha_texto_atual = ""
            largura_maxima_linha = largura_disponivel_conteudo
            if not centralizado:
                 largura_maxima_linha -= (recuo_x_atual - recuo_base_conteudo)

            for palavra in palavras:
                linha_teste = linha_texto_atual + palavra + " "
                if fonte_usar.size(linha_teste)[0] < largura_maxima_linha:
                    linha_texto_atual = linha_teste
                else:
                    segmentos_linha_texto.append(linha_texto_atual.strip())
                    linha_texto_atual = palavra + " "
            segmentos_linha_texto.append(linha_texto_atual.strip())

            y_render_linha = y_atual
            for segmento_linha in segmentos_linha_texto:
                if segmento_linha:
                    surf_texto = fonte_usar.render(segmento_linha, True, cor_texto)
                    pos_x = recuo_x_atual
                    if centralizado:
                        pos_x = recuo_base_conteudo + (largura_disponivel_conteudo - surf_texto.get_width()) // 2
                    self.itens_renderizaveis.append((surf_texto, "texto", pos_x, y_render_linha))
                    y_render_linha += surf_texto.get_height() + self.espacamento_interno_linha

            y_atual = y_render_linha
            if segmentos_linha_texto:
                 y_atual -= self.espacamento_interno_linha
            y_atual += espaco_apos_item
            fonte_usar.set_bold(estado_negrito_original)

        self.altura_conteudo_total = y_atual

        if self.altura_conteudo_total > 0:
            self.superficie_conteudo_scroll = pygame.Surface((self.rect_area_conteudo_viewport.width, self.altura_conteudo_total), pygame.SRCALPHA)
            self.superficie_conteudo_scroll.fill((0,0,0,0))

            for surf_item, tipo_desenho_item, x_no_conteudo, y_no_conteudo in self.itens_renderizaveis:
                if tipo_desenho_item == "texto" and surf_item:
                    self.superficie_conteudo_scroll.blit(surf_item, (x_no_conteudo, y_no_conteudo))
                elif tipo_desenho_item == "linha_divisora":
                    pygame.draw.line(self.superficie_conteudo_scroll, self.cor_linha_divisora,
                                     (recuo_base_conteudo, y_no_conteudo),
                                     (self.rect_area_conteudo_viewport.width - recuo_base_conteudo, y_no_conteudo), 2)
                elif tipo_desenho_item == "linha_cartas_exemplo":
                    y_cartas_no_conteudo = y_no_conteudo + self.margem_y_cartas_exemplo
                    largura_total_cartas = (len(self.superficies_cartas_exemplo) * self.largura_carta_exemplo) + \
                                           ((len(self.superficies_cartas_exemplo) - 1) * self.espacamento_x_cartas_exemplo)
                    x_inicio_cartas = recuo_base_conteudo + (largura_disponivel_conteudo - largura_total_cartas) // 2
                    if x_inicio_cartas < recuo_base_conteudo: x_inicio_cartas = recuo_base_conteudo

                    x_atual_carta = x_inicio_cartas
                    for surf_carta in self.superficies_cartas_exemplo:
                        self.superficie_conteudo_scroll.blit(surf_carta, (x_atual_carta, y_cartas_no_conteudo))
                        x_atual_carta += self.largura_carta_exemplo + self.espacamento_x_cartas_exemplo
        else:
            self.superficie_conteudo_scroll = None
        
        self.scroll_max = max(0, self.altura_conteudo_total - self.rect_area_conteudo_viewport.height)

    def handle_event(self, event):
        if self.botao_voltar.handle_event(event): return
        mouse_pos = pygame.mouse.get_pos()
        if self.rect_area_conteudo_viewport.collidepoint(mouse_pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.scroll_y = max(0, self.scroll_y - 50)
                elif event.button == 5:
                    self.scroll_y = min(self.scroll_max, self.scroll_y + 50)

    def update(self, dt):
        pass

    def render(self):
        draw_linear_gradient_rect(self.screen, self.screen.get_rect(),
                                  self.cor_fundo_tela_inicio, self.cor_fundo_tela_fim)

        pygame.draw.rect(self.screen, self.cor_fundo_painel, self.rect_painel, border_radius=C.UI_PANEL_BORDER_RADIUS)
        pygame.draw.rect(self.screen, self.cor_borda_painel, self.rect_painel, self.largura_borda_painel_attr, border_radius=C.UI_PANEL_BORDER_RADIUS)

        surf_titulo_principal = self.fonte_titulo_principal_regras.render("Regras do Jogo", True, self.cor_titulo_principal)
        rect_titulo_principal = surf_titulo_principal.get_rect(centerx=self.rect_painel.centerx,
                                                               top=self.rect_painel.top + self.padding_conteudo_painel)
        self.screen.blit(surf_titulo_principal, rect_titulo_principal)

        if self.superficie_conteudo_scroll:
            area_visivel_do_scroll = pygame.Rect(0, self.scroll_y,
                                                 self.rect_area_conteudo_viewport.width, 
                                                 self.rect_area_conteudo_viewport.height)
            self.screen.blit(self.superficie_conteudo_scroll, self.rect_area_conteudo_viewport.topleft, area_visivel_do_scroll)

        if self.scroll_max > 0:
            rect_trilha_scrollbar = pygame.Rect(
                self.rect_area_conteudo_viewport.right + self.padding_scrollbar,
                self.rect_area_conteudo_viewport.top,
                self.largura_scrollbar,
                self.rect_area_conteudo_viewport.height
            )
            pygame.draw.rect(self.screen, (50, 50, 50, 150), rect_trilha_scrollbar, border_radius=self.largura_scrollbar // 2)

            if self.altura_conteudo_total > self.rect_area_conteudo_viewport.height:
                ratio_altura_manipulador = self.rect_area_conteudo_viewport.height / self.altura_conteudo_total if self.altura_conteudo_total > 0 else 0
                altura_manipulador = max(20, self.rect_area_conteudo_viewport.height * ratio_altura_manipulador)
                
                ratio_scroll = self.scroll_y / self.scroll_max if self.scroll_max > 0 else 0
                pos_y_manipulador = rect_trilha_scrollbar.top + (rect_trilha_scrollbar.height - altura_manipulador) * ratio_scroll

                rect_manipulador_scrollbar = pygame.Rect(
                    rect_trilha_scrollbar.left, pos_y_manipulador,
                    rect_trilha_scrollbar.width, altura_manipulador
                )
                pygame.draw.rect(self.screen, (100, 100, 100, 200), rect_manipulador_scrollbar, border_radius=self.largura_scrollbar // 2)

        self.botao_voltar.draw(self.screen)