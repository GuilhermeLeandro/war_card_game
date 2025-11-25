import unittest
import pygame
from src.ui.ui_utils import draw_linear_gradient_rect
# Testa gradiente vertical


class TestDrawLinearGradientRect(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_vertical_gradient(self):
        surface = pygame.Surface((10, 10))
        rect = (0, 0, 10, 10)
        start_color = (0, 0, 0)      # Preto
        end_color = (255, 255, 255)  # Branco

        draw_linear_gradient_rect(surface, rect, start_color, end_color, vertical=True)

        # Verifica se o topo é preto
        self.assertEqual(surface.get_at((5, 0))[:3], start_color)

        # Verifica se a base é branco
        self.assertEqual(surface.get_at((5, 9))[:3], end_color)

    def test_horizontal_gradient(self):
        surface = pygame.Surface((10, 10))
        rect = (0, 0, 10, 10)
        start_color = (255, 0, 0)    # Vermelho
        end_color = (0, 0, 255)      # Azul

        draw_linear_gradient_rect(surface, rect, start_color, end_color, vertical=False)

        # Verifica se a esquerda é vermelho
        self.assertEqual(surface.get_at((0, 5))[:3], start_color)

        # Verifica se a direita é azul
        self.assertEqual(surface.get_at((9, 5))[:3], end_color)

    def test_empty_rect_vertical(self):
        surface = pygame.Surface((0, 10))  # width zero
        rect = (0, 0, 0, 10)
        try:
            draw_linear_gradient_rect(surface, rect, (0, 0, 0), (255, 255, 255), v_
