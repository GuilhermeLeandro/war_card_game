import pygame

class BaseScreen:
    def __init__(self, screen, manager, font=None):
        self.screen = screen
        self.manager = manager 
        self.font = font if font else pygame.font.Font(None, 30)

    def handle_event(self, event):
        pass 

    def update(self, dt):
        pass 

    def render(self):
        pass 

    def _draw_text(self, text, font, color, x, y, center_x=False, center_y=False, antialias=True):
        text_surface = font.render(text, antialias, color)
        text_rect = text_surface.get_rect()
        if center_x: text_rect.centerx = x
        else: text_rect.x = x
        if center_y: text_rect.centery = y
        else: text_rect.y = y
        self.screen.blit(text_surface, text_rect)
        return text_rect